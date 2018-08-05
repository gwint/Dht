class Host_IP_Tuple_Collection {
  constructor(host, port) {
    this.host = host;
    this.port = port;
    this.host_port_tuples = [];
  }

  get_host() {
    return this.host;
  }

  get_port() {
    return this.port;
  }

  add_tuple(host, port) {
    this.host_port_tuples.push([host, port]);
  }
}
