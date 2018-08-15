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

  get_target_info(id_str) {
    let id = "#" + id_str;
    let target_info = {};
    jQuery(id).children().each(function() {
      alert("inside");
      if(jQuery(this).attr("id") == "port") {
        target_info["port"] = jQuery(this).val();
      }
      if(jQuery(this).attr("id") == "host") {
        target_info["host"] = jQuery(this).val();
      }
    });
    return target_info;
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
        let target_info =
                 self.get_target_info(creator.get_current_target_id());
        command_data["target"] = target_info;
        alert(target_info["host"]);
        alert(target_info["port"]);

        alert(command_data);
        // send using dht_creator
        creator.send_data(JSON.stringify(command_data));
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
