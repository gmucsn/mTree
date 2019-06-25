import sys, getopt
import json
import importlib
import inspect
import os
import glob

import importlib.util
import sys

from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container
from mTree.components import registry


class Runner():
    def __init__(self, config_file):
        self.component_registry = registry.Registry()
        self.component_registry.register_server(self)
        self.configuration = self.load_mtree_config(config_file)
        print("Runner")
        print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))


    def load_mtree_config(self, config_file):
        configuration = None
        with open(config_file) as json_file:
            configuration = json.load(json_file)
        return configuration

    def examine_directory(self):
        import importlib
        from importlib import import_module
        module = importlib.import_module("mTree.components")

        import glob
        import sys
        from types import ModuleType
        import os
        cwd = os.getcwd()
        sys.path.append(cwd)

        base_module = ModuleType('mTree.components')

        #base_module = ModuleType('cva_mes')
        #sys.modules['cva_mes'] = ModuleType('cva_mes')
        #sys.modules['cva_mes.cva_environment'] = ModuleType('cva_mes.cva_environment')
        #"cva_mes."
        #globals()[module_name] = foo

        modules_imported = []
        module_names = []
        for filename in glob.iglob('./mes/*.py', recursive=True):


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
            print(sys.modules[module_name])
            #return module

            #foo = importlib.util.module_from_spec(spec)
            #loader = importlib.util.LazyLoader(spec.loader)

            #globals()[module_name] = module
            #print(module)
            #modules_imported.append((module, spec))
            #module_names.append(module)
            #print(foo)
            #base_module


            #spec.loader.exec_module(foo)
            #sys.modules[module_name] = module
            # print(foo)
            #foo.MyClass()
            # module_path = module
            #
            # module_name = os.path.basename(filename)
            # new_module = __import__(module_name, fromlist=[filename])
            # print(new_module)
            # globals()[module_name] = new_module
        #all_my_base_classes = {cls.__name__: cls for cls in base._MyBase.__subclasses__()}

        sys.modules['mes'] = ModuleType('mes')

        import inspect
        target_class = None
        for name, obj in inspect.getmembers(sys.modules["mTree.server"]):
            if inspect.isclass(obj):
                if obj.__name__ == "CVAEnvironment":
                    target_class = obj

        # print("SHOULD HAVE LOADED THEM>>>>")
        # print(module_names)
        # print("ABOVE")
        # test = modules_imported[0]
        # for i in modules_imported:
        #     print("\t\tAbout to load: ", i[0])
        #     try:
        #         i[1].loader.exec_module(i[0])
        #     except Exception as e:
        #         print("ISSUE LOADING")
        #         print(e)
        #         print("<<<<<<<<")
        # print(test)
        #spec.loader.exec_module(test)

    def runner(self):
        self.examine_directory()
        self.launch_simulation()

    def launch_simulation(self):

        component_registry = registry.Registry()
        #print(component_registry.environment_list())

        #print(self.configuration["environment"])
        environment = component_registry.get_component_class(self.configuration["environment"])
        institution = component_registry.get_component_class(self.configuration["institution"])
        agents = []
        for agent_d in self.configuration["agents"]:
            agent_class = component_registry.get_component_class(agent_d["agent_name"])
            agent_count = agent_d["number"]
            agents.append((agent_class, agent_count))

        container = Container()
        container.create_root_environment(environment)
        container.setup_environment_institution(institution)
        for agent in agents:
            container.setup_environment_agents(agent[0], agent[1])

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        print("start message sent to the environment...")
        container.send_root_environment_message(start_message)

        # create Collateal Game Environment
        #self.container.create_root_environment(self.configuration["environment"])
