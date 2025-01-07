from pypacks import Pack

import os
os.chdir(os.path.dirname(__file__))

pack = Pack(
    "Empty Pack", "An empty Datapack + Resource pack", "pypacks_empty",
    resource_pack_path=os.path.join(os.path.dirname(__file__), "resource_pack"),
    datapack_output_path=os.path.join(os.path.dirname(__file__), "datapack")
)
