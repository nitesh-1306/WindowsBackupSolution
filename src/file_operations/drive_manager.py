import os
import json
import psutil
from typing import Final
from file_operations.config_handler import ConfigLoader

class DriveExplorationManager:
    def __init__(self):
        self.config = ConfigLoader().load_config()
        self.folders_to_ignore = self.config['folders_to_ignore']
        self.folders_to_only_name = self.config['folders_to_only_name']
        self.folder_name_pattern_to_ignore = self.config['folder_name_pattern_to_ignore']
        self.files_to_ignore = self.config['files_to_ignore']
        self.file_types_to_ignore = self.config['file_types_to_ignore']
        self.file_name_pattern_to_ignore = self.config['file_name_pattern_to_ignore']
        self.drives_to_ignore = self.config['drives_to_ignore']

        self.output_file="drive_map.json"
        self.no_permission_annotation: Final = {"00files": [],"error": "Permission denied!"}
        self.empty_directory_annotation: Final = {"00files": []}

    def __get_drives(self):
        drives = [partition.device for partition in psutil.disk_partitions()]
        return [drive for drive in drives if drive not in self.drives_to_ignore]
    
    def __scan_directory(self, path):
        structure = {}
        files = []
        file_count = 0

        # Handle no permission paths
        try:
            entries = os.listdir(path)
        except PermissionError:
            return self.no_permission_annotation, file_count

        for entry in entries:
            entry_path = os.path.join(path, entry)

            if entry in self.folders_to_ignore and os.path.isdir(entry_path):
                continue

            parent_folder = os.path.basename(os.path.dirname(entry_path))
            
            if parent_folder in self.folders_to_only_name and os.path.isdir(entry_path):
                structure[entry] = self.empty_directory_annotation
                continue

            if os.path.isdir(entry_path):
                structure[entry], subdir_file_count = self.__scan_directory(entry_path)
                file_count += subdir_file_count
            elif os.path.isfile(entry_path) and entry not in self.files_to_ignore:
                _, filetype = os.path.splitext(entry)
                if filetype and filetype not in self.file_types_to_ignore:
                    files.append(entry)
                    file_count += 1
                    

        structure["00files"] = files
        return structure, file_count

    def __explore_drives(self):
        drives = self.__get_drives()
        drive_files = {}
        file_count = 0

        for drive in drives:
            drive_files[drive], count = self.__scan_directory(drive)
            drive_files[drive.replace('/','')+'_file_count'] = count
            file_count += count
        drive_files['total_files'] = file_count
        return drive_files
    
    def generate_drive_map(self, ):
        drive_map = self.__explore_drives()
        print(f'{drive_map['total_files']} files to be uploaded.')
        with open(self.output_file, "w", encoding="utf-8") as json_file:
            json.dump(drive_map, json_file, indent=4)
        return True

if __name__ == '__main__':
    drive_manager = DriveExplorationManager()
    drive_manager.generate_drive_map()