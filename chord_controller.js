var DHT_CREATED = false;

function create_dht() {
  if(!DHT_CREATED) {
    // Create WebSocket connection.
    const socket = new WebSocket('ws://localhost:9999');

    // Connection opened
    socket.addEventListener('open', function (event) {
      socket.send('Hello Server!');
    });

    // Listen for messages
    socket.addEventListener('message', function (event) {
      console.log('Message from server ', event.data);
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
    let new_contents = curr_contents + "<br>" + new_port;
    alert(new_contents);
    jQuery("#added_ports").html(new_contents);
    jQuery
  });
});
