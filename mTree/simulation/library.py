import os
from pathlib import Path

from mTree.simulation import MESDescription, SimulationDescription


class Library:
    def __init__(self, scan_current_directory=True):
        self.scan = False
        self.mes_library = {}

        if scan_current_directory is not None:
            self.scan = scan_current_directory
            self.load_libraries_from_directories()

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
        simulation_descriptions = []
        for config_file in config_files:
            input_json = config_file.read_text()
            configuration = SimulationDescription.model_validate_json(input_json)
            configuration.file_source = config_file
            configuration.mes_directory = mes_directory
            simulation_descriptions.append(configuration)
        return MESDescription(
            mes_directory=mes_directory, configurations=simulation_descriptions
        )

    def find_mes_directories(self):
        starting_directory = Path.cwd()
        mes_directories = []
        for root, dirs, files in starting_directory.walk(top_down=True):
            if "mes" in dirs and "config" in dirs:
                # assume it is a real MES
                mes_directories.append(root)
        return mes_directories
