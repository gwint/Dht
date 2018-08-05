class Host_IP_Tuple_Collection {
  constructor() {
    this.host_port_tuples = [];
  }

  get_ports() {
    let ports = [];
    this.host_port_tuples.forEach(function(tuple) {
      ports.push(tuple[1]);
    });
    alert("ports:" + ports);
    return ports;
  }

  get_hosts() {
  }

  get_host_port_tuples() {
  }

  add_tuple(host, port) {
    this.host_port_tuples.push([host, port]);
  }
}
