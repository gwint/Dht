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

  connect() {
    //this.socket = new WebSocket("ws://localhost:9999");
  }

  create_dht() {
    if(!this.created) {
      // Create WebSocket connection.
      this.socket = new WebSocket("ws://localhost:9999");

      // Listen for messages
      this.socket.addEventListener('message', function(event) {
        //will listen for responses when commands sent to server
        var a = 10;
        return false;
      });

      this.socket.addEventListener('error', function(event) {
        alert("Error: Could not connect to server!");
        jQuery("#commit_host_port_tuples_btn").attr("disabled", false);
        jQuery("#add_host_ip_tuple_btn").attr("disabled", false);
        jQuery(".entry").attr("readonly", false);
        jQuery(".entry").css("background-color", "white");
        jQuery("#host_ip_tuple_panel").css("background-color", "red");
      });

      // Connection opened
      let self = this;
      this.socket.addEventListener('open', function(event) {
        let ports = self.host_ip_tuples.get_ports();
        alert(ports);
        this.created = true;
        // Send Json object containing port numbers
        self.socket.send(JSON.stringify(ports));
        alert(this.created);

        // Show what success looks like
        jQuery("#create_dht_btn").attr("disabled", true);
        jQuery("#host_ip_tuple_panel").css("background-color", "green");
      });
    }
  }
}
