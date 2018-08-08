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
    alert("In constructor: " + this.current_id);
  }

  has_command_executed() {
    return this.command_executed;
  }

  execute_command() {
    alert("this.current_id:" + this.current_id);
    alert(this.id_action_mappings[this.current_id]);
    (this.id_action_mappings[this.current_id])();
    this.command_executed = true;
  }

  change_command(id) {
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
