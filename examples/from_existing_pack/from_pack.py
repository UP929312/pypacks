from pypacks import Pack
import zipfile
import shutil

import requests

import os
os.chdir(os.path.dirname(__file__))

IMPORTS = """
from pypacks import Pack
from pypacks.resources import *  # noqa: F403
from pypacks.additions.item_components import *  # noqa: F403
from pypacks.additions import *  # noqa: F403
from pathlib import WindowsPath, PosixPath

"""

existing_datapack = "SimplEnergy_datapack"
datapack_namespace = "simplenergy"
existing_resource_pack = "SimplEnergy_resource_pack"
resource_pack_namespace = "simplenergy"

existing_datapack_zip = "https://github.com/Stoupy51/SimplEnergy/releases/download/v2.0.1/SimplEnergy_datapack.zip"
existing_resource_pack_zip = "https://github.com/Stoupy51/SimplEnergy/releases/download/v2.0.1/SimplEnergy_resource_pack.zip"

datapack_zip = requests.get(existing_datapack_zip)
resource_pack_zip = requests.get(existing_resource_pack_zip)

# Unzip the datapack into a folder
with open(f"{existing_datapack}.zip", "wb") as f:
    f.write(datapack_zip.content)
with zipfile.ZipFile(f"{existing_datapack}.zip", "r") as zip_ref:
    zip_ref.extractall(path=existing_datapack)

# Unzip the resource pack
with open(f"{existing_resource_pack}.zip", "wb") as f:
    f.write(resource_pack_zip.content)
with zipfile.ZipFile(f"{existing_resource_pack}.zip", "r") as zip_ref:
    zip_ref.extractall(path=existing_resource_pack)

# Delete the initial zip files
os.remove(f"{existing_datapack}.zip")
os.remove(f"{existing_resource_pack}.zip")

pack = Pack.from_existing_pack(
    datapack_namespace,
    resource_pack_namespace,
    os.path.join(os.path.dirname(__file__), existing_datapack),
    os.path.join(os.path.dirname(__file__), existing_resource_pack),
)
with open("generated_pack.py", "w", encoding="utf-8") as f:
    f.write(IMPORTS+"pack = "+str(pack))

# Delete the nested folders:
shutil.rmtree(existing_datapack)
shutil.rmtree(existing_resource_pack)