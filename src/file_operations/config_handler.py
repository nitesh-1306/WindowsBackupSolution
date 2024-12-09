import yaml

class ConfigLoader:
    def __init__(self, file_path='config.yaml'):
        self.file_path = file_path

    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                config = yaml.safe_load(file)
                return config if config else {}
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{self.file_path}' does not exist.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file '{self.file_path}': {e}")

if __name__ == "__main__":
    try:
        loader = ConfigLoader()
        config_data = loader.load_config()
        print("Configuration Loaded:", config_data)
    except Exception as e:
        print(e)
