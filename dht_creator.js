class Dht_Creator {
  constructor(host_ip_tuple_collection) {
    this.created = false;
    this.host_ip_tuples = host_ip_tuple_collection;
    this.socket = null;
    this.target_id = -1;
  }

  is_dht_created() {
    return this.created;
  }

  get_current_target_id() {
    return this.target_id;
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

  create_dht(manager_arr) {
    if(!this.created) {
      // Create WebSocket connection.
      this.socket = new WebSocket("ws://localhost:9999");

      // Listen for messages
      this.socket.addEventListener('message', function(event) {
        //will listen for responses when commands sent to server
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
        jQuery("#btn_response_area").text("DHT CREATED");
        jQuery(".tuple_container").click(function(event) {
          jQuery(".tuple_container").css("background-color", "grey");
          jQuery(event.currentTarget).css("background-color", "white");
          self.target_id = parseInt(jQuery(event.currentTarget).attr("id"));
          alert(self.get_current_target_id());
        });
        manager_arr[0].register_targets("host_ip_tuple_entry_area");
      });
    }
  }
}
