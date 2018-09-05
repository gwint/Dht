jQuery(document).ready(function() {
  let id_to_html_str_mappings = {};
  let host_ip_tuples = new Host_IP_Tuple_Collection();
  let dht_creator = null;
  let command_manager =
            new Command_Manager({"read_btn":"read_command_prompt",
                                 "write_btn":"write_command_prompt"},
                                 "prompt_area");
  let illustrator = null;

  jQuery("#create_dht_btn").click(function() {
    host_ip_tuples.get_host_port_tuples();
    dht_creator = new Dht_Creator(host_ip_tuples);

    let man_arr = [command_manager];
    dht_creator.create_dht(man_arr);
    command_manager.register_targets("host_ip_tuple_entry_area");

  });

  jQuery("#add_port_btn").click(function() {
    let curr_contents = jQuery("#added_ports").text();
    let new_port = jQuery("#port_entry_box").val();
    let new_contents = curr_contents + "\n" + new_port;
    jQuery("#added_ports").html(jQuery.trim(new_contents));
    jQuery("#port_entry_box").val("");
  });

  jQuery("#add_host_ip_tuple_btn").click(function() {
    let container_open = '<div class="tuple_container">';
    let host_label = '<label for="host">IP:</label>';
    let host_entry = '<input class="host_entry entry" id="host" type="text"/>';
    let port_label = '<label for="port">Port:</label>';
    let port_entry = '<input class="port_entry entry" id="port" type="text"/>';
    let container_close = '</div>';

    html_str = container_open + host_label + host_entry + port_label +
               port_entry + container_close;

    jQuery("#host_ip_tuple_entry_area").append(html_str);
    jQuery("#commit_host_port_tuples_btn").attr("disabled", false);

    jQuery("#host_ip_tuple_entry_area input").change(function() {
      let is_any_input_field_empty = function() {
        let empty = false;
        jQuery("#host_ip_tuple_entry_area input").each(function() {
          if(jQuery(this).val() === "") {
            empty = true;
          }
        });
        return empty;
      };
      if(is_any_input_field_empty()) {
        jQuery("#create_dht_btn").attr("disabled", true);
      }
      else {
        jQuery("#create_dht_btn").attr("disabled", false);
      }
    });
  });

  jQuery(".command_btn").click(function() {
    jQuery(".command_btn").removeClass("pressed_btn");
    jQuery(this).addClass("pressed_btn");

    let pressed_command_btn_id = jQuery(document.activeElement).attr("id");

    if(command_manager != null &&
       (!command_manager.is_current_prompt_displayed() ||
       (command_manager.get_curr_id() != pressed_command_btn_id))) {
      command_manager.change_prompt(pressed_command_btn_id);
    }
  });

  jQuery(".exec_command_btn").click(function() {
    if(dht_creator.get_current_target_id() != -1) {
      let labels = [];
      let values = [];
      let command_data = {"command_id":self.current_id};
      jQuery(".command_label").each(function() {
        labels.push(jQuery(this).text());
      });
      jQuery(".command_input").each(function() {
        values.push(jQuery(this).val());
      });

      command_data["labels"] = labels;
      command_data["values"] = values;
      let target_info =
             self.get_target_info(dht_creator.get_current_target_id());
      command_data["target"] = target_info;

      dht_creator.send_data(JSON.stringify(command_data));
    }
    else {
      alert("Select a node on which to execute the command!");
    }
  });
});
