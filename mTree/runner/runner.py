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
from mTree.microeconomic_system.simulation_container import SimulationContainer

from mTree.components import registry


class Runner():
    def __init__(self, config_file, multi_simulation=False):
        self.component_registry = registry.Registry()
        self.component_registry.register_server(self)
        self.multi_simulation = multi_simulation
        if self.multi_simulation is not True:
            self.configuration = self.load_mtree_config(config_file)
        else:
            self.configuration = self.load_multiple_mtree_config(config_file)
        print("Runner")
        print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))


    def load_mtree_config(self, config_file):
        configuration = None
        with open(config_file) as json_file:
            configuration = json.load(json_file)
        return [configuration]

    def load_json_multiple(self, segments):
        chunk = ""
        for segment in segments:
            chunk += segment
            try:
                yield json.loads(chunk)
                chunk = ""
            except ValueError:
                pass

    def load_multiple_mtree_config(self, config_file):
        configurations = []
        with open(config_file) as f:
            for parsed_json in self.load_json_multiple(f):
                configurations.append(parsed_json)

        return configurations



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
        if self.multi_simulation is False:
            self.launch_multi_simulations()
        else:
            self.launch_multi_simulations()


    def launch_multi_simulations(self):
        container = SimulationContainer()
        container.create_dispatcher()
        container.send_dispatcher_simulation_configurations(self.configuration)

    def launch_simulation(self):
        component_registry = registry.Registry()

        environment = component_registry.get_component_class(self.configuration["environment"])
        institution = component_registry.get_component_class(self.configuration["institution"])
        agents = []
        for agent_d in self.configuration["agents"]:
            agent_class = component_registry.get_component_class(agent_d["agent_name"])
            agent_count = agent_d["number"]
            agents.append((agent_class, agent_count))

        container = Container()
        properties = None
        if "properties" in self.configuration.keys():
            properties = self.configuration["properties"]
        container.create_root_environment(environment, properties)
        container.setup_environment_institution(institution)
        for agent in agents:
            container.setup_environment_agents(agent[0], agent[1])

        start_message = Message()
        start_message.set_sender("experimenter")
        start_message.set_directive("start_environment")
        container.send_root_environment_message(start_message)

        # create Collateal Game Environment
        #self.container.create_root_environment(self.configuration["environment"])
