class Command_Manager {
  constructor(button_id_to_prompt_mapping, prompt_areas_common_class) {
    this.button_id_to_prompt_mapping = button_id_to_prompt_mapping;
    this.prompt_currently_displayed = false;
    this.current_id = 0;
    this.targets_registered = false;
    this.common_class = prompt_areas_common_class;
  }

  get_target_info(id_str) {
    let id = "#" + id_str;
    let target_info = {};
    jQuery(id).children().each(function() {
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

  is_current_prompt_displayed() {
    return this.prompt_currently_displayed;
  }

  get_curr_id() {
    return this.current_id;
  }

  change_prompt(id) {
    if(this.targets_registered) {
      let command_changed = false;
      if(id in this.button_id_to_prompt_mapping) {
        this.current_id = id;
        this.prompt_currently_displayed = false;
        let prompt_area_id = this.button_id_to_prompt_mapping[id];
        jQuery("." + this.common_class).addClass("prompt_na");
        jQuery("#" + prompt_area_id).removeClass("prompt_na");
      }
      return command_changed;
    }
  }
}
