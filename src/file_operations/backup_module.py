import os
from tqdm import tqdm
from cloud_modules.catbox_cloud import CloudStorage

def upload_files_from_list(file_list_path: str):
    cloud_storage = CloudStorage()

    if not os.path.exists(file_list_path):
        print(f"File list not found: {file_list_path}")
        return

    with open(file_list_path, "r") as file:
        file_paths = [line.strip() for line in file.readlines() if line.strip()]

    if not file_paths:
        print("No file paths found in the list.")
        return

    print(f"Starting upload of {len(file_paths)} files...")

    with open("uploaded_urls.txt", "w") as url_file:
        with open("failed_uploads.txt", "w") as failed_file:
            for file_path in tqdm(file_paths, desc="Uploading files", unit="file"):
                try:
                    if not os.path.exists(file_path):
                        print(f"File not found: {file_path}")
                        continue
                    upload_result = cloud_storage.upload_to_cloud(file_path)
                    if upload_result:
                        url_file.write(f"{file_path} -> {upload_result}\n")
                    else:
                        failed_file.write(f"{file_path}\n")
                except Exception as e:
                    print(f"[ERROR] File: {file_path} encountered an error: {e}")

def main():
    file_list_path = "file_paths.txt"
    upload_files_from_list(file_list_path)

if __name__ == "__main__":
    main()