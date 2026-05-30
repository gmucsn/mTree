import json
from pathlib import Path
import yaml
from mTree.simulation.configuration import Configuration
from mTree.simulation.mes_description import MESDescription


class Library:
    def __init__(self, scan_current_directory=True):
        self.scan = False
        self.mes_library = {}

        if scan_current_directory is not None:
            self.scan = scan_current_directory
            self.load_libraries_from_directories()

    @staticmethod
    def load_configuration_from_path(path_to_config):
        """
        Method to examine a json or yaml configuration file and to load it into a validate Configuration object
        """

        config_file_path = Path(path_to_config)
        if config_file_path.suffix == ".json":
            with open(config_file_path, "r") as f:
                json_content = json.load(f)
                experiment_configuration = Configuration.model_validate_json(
                    json_content
                )
        elif config_file_path.suffix == ".yaml":
            with open(config_file_path, "r") as f:
                yaml_content = yaml.safe_load(f)
                experiment_configuration = Configuration.model_validate(yaml_content)
        else:
            raise Exception("Invalid Configuration file type")
        return experiment_configuration

    @property
    def mes_list(self):
        return [
            self.mes_library[mes].mes_directory.name for mes in self.mes_library.keys()
        ]

    def configuration_dict(self, mes):
        temp = {
            configuration.name: configuration
            for configuration in self.mes_library[mes].configurations
        }
        return temp

    def load_libraries_from_directories(self):
        # examine the current directory tree and see if there are any MESs inside
        mes_directories = self.find_mes_directories()
        self.mes_library = {
            str(mes_dir.name): self.generate_mes_description(mes_dir)
            for mes_dir in mes_directories
        }

    def generate_mes_description(self, mes_directory: Path):
        config_directory = mes_directory / "config"
        config_files = [config_file for config_file in config_directory.glob("*.json")]
        configurations = []
        for config_file in config_files:
            input_json = config_file.read_text()
            configuration = Configuration.model_validate_json(input_json)
            configuration.file_source = config_file
            configuration.mes_directory = mes_directory
            configurations.append(configuration)
        return MESDescription(
            mes_directory=mes_directory, configurations=configurations
        )

    def find_mes_directories(self):
        starting_directory = Path.cwd()
        mes_directories = []
        for root, dirs, files in starting_directory.walk(top_down=True):
            if "mes" in dirs and "config" in dirs:
                # assume it is a real MES
                mes_directories.append(root)
        return mes_directories
