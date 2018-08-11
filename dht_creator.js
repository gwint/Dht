class Dht_Creator {
  constructor(host_ip_tuple_collection) {
    this.created = false;
    this.host_ip_tuples = host_ip_tuple_collection;
    this.socket = null;
  }

  is_dht_created() {
    return this.created;
  }

  get_state() {
    return this.socket.readyState;
  }

  set_host_ip_tuples(new_host_ip_tuples) {
    this.host_ip_tuples = new_host_ip_tuples;
  }

  clear_host_ip_tuples() {
    this.host_ip_tuples = null;
  }

  create_dht() {
    if(!this.created) {
      // Create WebSocket connection.
      this.socket = new WebSocket("ws://localhost:9999");

      // Listen for messages
      this.socket.addEventListener('message', function(event) {
        //will listen for responses when commands sent to server
      });

      // Connection opened
      let self = this;
      this.socket.addEventListener('open', function(event) {
        let ports = self.host_ip_tuples.get_ports();
        alert(ports);
        this.created = true;
        // Send Json object containing port numbers
        self.socket.send(JSON.stringify(ports));
      });
    }
  }
}
