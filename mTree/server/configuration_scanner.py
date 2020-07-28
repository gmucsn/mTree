import os
from os import listdir
from os.path import isfile, join
import json

class ConfigurationScanner:
    class __ConfigurationScanner:
        def __init__(self):
            self.configuration_files = []
            self.configuration_directory = None
            self.configurations = {}
            
        def __str__(self):
            return repr(self)


    instance = None

    def __init__(self):
        if not ConfigurationScanner.instance:
            ConfigurationScanner.instance = ConfigurationScanner.__ConfigurationScanner()
        
    def scan_configurations(self):
        ConfigurationScanner.instance.configuration_directory = os.path.join(os.getcwd(), "config")
        ConfigurationScanner.instance.configuration_files = [f for f in listdir(ConfigurationScanner.instance.configuration_directory) if isfile(join(ConfigurationScanner.instance.configuration_directory, f))]
        for configuration in ConfigurationScanner.instance.configuration_files:
            with open(join(ConfigurationScanner.instance.configuration_directory, configuration)) as f:
                data = json.load(f)
                ConfigurationScanner.instance.configurations[configuration] = data

    def get_configurations(self):
        temp = []
        for i in ConfigurationScanner.instance.configurations.keys():
            temp.append([i, json.dumps(ConfigurationScanner.instance.configurations[i]), ConfigurationScanner.instance.configurations[i]])
        return temp
        
        
