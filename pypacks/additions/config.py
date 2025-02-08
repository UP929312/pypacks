from dataclasses import dataclass


@dataclass
class Config:
    """Allows for configuration of the library.<br>
    generate_refrence_book -> Whether to generate a refrence book for the pack.<br>
    enable_language_propogation -> Whether to copy over translations for common languages (e.g. en_us -> en_ca)."""
    generate_refrence_book: bool = True
    enable_language_propogation: bool = False
    # auto_generate_block_varients: bool = False  # Auto create slabs from full blocks.
