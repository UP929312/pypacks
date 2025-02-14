from pypacks import Pack, Config

import os
os.chdir(os.path.dirname(__file__))

pack = Pack(
    "Empty Pack", "An empty Datapack + Resource pack", "pypacks_empty",
    config=Config(generate_reference_book=False, generate_create_wall_command=False),
    resource_pack_path=os.path.join(os.path.dirname(__file__), "resource_pack"),
    datapack_output_path=os.path.join(os.path.dirname(__file__), "datapack")
)
