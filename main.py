import os
import json
import psutil

# Read folders.ignore and folders.name content
def read_config_files():
    """
    Reads configuration files `folders.ignore` and `folders.name` to load ignored and special-handling folder names.
    """
    ignore_list = []
    name_list = []
    
    # Read folders.ignore
    if os.path.exists("folders.ignore"):
        with open("folders.ignore", "r") as f:
            ignore_list = [line.strip() for line in f if line.strip()]
    
    # Read folders.name
    if os.path.exists("folders.name"):
        with open("folders.name", "r") as f:
            name_list = [line.strip() for line in f if line.strip()]
    
    return ignore_list, name_list

def get_drives():
    """
    Use psutil to get all mounted drives except the C drive.
    """
    drives = [partition.device for partition in psutil.disk_partitions()]
    return [drive for drive in drives if not drive.startswith("C:")]

def scan_directory(path, ignore_list, name_list):
    """
    Recursively scan a directory and return its structure as a nested dictionary,
    considering folders to ignore and folders to handle specially.
    """
    structure = {}
    files = []

    # List all entries in the directory
    try:
        entries = os.listdir(path)
    except PermissionError:
        # Skip directories that require elevated permissions
        return {"00files": []}

    for entry in entries:
        entry_path = os.path.join(path, entry)

        # Handle ignored folders
        if entry in ignore_list and os.path.isdir(entry_path):
            continue
        
        # Handle folders in name_list
        if entry in name_list and os.path.isdir(entry_path):
            structure[entry] = {"00files": []}
            continue

        # Explore directories recursively
        if os.path.isdir(entry_path):
            structure[entry] = scan_directory(entry_path, ignore_list, name_list)

        # Add files to the list
        elif os.path.isfile(entry_path):
            files.append(entry)

    # Add files under the key "00files"
    structure["00files"] = files
    return structure

def create_file_structure():
    """
    Create the file structure JSON for all drives except C drive.
    """
    drives = get_drives()
    ignore_list, name_list = read_config_files()
    file_structure = {}

    for drive in drives:
        file_structure[drive] = scan_directory(drive, ignore_list, name_list)

    return file_structure

def export_to_json(file_structure, output_file="file_structure.json"):
    """
    Export the file structure to a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(file_structure, json_file, indent=4)

if __name__ == "__main__":
    # Generate file structure
    file_structure = create_file_structure()

    # Export to JSON
    export_to_json(file_structure)

    print("File structure exported to 'file_structure.json'")
