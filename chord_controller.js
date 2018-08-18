jQuery(document).ready(function() {
  let id_to_html_str_mappings = {};
  let host_ip_tuples = new Host_IP_Tuple_Collection();
  let dht_creator = null;
  let command_manager = null;

  jQuery("#create_dht_btn").click(function() {
    let man_arr = [command_manager];
    dht_creator.create_dht(man_arr);
    // Draw circle on dht_drawing_area
    let ctx = document.getElementById("drawing_pad").getContext("2d");
    ctx.beginPath();
    ctx.arc(100, 75, 50, 0, 2*Math.PI);
    ctx.stroke();
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
  });

  jQuery("#commit_host_port_tuples_btn").click(function() {
    let hosts = [];
    let ports = [];

    jQuery("#host_ip_tuple_entry_area input").each(function() {
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

    for(let i = 0; i < hosts.length; i++) {
      host_ip_tuples.add_tuple(hosts[i], parseInt(ports[i], 10));
    }
    dht_creator = new Dht_Creator(host_ip_tuples);
  });

  jQuery(".command_btn").click(function() {
    jQuery(".command_btn").css("border-style", "outset");
    jQuery(this).css("border-style", "inset");

    let id = jQuery(this).attr("id");
    if(command_manager != null &&
       (!command_manager.has_command_executed() ||
       (command_manager.get_curr_id() != id))) {
      command_manager.change_prompt(id);
      command_manager.show_prompt(dht_creator);
    }
  });

  jQuery.get("command_prompt_template.html #command_prompt_template", function(data) {
    jQuery("head").append(data);
    let replace_command_prompt = function(parent, html_str) {
      jQuery(parent).html(html_str);
    };

    let template = jQuery("#command_prompt_template").html();
    let btn_template = jQuery("#exec_command_btn_template").html();

    let template_script = Handlebars.compile(template);
    let btn_script = Handlebars.compile(btn_template);

    let add_btn_context = [{"label":"Host:"},
                           {"label":"Port:"},
                           {"btn_text":"Add Node"}];
    let read_data_context = [{"label":"File Name:"},
                             {"label":"Owner:"},
                             {"btn_text":"Read Data"}];
    let write_data_context = [{"label":"File:"},
                              {"label":"Owner:"},
                              {"label":"Contents:"},
                              {"btn_text":"Write Data"}];

    id_to_html_str_mappings["add_btn"] = function() {
      let html_str = template_script(add_btn_context[0]) + "<br>" +
                     template_script(add_btn_context[1]) + "<br>" +
                     btn_script(add_btn_context[2]);
      replace_command_prompt("#command_prompt_area", html_str);
    };
    id_to_html_str_mappings["read_btn"] = function() {
      let html_str = template_script(read_data_context[0]) + "<br>" +
                     template_script(read_data_context[1]) + "<br>" +
                     btn_script(read_data_context[2]);
      replace_command_prompt("#command_prompt_area", html_str);
    };
    id_to_html_str_mappings["write_btn"] = function() {
      let html_str = template_script(write_data_context[0]) + "<br>" +
                     template_script(write_data_context[1]) + "<br>" +
                     template_script(write_data_context[2]) + "<br>" +
                     btn_script(write_data_context[3]);
      replace_command_prompt("#command_prompt_area", html_str);
    };
    command_manager = new Command_Manager(id_to_html_str_mappings);
  });
});
