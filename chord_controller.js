jQuery(document).ready(function() {
  let host_ip_tuples = new Host_IP_Tuple_Collection();
  let dht_creator = null;

  jQuery("#create_dht_btn").click(function() {
    jQuery("#btn_response_area").text("DHT CREATED");
    dht_creator.create_dht();
  });

  jQuery("#add_port_btn").click(function() {
    let curr_contents = jQuery("#added_ports").text();
    let new_port = jQuery("#port_entry_box").val();
    let new_contents = curr_contents + "\n" + new_port;
    alert(new_contents);
    jQuery("#added_ports").html(jQuery.trim(new_contents));
    jQuery("#port_entry_box").val("");
  });

  jQuery(".command_bar").click(function() {
    jQuery(".command_bar").css("background-color", "white");
    jQuery(this).css("background-color", "grey");
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
});
