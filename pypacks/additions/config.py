from dataclasses import dataclass


@dataclass
class Config:
    """Allows for configuration of the library.<br>
    generate_reference_book -> Whether to generate a refrence book for the pack.<br>
    enable_language_propogation -> Whether to copy over translations for common languages (e.g. en_us -> en_ca).<br>
    warn_about_tags_with_custom_items -> If an Item tag with a custom item in it is used in a recipe, raise a warning (will use the base item instead!).<br>
    generate_create_wall_command -> Creates a command which generates all the custom items on a big wall using item frames.<br>
    warn_about_non_marked_macro_line -> Raises a warning if any line in a mcfunction references a macro `$(x)` without marking that command as a macro
    """
    generate_reference_book: bool = True
    enable_language_propogation: bool = False
    warn_about_tags_with_custom_items: bool = True
    generate_create_wall_command: bool = True  # Generate a command to create a wall of our custom items (/function <namespace>:create_wall).
    warn_about_non_marked_macro_line: bool = True
    # auto_generate_block_varients: bool = False  # ( Auto create slabs from full blocks.
    # send_analytics: bool = True  # Send anonymous analytics to the developer (me).
    # warn_about_world_gen_warning: bool = True  # Warn about world generation warnings (Experimental warning).
