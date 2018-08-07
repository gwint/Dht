class Command_Manager {
  constructor(command_action_mappings) {
    this.command_action_mappings = command_action_mappings;
    this.current_command = function(command_mappings) {
      let first_command = null;
      if(command_mappings.length > 0) {
        let first_command = command_mappings.shift();
      }
      return first_command;
    }(command_action_mappings);
  }

  execute_command() {
    this.command_action_mappings[this.current_command]();
  }

  change_command(new_command) {
    let command_changed = false;
    if(new_command in this.command_action_mappings) {
      this.current_command = new_command;
      command_changed = true;
    }
    return command_changed;
  }
}
