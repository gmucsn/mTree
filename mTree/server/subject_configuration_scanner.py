import os
from os import listdir
from os.path import isfile, join
import json

class SubjectConfigurationScanner:
    class __SubjectConfigurationScanner:
        def __init__(self):
            self.configuration_files = []
            self.configuration_directory = None
            self.configurations = {}
            
        def __str__(self):
            return repr(self)


    instance = None

    def __init__(self):
        if not SubjectConfigurationScanner.instance:
            SubjectConfigurationScanner.instance = SubjectConfigurationScanner.__SubjectConfigurationScanner()
        
    def scan_configurations(self):
        SubjectConfigurationScanner.instance.configuration_directory = os.path.join(os.getcwd(), "subject_config")
        SubjectConfigurationScanner.instance.configuration_files = [f for f in listdir(SubjectConfigurationScanner.instance.configuration_directory) if isfile(join(SubjectConfigurationScanner.instance.configuration_directory, f))]
        for configuration in SubjectConfigurationScanner.instance.configuration_files:
            with open(join(SubjectConfigurationScanner.instance.configuration_directory, configuration)) as f:
                data = json.load(f)
                SubjectConfigurationScanner.instance.configurations[configuration] = data

    def get_configurations(self):
        temp = []
        for i in SubjectConfigurationScanner.instance.configurations.keys():
            temp.append([i, json.dumps(SubjectConfigurationScanner.instance.configurations[i]), SubjectConfigurationScanner.instance.configurations[i]])
        return temp
        
        
