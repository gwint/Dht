class Host_IP_Tuple_Collection {
  constructor() {
    this.host_port_tuples = [];
    //this.container_id = tuple_container_id;
  }

  get_ports() {
    let ports = [];
    this.host_port_tuples.forEach(function(tuple) {
      ports.push(tuple[1]);
    });
    return ports;
  }

  get_host_port_tuples() {
    let hosts = [];
    let ports = [];

    jQuery("#host_ip_tuple_entry_area input").each(function() {
      let has_classes = jQuery(this).attr("class") != undefined;

      if(has_classes) {
        let class_list = jQuery(this).attr("class").split(" ");
        for(let idx in class_list) {
          let class_name = class_list[idx];
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
    jQuery("#create_dht_btn").attr("disabled", false);
    for(let i = 0; i < hosts.length; i++) {
      this.add_tuple(hosts[i], parseInt(ports[i], 10));
    }
  }

  add_tuple(host, port) {
    this.host_port_tuples.push([host, port]);
  }
}
