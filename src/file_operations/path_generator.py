import json
import os

def extract_file_paths(base_path, data, result):
    """
    Recursively extracts valid file paths from the JSON data.
    Validates that the file exists and is below the size limit.

    :param base_path: The current directory path being processed.
    :param data: The current level of the JSON data.
    :param result: The list to store valid file paths.
    """
    for key, value in data.items():
        if key == "00files" and isinstance(value, list):
            for file in value:
                full_path = os.path.join(base_path, file)
                if os.path.isfile(full_path):
                    # Check file size
                    file_size_mb = os.path.getsize(full_path) / (1024 * 1024)
                    if file_size_mb > 195:
                        print(f"Skipped (over 195 MB): {full_path}")
                    else:
                        result.append(full_path.replace('\\','/'))
                else:
                    print(f"File not found: {full_path}")
        elif isinstance(value, dict):
            extract_file_paths(os.path.join(base_path, key), value, result)

def main():
    # Replace 'input.json' with the actual file path of your JSON file
    json_file_path = 'drive_map.json'
    output_file_path = 'file_paths.txt'

    # Read the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    result = []
    for key, value in data.items():
        if isinstance(value, dict):
            extract_file_paths(key, value, result)

    # Write the extracted file paths to the output file
    with open(output_file_path, 'w') as file:
        for path in result:
            file.write(path + '\n')

    print(f"File paths saved to {output_file_path}")

if __name__ == "__main__":
    main()
