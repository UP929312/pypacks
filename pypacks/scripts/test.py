# PUT THIS IN C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions\<version>\EXTRACTED_JAR
import os
import re

RE_PATTERN = r"\"layer0\": \"(minecraft:)?(item|block)\/.*\""
mapping = {}

folder = "assets/minecraft/models/item"
for item_model_file in os.listdir(folder):
    with open(f"{folder}/{item_model_file}") as file:
        data = file.read()

    match = re.search(RE_PATTERN, data)
    if match is None:
        pass
        # print(f"Couldn't find anything for {item_model_file}")
    else:
        mapping[item_model_file.removesuffix(".json")] = match.group(0).split("/")[1].removesuffix("\"")

print(mapping)
