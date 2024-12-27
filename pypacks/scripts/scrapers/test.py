# PUT THIS IN C:\Users\%USERNAME%\AppData\Roaming\.minecraft\versions\<version>\EXTRACTED_JAR
import os
import re

VERSION = "1.21.4"
folder = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\assets\\minecraft\\models\\item"

RE_PATTERN = r"\"layer0\": \"(minecraft:)?(item|block)\/.*\""
mapping = {}

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
