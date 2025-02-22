import os

VERSION = "1.21.4"
input_path = f"C:\\Users\\{os.environ['USERNAME']}\\AppData\\Roaming\\.minecraft\\versions\\{VERSION}\\{VERSION}\\data\\minecraft"


def search_keyword(directory: str, keyword: str) -> None:
    """Recursively searches for a keyword in all files within a directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line_number, line in enumerate(f, start=1):
                        if keyword in line:
                            print(f"Found in: {file_path} (Line {line_number})")
                            print(f"Extract: {line.strip()}\n")
            except Exception as e:
                print(f"Could not read {file_path}: {e}")


search_keyword(input_path, "set_loot_table")
