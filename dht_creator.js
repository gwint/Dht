class Dht_Creator {
  constructor(host_ip_tuple_collection) {
    this.created = false;
    this.host_ip_tuples = host_ip_tuple_collection;
  }

  is_dht_created() {
    return this.created;
  }

  create_dht() {
    if(!this.created) {
      // Create WebSocket connection.
      const socket = new WebSocket("ws://localhost:9999");

      // Listen for messages
      socket.addEventListener('message', function(event) {
      });

      // Connection opened
      let self = this;
      socket.addEventListener('open', function(event) {
        alert(self.host_ip_tuples.get_ports());
        // Send Json object containing port numbers
        //let port_list_contents = (jQuery("#added_ports").val()).split("\n").map(
        //                       function(port_str) {
        //                         return parseInt(port_str);
        //                       });
        //let ports = port_list_contents;
        //socket.send(JSON.stringify(ports));
      });

    this.created = true;
    }
  }
}
