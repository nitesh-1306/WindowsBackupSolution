import psutil
import os

def list_non_c_drives():
    drives = [disk.device for disk in psutil.disk_partitions(all=False)]
    non_c_drives = [drive for drive in drives if not drive.startswith("C:")]
    return non_c_drives

def list_folders_in_drive(drive):
    try:
        folders = [f.name for f in os.scandir(drive) if f.is_dir()]
        if folders:
            print(f"Folders in {drive}:")
            for folder in folders:
                print(f"- {folder}")
        else:
            print(f"No folders found in {drive}.")
    except PermissionError:
        print(f"Permission denied while accessing {drive}.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    non_c_drives = list_non_c_drives()
    if not non_c_drives:
        print("No drives found apart from C.")
        return

    print("Drives excluding C:")
    for idx, drive in enumerate(non_c_drives, start=1):
        print(f"{idx}. {drive}")

    try:
        choice = int(input("Select a drive by entering the number: ")) - 1
        if 0 <= choice < len(non_c_drives):
            selected_drive = non_c_drives[choice]
            list_folders_in_drive(selected_drive)
        else:
            print("Invalid choice. Please run the program again.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
