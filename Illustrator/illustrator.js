class Dht_Illustrator {
  constructor(a_drawing_area_id, some_port_host_tuples) {
    this.drawing_area_id = a_drawing_area_id;
    this.port_host_tuples = some_port_host_tuples;
  }

  draw_dht() {
    let ctx = document.getElementById(this.drawing_area_id).getContext("2d");
    ctx.beginPath();
    let center_x = document.getElementById(this.drawing_area_id).width / 2;
    let center_y = document.getElementById(this.drawing_area_id).height / 2;
    ctx.arc(center_x, center_y, 50, 0, 2*Math.PI);
    ctx.stroke();
  }

  add_node(host, port) {
  }

  remove_node(host, port) {
  }
}
