var DHT_CREATED = false;

function create_dht() {
  if(!DHT_CREATED) {
    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:9999');
    console.log("got here though");

    // Listen for messages
    socket.addEventListener('message', function (event) {
      alert("received message");
      console.log('Message from server ', event.data);
    });


    // Connection opened
    socket.addEventListener('open', function (event) {
      console.log("open method called");
      socket.send('Hello Server!');
      // Send Json object containing port numbers
      port_list_contents = (jQuery("#added_ports").val()).split("\n");
      alert(port_list_contents);
      let ports = {to:"http://localhost",
                   message:{port_list_contents}};
      alert(JSON.stringify(ports));
      socket.send(JSON.stringify(ports));
    });

    DHT_CREATED = true;
  }
}

jQuery(document).ready(function() {
  jQuery("#create_dht_btn").click(function() {
    jQuery("#btn_response_area").text("DHT CREATED");
    create_dht();
  });

  jQuery("#add_port_btn").click(function() {
    let curr_contents = jQuery("#added_ports").text();
    let new_port = jQuery("#port_entry_box").val();
    let new_contents = curr_contents + "\n" + new_port;
    alert(new_contents);
    jQuery("#added_ports").html(jQuery.trim(new_contents));
    jQuery("#port_entry_box").val("");
  });
});
