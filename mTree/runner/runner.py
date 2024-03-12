import sys, getopt
import json
import importlib
import inspect
import os
import glob

import importlib.util
import sys
import time

from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.container import Container
from mTree.microeconomic_system.simulation_container import SimulationContainer
from thespian.actors import *
from mTree.components import registry
from mTree.server.actor_system_connector import ActorSystemConnector
from mTree.simulation.mes_simulation_library import MESSimulationLibrary

from simple_term_menu import TerminalMenu
from terminaltables import AsciiTable

from cmd import Cmd

import atexit
from thespian.actors import *


capabilities = dict([('Admin Port', 19000)])

@atexit.register
def goodbye():
    capabilities = dict([('Admin Port', 19000)])
    actors = ActorSystem('multiprocTCPBase') #, capabilities)
    actors.shutdown()
    time.sleep(2)
    #print("You are now leaving mTree Runner.")

class MTreePrompt(Cmd):
    def __init__(self, runner):
        self.runner = runner
        Cmd.__init__(self)
        
    def emptyline(self): pass  # do nothing

    def do_run_simulation(self, args):
        """Runs the loaded simulation."""
        #self.runner.run_simulation()
        self.runner.show_configuration_menu()

    def do_check_status(self, args):
        """Check the status object in mTree to see what is running."""
        self.runner.check_status()

    def do_force_shutdown(self, args):
        """Forces an exit on all MES components"""
        print("Forcing system shutdown")
        capabilities = dict([('Admin Port', 19000)])
        actors = ActorSystem('multiprocTCPBase', capabilities)
        actors.shutdown()

    def do_kill_run(self, run_id):
        """Force a running MES to shutdown"""
        self.runner.kill_run_by_id(run_id)




    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print( "Hello, %s" % name)

    


    def do_quit(self, args):
        """Quits the program."""
        self.runner.shutdown()
        print("Quitting.")  
        
        raise SystemExit




class Runner():
    def __init__(self, running_directory): #, multi_simulation=False):
        self.container = None
        self.running_directory = running_directory
        self.config_directory = os.path.join(running_directory, "config")
        if not os.path.isdir(self.config_directory):
            print("!!! Config directory doesn't exist !!!")
            print("!!! Make sure you are running inside an MES !!!")
            exit()
            
        # self.component_registry = registry.Registry()
        
        # self.component_registry.register_server(self)
        # self.multi_simulation = multi_simulation
        # self.container = None
        #self.configuration = config_file
        # if self.multi_simulation is not True:
        #     self.configuration = self.load_mtree_config(config_file)
        # else:
        #     self.configuration = self.load_multiple_mtree_config(config_file)
        #print("Current Configuration: ", json.dumps(self.configuration, indent=4, sort_keys=True))
        self.actor_system = ActorSystemConnector()
    


    def show_configuration_menu(self):
        config_files = [file for file in os.listdir(self.config_directory) if file.endswith('.json')]

        terminal_menu = TerminalMenu(
            config_files,
            multi_select=True,
            show_multi_select_hint=True,
        )
        menu_entry_indices = terminal_menu.show()

        if len(menu_entry_indices) == 0:
            print("Make sure to select a configuration")

        selected_configs = [config_files[selected] for selected in menu_entry_indices]

        self.run_simulation_from_configurations(selected_configs)


    def run_simulation_from_configurations(self, configurations):
        for configuration in configurations:
            working_dir = os.getcwd()
            #actor_system.send_message()
            configuration_good = True
            try:
                simulation_library = MESSimulationLibrary()
                simulation_library.list_simulation_files_directory(working_dir)
                simulation = simulation_library.get_simulation_by_filename(os.path.basename(configuration))
            except Exception as e:
                print("EXCEPTION LOADING CONFIGURATIONS!")
                print(e)
                configuration_good = False    
                
            if configuration_good:
                actor_system = ActorSystemConnector()
                working_dir = os.getcwd()
                #actor_system.send_message()
                print("===> Starting to run: ", configuration)
                actor_system.run_simulation(working_dir, configuration, simulation["description"].to_hash())

                # self.examine_directory()
                # if self.multi_simulation is False:
                #     self.launch_multi_simulations()
                # else:
                #     self.launch_multi_simulations()

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
        
        ### updare for MES/mes naming
        ### create errors here
        
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

            #print(sys.modules[module_name])

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
        working_dir = os.getcwd()
        #actor_system.send_message()
        simulation_library = MESSimulationLibrary()
        simulation_library.list_simulation_files_directory(working_dir)
        
        simulation = simulation_library.get_simulation_by_filename(os.path.basename(self.configuration))
        actor_system = ActorSystemConnector()
        working_dir = os.getcwd()
        #actor_system.send_message()
        actor_system.run_simulation(working_dir, simulation["description"].to_hash())

        # self.examine_directory()
        # if self.multi_simulation is False:
        #     self.launch_multi_simulations()
        # else:
        #     self.launch_multi_simulations()

    def check_status(self):
        table_data = [
            ['Run Code', 'Configuration', 'Run Number', 'Status', 'Total Time'],
        ]
        actor_system = ActorSystemConnector()
        statuses = actor_system.get_status()
        print("STATUS REPORTING")
        print(statuses)
        if statuses is None:
            table_data.append(["No Simulations Runnings"])
        else:
            table_data.extend(statuses)
        table = AsciiTable(table_data)
        print(table.table)

    def kill_run_by_id(self, run_id):
        actor_system = ActorSystemConnector()
        actor_system.kill_run_by_id(run_id)
        print("Kill command sent")


    def runner(self):
        prompt = MTreePrompt(self)
        prompt.prompt = 'mTree> '
        prompt.cmdloop('Starting prompt...')

        #self.examine_directory()
        #if self.multi_simulation is False:
        #    self.launch_multi_simulations()
        #else:
        #    self.launch_multi_simulations()

    def shutdown(self):
        if self.container is not None:
            self.container.shutdown_thespian()

    def launch_multi_simulations(self):
        if self.container is None:
            self.container = SimulationContainer()
        self.container.create_dispatcher()
        self.container.send_dispatcher_simulation_configurations(self.configuration)

    def launch_simulation(self):
        """ DEPRECATED """
        
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
