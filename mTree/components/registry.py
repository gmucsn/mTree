from mTree.components.admin_message import AdminMessage
import json
import sys
import os
import inspect
from pathlib import Path
import time
from datetime import datetime, date

class Registry:
    class __Registry:
        def __init__(self):
            self.server = None
            self.class_list = {}
            self.agent_list = []
            self.institution_list = []
            self.environment_list = []
        def __str__(self):
            return repr(self)



    instance = None

    def __init__(self):
        if not Registry.instance:
            Registry.instance = Registry.__Registry()
        self.class_list = []

    def read_system_run_status_file(self, status_file_location):
        status_file_data = {}
        with open(status_file_location, 'r') as status_file:
            status_file_data = json.load(status_file)
        return status_file_data

    def get_system_run_configuration(self, mes_run_log_dir):
        p = Path(mes_run_log_dir)
        configuration_file_data = {}
        configuration_file_location = [i for i in p.glob('**/*-configuration.json')][0]
        with open(configuration_file_location, 'r') as configuration_file:
            configuration_file_data = json.load(configuration_file)
        return configuration_file_data

    def read_mes_run_sequence_file(self, mes_run_log_dir):
        p = Path(mes_run_log_dir)
        sequence_file_location = [i for i in p.glob('**/*-sequence.log')][0]
        sequence_file_data = ""
        with open(sequence_file_location, 'r') as sequence_file:
            sequence_file_data = sequence_file.read()
        return sequence_file_data

    def get_system_run_log(self, mes_run_log_dir):
        p = Path(mes_run_log_dir)
        experiment_log_location = [i for i in p.glob('**/*-experiment.log')][0]
        experiment_log_file_data = ""
        log_lines = []
        with open(experiment_log_location, 'r') as log_file:
            for line in log_file:
                log_line = {}
                timestamp = ""
                try:
                    split_line = line.split("\t")
                    timestamp = datetime.fromtimestamp(float(split_line[0]))
                    log_line["timestamp"] = str(timestamp)
                    log_line["message"] = " ".join(split_line[1:]).strip()
                except:
                    log_line["message"] = line.strip()

                log_lines.append(log_line)
        return log_lines

    def get_system_data_log(self, mes_run_log_dir):
        p = Path(mes_run_log_dir)
        experiment_data_location = [i for i in p.glob('**/*-experiment.data')]
        if len(experiment_data_location) > 0:
            experiment_data_location = experiment_data_location[0]
        else:
            return [{"message": "NO DATA LOGGED"}]
        experiment_data_file_data = ""
        data_lines = []
        with open(experiment_data_location, 'r') as data_file:
            for line in data_file:
                data_line = {}
                timestamp = ""
                try:
                    split_line = line.split("\t")
                    timestamp = datetime.fromtimestamp(float(split_line[0]))
                    data_line["timestamp"] = str(timestamp)
                    raw_data = " ".join(split_line[1:]).strip()
                    # print(raw_data)
                    line_data = json.loads(raw_data)
                    data_line["message"] = json.dumps(line_data)
                except:
                    line_data = json.loads(" ".join(split_line[1:]).strip())
                    data_line["message"] = json.dumps(line_data)

                data_lines.append(data_line)
        return data_lines

    def get_system_runs(self, run_dir=None):
        if run_dir is None:
            base_dir = os.getcwd() 
        else:
            base_dir = run_dir

        p = Path(base_dir)
        system_runs = [self.read_system_run_status_file(run_status_file) for run_status_file in p.glob('**/.mtree_mes_status.json')]
        return system_runs

    def get_system_run_output(self, mes_run_log_dir):
        p = Path(mes_run_log_dir)
        system_run = [self.read_system_run_status_file(run_status_file) for run_status_file in p.glob('**/.mtree_mes_status.json')][0]
        return system_run

    def get_system_run_output_by_run_code(self, run_code):
        system_runs = self.get_system_runs()
        for run in system_runs:
            if run["run_code"] == run_code:
                break
        
        return run


    def add_class(self, classobject):
        class_name = classobject.__name__
        #class_source = inspect.getfile(classobject).__class__
        class_source = "temp"
        Registry.instance.class_list[class_name] = {"class": classobject, "source": class_source}
        for base_class in classobject.__bases__:
            if base_class.__name__ == "Agent":
                Registry.instance.agent_list.append(class_name)
            elif base_class.__name__ == "Institution":
                Registry.instance.institution_list.append(class_name)
            elif base_class.__name__ == "Environment":
                Registry.instance.environment_list.append(class_name)

    def get_component_class(self, mes_class):
        print("REGISTRY CLASSES AVAILABLE: ")
        for i in Registry.instance.class_list.keys():
            # print("\t", i)
            pass
        classobject = Registry.instance.class_list[mes_class]["class"]
        return classobject

    def get_component_source_file(self, mes_class):
        classobject = Registry.instance.class_list[mes_class]["class"]
        filename = sys.modules[classobject.__module__].__file__
        contents = None
        with open(filename) as f:
            contents = f.read()
        return contents

    def list_contents(self):
        for target in Registry.instance.class_list.keys():
            # print(Registry.instance.class_list[target])
            pass
        
    def clear_contents(self):
        Registry.instance.class_list = {}
        Registry.instance.agent_list = []
        Registry.instance.institution_list = []
        Registry.instance.environment_list = []


    def examine_directory(self, target_directory):
        import importlib
        from importlib import import_module
        module = importlib.import_module("mTree.components")

        import glob
        import sys
        from types import ModuleType
        import os
        
        sys.path.append(target_directory)

        base_module = ModuleType('mTree.components')

        modules_imported = []
        module_names = []
        for filename in glob.iglob(target_directory + '/mes/*.py', recursive=True):
            import_name = os.path.splitext(os.path.basename(filename))[0]
            module_name = "mes." + import_name.partition('.')[0]
            import importlib.util


            #try:
            #    return sys.modules[fullname]
            #except KeyError:
            spec = importlib.util.spec_from_file_location(module_name, filename)
            #spec = importlib.util.find_spec(fullname)
            #sys.modules[module_name] = ModuleType(module_name)
            module = importlib.util.module_from_spec(spec)
            loader = importlib.util.LazyLoader(spec.loader)
            # Make module with proper locking and get it inserted into sys.modules.
            a = loader.exec_module(module)
            sys.modules[module_name] = module
            t = sys.modules[module_name]

            # print(sys.modules[module_name])

         
        sys.modules['mes'] = ModuleType('mes')

        import inspect
        target_class = None
        for name, obj in inspect.getmembers(sys.modules["mTree.server"]):
            if inspect.isclass(obj):
                if obj.__name__ == "CVAEnvironment":
                    target_class = obj



    def list_classes(self):
        return Registry.instance.class_list

    def agent_list(self):
        return Registry.instance.agent_list

    def get_mes_component_details(self, mes_class):
        mes_component_type = None
        directives_schemas = []
        directives = Registry.instance.class_list[mes_class]["class"]._enabled_directives.keys()
        for directive in directives:
            schema = None
            docString = None
            docString = Registry.instance.class_list[mes_class]["class"]._enabled_directives[directive].__doc__
            if directive in Registry.instance.class_list[mes_class]["class"]._enabled_directives_schemas.keys():
                schema =  Registry.instance.class_list[mes_class]["class"]._enabled_directives_schemas[directive]
            directives_schemas.append((directive, schema, docString))
        return directives_schemas

    def get_mes_component_properties(self, mes_class):
        mes_component_type = None
        property_list = []
        properties = Registry.instance.class_list[mes_class]["class"]._mtree_properties.keys()
        for property_name in properties:
            property_list.append((property_name, Registry.instance.class_list[mes_class]["class"]._mtree_properties[property_name]))
        return property_list


    def institution_list(self):
        return Registry.instance.institution_list

    def environment_list(self):
        return Registry.instance.environment_list

    def register_server(self, server):

        Registry.instance.server = server

    def get_server(self):
        return Registry.instance.server

    # this would be a handy class to have decorators on...

    def message(self, message):
        new_message = AdminMessage(message)
        if new_message.request() == "component_list":
            return json.dumps(self.agent_list())






