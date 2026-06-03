import json
from pathlib import Path

import yaml

from mTree.simulation.configuration import Configuration
from mTree.simulation.mes_description import MESDescription


class Library:
    def __init__(self, starting_directory=None):
        self.starting_directory = starting_directory
        self.mes_library = {}
        if starting_directory is None:
            self.starting_directory = Path.cwd()
        self.load_libraries_from_directories()

    @staticmethod
    def load_configuration_from_path(path_to_config):
        """
        Method to examine a json or yaml configuration file and to load it into a validate Configuration object
        """

        config_file_path = Path(path_to_config)
        experiment_configuration = Configuration.load_from_file(config_file_path)
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
        config_files = [config_file for config_file in config_directory.iterdir() if config_file.suffix in [".json", ".yaml"]]
        configurations = []
        for config_file in config_files:
            configuration = Configuration.load_from_file(config_file)
            configuration.file_source = config_file
            configuration.mes_directory = mes_directory
            configurations.append(configuration)
        return MESDescription(
            mes_directory=mes_directory, configurations=configurations
        )

    def find_mes_directories(self):
        mes_directories = []
        for root, dirs, files in self.starting_directory.walk(top_down=True):
            if "mes" in dirs and "config" in dirs:
                # assume it is a real MES
                mes_directories.append(root)
        return mes_directories
