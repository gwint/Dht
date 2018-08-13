class Command_Manager {
  constructor(id_action_mappings) {
    this.id_action_mappings = id_action_mappings;
    this.command_executed = false;
    this.current_id = function(command_mappings) {
      let first_id = null;
      if((Object.keys(command_mappings)).length > 0) {
        first_id = (Object.keys(command_mappings)).shift();
      }
      return first_id;
    }(id_action_mappings);
    this.curr_ip_host_tuple_idx = -1;
    this.targets_registered = false;
  }

  register_targets(parent_element_id) {
    let self = this;
    let curr_idx = 0;
    let id = "#" + parent_element_id;
    jQuery(id).children().each(function() {
      jQuery(this).attr("id", curr_idx.toString());
      curr_idx++
    });
    this.targets_registered = true;
  }

  unregister_targets(parent_element_id) {
    let self = this;
    let id = "#" + parent_element_id;
    jQuery(id).children().each(function() {
      jQuery(this).removeAttr("id");
    });
    this.targets_registered = false;
  }

  has_command_executed() {
    return this.command_executed;
  }

  get_curr_id() {
    return this.current_id;
  }

  show_prompt(creator) {
    if(this.targets_registered) {
      alert("this.current_id:" + this.current_id);
      alert(this.id_action_mappings[this.current_id]);
      (this.id_action_mappings[this.current_id])();
      this.command_executed = true;

      // Attach handler to execute command button
      self = this;
      jQuery("#exec_command_btn").click(function() {
        alert("pressed");
        let labels = [];
        let values = [];
        let command_data = {"command_id":self.current_id};
        jQuery(".command_label").each(function() {
          labels.push(jQuery(this).text());
        });
        jQuery(".command_input").each(function() {
          values.push(jQuery(this).val());
        });

        alert(labels);
        alert(values);
        command_data["labels"] = labels;
        command_data["values"] = values;

        alert(command_data);

        // send using dht_creator
      });
    }
  }

  change_prompt(id) {
    if(this.targets_registered) {
      let command_changed = false;
      if(id in this.id_action_mappings &&
         id != this.current_id) {
        this.current_id = id;
        command_changed = true;
        this.command_executed = false;
      }
      return command_changed;
    }
  }
}
