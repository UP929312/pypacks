import requests
from zipfile import ZipFile
import io


def get_minecraft_font() -> io.BytesIO:
    # This is a download to the font ZIP file, we need to extract the TTF file from it
    font_zip = requests.get("https://dl.dafont.com/dl/?f=minecraftia").content  # This is the in-game text
    # https://dl.dafont.com/dl/?f=minecrafter  # This is the title/main menu text

    # Open the ZIP file from memory
    with ZipFile(io.BytesIO(font_zip)) as zip:
        # Extract the first font file to an in-memory BytesIO object
        ttf_filename = [name for name in zip.namelist() if name.lower().endswith(".ttf")][0]
        with zip.open(ttf_filename) as extracted_file:
            ttf_data = io.BytesIO(extracted_file.read())
            # ttf_bytes = ttf_data.getvalue()  # Convert from BytesIO to regular Python bytes
    return ttf_data
