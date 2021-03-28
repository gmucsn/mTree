import sys, getopt
import json
import importlib
import inspect
import os
import glob

import importlib.util
import sys
import time

from mTree.microeconomic_system.dispatcher import Dispatcher

from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container
from mTree.microeconomic_system.simulation_container import SimulationContainer
from thespian.actors import *
from mTree.components import registry

import atexit

@atexit.register
def goodbye():
    ActorSystem().shutdown()
    time.sleep(2)
    

class ServerRunner():

    class __ServerRunner:
        def __init__(self):
            self.actor_system = None
        


            self.component_registry = registry.Registry()
            self.container = None
            self.component_registry.register_server(self)
            #self.multi_simulation = multi_simulation
            self.container = None
            self.configuration = None
            
            # if self.multi_simulation is not True:
            #     self.configuration = self.load_mtree_config(config_file)
            # else:
            #     self.configuration = self.load_multiple_mtree_config(config_file)
            # print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))

        def __str__(self):
            return repr(self)

    instance = None
    
    def __init__(self):
        if not ServerRunner.instance:
            ServerRunner.instance = ServerRunner.__ServerRunner()
        #else:
        #    return ServerRunner.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)


    def create_actor_system(self):
        logcfg = {'version': 1,
                  'formatters': {
                      'normal': {'format': '%(levelname)-8s %(message)s'},
                      'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'},
                      "json": { "()": CustomJsonFormatter}
                      },
                  'filters': {'isActorLog': {'()': actorLogFilter},
                              'notActorLog': {'()': notActorLogFilter}},
                  'handlers': {'h1': {'class': 'logging.FileHandler',
                                      'filename': 'mtree.log',
                                      'formatter': 'normal',
                                      'filters': ['notActorLog'],
                                      'level': logging.INFO},
                               'h2': {'class': 'logging.FileHandler',
                                      'filename': 'mtree.log',
                                      'formatter': 'actor',
                                      'filters': ['isActorLog'],
                                      'level': logging.INFO},
                               'exp': {'class': 'logging.FileHandler',
                                      'filename': 'experiment.log',
                                      'formatter': 'actor',
                                      'filters': ['isActorLog'],
                                      'level': logger.EXPERIMENT},
                                "json": {
                                    "class": "logging.FileHandler",
                                    "formatter": "json",
                                    'filters': ['notActorLog'],
                                    'filename': 'experiment_data.log',
                                    'level': logger.EXPERIMENT_DATA
                                }
                               },
                  'loggers': {'': {'handlers': ['h1', 'h2', 'exp', 'json'], 'level': logging.DEBUG}}
                  }

        logcfg = { 'version': 1,
           'formatters': {
               'normal': {'format': '%(levelname)-8s %(message)s'},
               'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
           'filters': { 'isActorLog': { '()': actorLogFilter},
                        'notActorLog': { '()': notActorLogFilter}},
           'handlers': { 'h1': {'class': 'logging.StreamHandler',
                                'formatter': 'normal',
                                'filters': ['notActorLog'],
                                'level': logging.INFO},
                         'h2': {'class': 'logging.StreamHandler',
                                'formatter': 'actor',
                                'filters': ['isActorLog'],
                                'level': logging.INFO},},
           'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
         }

        #self.actor_system = ActorSystem(None, logDefs=logcfg)
        #self.actor_system = ActorSystem('multiprocQueueBase', logDefs=logcfg)
        ServerRunner.instance.actor_system = ActorSystem()
        #actorSys = self.actor_system or ActorSystem()
        try:
            ServerRunner.instance.actor_system.tell(
                ServerRunner.instance.actor_system.createActor(SimpleSourceAuthority),
                'register')
        except:
            print('***ERROR starting source authority')
            #traceback.print_exc(limit=3)

        cwd = os.getcwd()
        sys.path.append(cwd)
        mes_components = {}




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
            t = sys.modules[module_name]

            ######
            # This is the magic line... this forces the lazyloader to kick in.
            ######

            print(sys.modules[module_name])

            #######
            #sys.modules[module_name]
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

    def run_simulation(self):
        self.examine_directory()
        if self.multi_simulation is False:
            self.launch_multi_simulations()
        else:
            self.launch_multi_simulations()

    def dispatcher(self):
        actor_system = ActorSystem('multiprocQueueBase')
        self.dispatcher_address = actor_system.createActor(Dispatcher)
        #ServerRunner.instance.container.create_dispatcher()        

    def load_mtree_config(self, config_file):
        configuration = None
        with open(config_file) as json_file:
            configuration = json.load(json_file)
        return [configuration]


    def run_simple_configuration(self):
        configuration = self.load_mtree_config("/Users/Shared/repos/mTree_examples/mes_example_1/config/mes_example_1.json")
        actor_system = ActorSystem('multiprocQueueBase')
        configuration_message = Message()
        configuration_message.set_directive("simulation_configurations")
        configuration_message.set_payload(configuration)
        
        actor_system.tell(self.dispatcher_address, configuration_message)

    def shutdown(self):
        if self.container is not None:
            self.container.shutdown_thespian()

    def launch_multi_simulations(self):
        
        if ServerRunner.instance.container is None:
            ServerRunner.instance.container = SimulationContainer()
        ServerRunner.instance.container.create_dispatcher()
        tester = None
        with open("/Users/Shared/repos/mTree_examples/mes_example_1/config/mes_example_1.json","r") as tester:
            import json
            tester = json.load(tester)
        ServerRunner.instance.container.send_dispatcher_simulation_configurations(tester)

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
