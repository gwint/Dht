jQuery(document).ready(function() {

  let id_to_html_str_mappings = {};
  let host_ip_tuples = new Host_IP_Tuple_Collection();
  let dht_creator = null;
  let command_manager = null;

  jQuery("#create_dht_btn").click(function() {
    jQuery("#btn_response_area").text("DHT CREATED");
    dht_creator.create_dht();
    jQuery("#create_dht_btn").attr("disabled", true);
  });

  jQuery("#add_port_btn").click(function() {
    let curr_contents = jQuery("#added_ports").text();
    let new_port = jQuery("#port_entry_box").val();
    let new_contents = curr_contents + "\n" + new_port;
    alert(new_contents);
    jQuery("#added_ports").html(jQuery.trim(new_contents));
    jQuery("#port_entry_box").val("");
  });

  jQuery("#add_host_ip_tuple_btn").click(function() {
    let host_label = '<label for="host">IP:</label>';
    let host_entry = '<input class="host_entry entry" id="host" type="text"/>';
    let port_label = '<label for="port">Port:</label>';
    let port_entry = '<input class="port_entry entry" type="text"/>';

    html_str = host_label + host_entry + port_label +
               port_entry + "<br>";

    jQuery("#host_ip_tuple_entry_area").append(html_str);
    jQuery("#commit_host_port_tuples_btn").attr("disabled", false);
  });

  jQuery("#commit_host_port_tuples_btn").click(function() {
    let hosts = [];
    let ports = [];
    //loop through all hosts and ports
    jQuery("#host_ip_tuple_entry_area").children().each(function() {
      let has_classes = jQuery(this).attr("class") != undefined;

      if(has_classes) {
        let class_list = jQuery(this).attr("class").split(" ");
        for(let idx in class_list) {
          class_name = class_list[idx];
          if(class_name == "host_entry") {
            hosts.push(jQuery(this).val());
            jQuery(this).css("background-color", "grey");
            jQuery(this).attr("readonly", true);
          }
          if(class_name == "port_entry") {
            ports.push(jQuery(this).val());
            jQuery(this).css("background-color", "grey");
            jQuery(this).attr("readonly", true);
          }
        }
      }
    });
    jQuery("#commit_host_port_tuples_btn").attr("disabled", true);
    jQuery("#add_host_ip_tuple_btn").attr("disabled", true);
    jQuery("#create_dht_btn").attr("disabled", false);
    alert(hosts);
    alert(ports);
    // place into collection object
    for(let i = 0; i < hosts.length; i++) {
      host_ip_tuples.add_tuple(hosts[i], ports[i]);
    }
    alert(host_ip_tuples);
    dht_creator = new Dht_Creator(host_ip_tuples);
    alert(dht_creator);
  });


  jQuery(".command_btn").click(function() {
    if(dht_creator != null && dht_creator.is_dht_created()) {
      jQuery(".command_btn").css("border-style", "outset");
      jQuery(this).css("border-style", "inset");

      let id = jQuery(this).attr("id");
      if(command_manager != null &&
         !command_manager.has_command_executed()) {
        command_manager.change_command(id);
        command_manager.execute_command();
      }
    }
  });


  jQuery.get("command_prompt_template.html #command_prompt_template", function(data) {
    jQuery("head").append(data);
    let replace_command_prompt = function(parent, html_str) {
      jQuery(parent).append(html_str);
    };

    let template = jQuery("#command_prompt_template").html();
    let template_script = Handlebars.compile(template);

    let add_btn_context = [{"label":"Host"},
                           {"label":"Port"}];
    let read_data_context = [{"label":"File Name"},
                             {"label":"Owner"}];

    id_to_html_str_mappings["add_btn"] = function() {
      let html_str = template_script(add_btn_context[0]) +
                     template_script(add_btn_context[1]);
      replace_command_prompt("#command_prompt_area", html_str);
    };
    id_to_html_str_mappings["read_btn"] = function() {
      let html_str = template_script(read_data_context[0]) +
                     template_script(read_data_context[1]);
      replace_command_prompt("#command_prompt_area", html_str);
    };

    command_manager = new Command_Manager(id_to_html_str_mappings);
  });



});
