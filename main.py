import os
import json
import psutil
from typing import Final


class DriveExplorer:
    def __init__(self):
        self.folders_ignore_config: Final = 'folders.ignore'
        self.folders_only_name_config: Final = 'folders.name'
        self.c_drive: Final = 'C:'
        self.ignore_folders_list = []
        self.only_names_list = []
        self.no_permission_annotation = {"00files": [],"error": "Permission denied!"}
        self.empty_directory_annotation = {"00files": []}

        # Loading the configurations
        self.read_config_files()

    def read_config_files(self):

        if os.path.exists(self.folders_ignore_config):
            with open(self.folders_ignore_config, "r") as f:
                self.ignore_folders_list = [line.strip() for line in f if line.strip()]

        if os.path.exists(self.folders_only_name_config):
            with open(self.folders_only_name_config, "r") as f:
                self.only_names_list = [line.strip() for line in f if line.strip()]

        return True
    
    def get_drives(self):
        drives = [partition.device for partition in psutil.disk_partitions()]
        return [drive for drive in drives if not drive.startswith(self.c_drive)]
    
    def scan_directory(self, path):
        structure = {}
        files = []

        try:
            entries = os.listdir(path)
        except PermissionError:
            return self.no_permission_annotation

        for entry in entries:
            entry_path = os.path.join(path, entry)

            if entry in self.ignore_folders_list and os.path.isdir(entry_path):
                continue
            
            if entry in self.only_names_list and os.path.isdir(entry_path):
                structure[entry] = self.empty_directory_annotation
                continue

            if os.path.isdir(entry_path):
                structure[entry] = self.scan_directory(entry_path)

            elif os.path.isfile(entry_path):
                files.append(entry)

        structure["00files"] = files
        return structure
    
    def create_file_structure(self):
        drives = self.get_drives()
        file_structure = {}

        for drive in drives:
            file_structure[drive] = self.scan_directory(drive)

        return file_structure
    
    def export_to_json(self, output_file="file_structure.json"):
        file_structure = self.create_file_structure()

        with open(output_file, "w", encoding="utf-8") as json_file:
            json.dump(file_structure, json_file, indent=4)


if __name__ == "__main__":
    explore = DriveExplorer()
    explore.export_to_json()
    print("File structure exported to 'file_structure.json'")
