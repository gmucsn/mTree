import os
import glob
from zipfile import ZipFile
from thespian.actors import *
from mTree.microeconomic_system import *

capabilities = dict([('Admin Port', 1900)])


class ComponentRegistration:
    def __init__(self, component_name, component_src, source_hash):
        self.component_name = component_name
        self.component_src = component_src
        self.source_hash = source_hash


        


class ComponentRegistrar:
    class __ComponentRegistrar:
        def __init__(self):
            self.components = {}
            self.component_files = []
            self.source_hash = None
            
        

    instance = None
        
    def __init__(self):
        if not ComponentRegistrar.instance:
            ComponentRegistrar.instance = ComponentRegistrar.__ComponentRegistrar()
        self.load_components()

    def get_source_hash(self):
        return ComponentRegistrar.instance.source_hash

    def find_component(self, component_name):
        pass

    def load_components(self):
        print("TRYING TO LOAD COMPONENTS INTO SYSTEM")
        #script_dir = os.path.dirname(os.path.abspath(__file__))
        plugins_directory_path = os.path.join(os.getcwd(), 'mes')
        print("\t plugin path: ", plugins_directory_path)
        plugin_file_paths = glob.glob(os.path.join(plugins_directory_path, "*.py"))
        for plugin_file_path in plugin_file_paths:
            print("\t\t !--> ", plugin_file_path)
            plugin_file_name = os.path.basename(plugin_file_path)
            module_name = os.path.splitext(plugin_file_name)[0]
            if module_name.startswith("__"):
                continue
            print("PLUGIN SHOULD LOAD...", plugin_file_path)
            ComponentRegistrar.instance.component_files.append([plugin_file_path, plugin_file_name])

        with ZipFile('temp_components.zip', 'w') as zipObj2:
            for component in ComponentRegistrar.instance.component_files:
                zipObj2.write(component[0],arcname=component[1])

        asys = ActorSystem('multiprocTCPBase', capabilities)
        source_hash = asys.loadActorSource('temp_components.zip')
        ComponentRegistrar.instance.source_hash = source_hash
        for component in ComponentRegistrar.instance.component_files:
            ComponentRegistrar.instance.components[component[1]] = ComponentRegistration(component[1], component[0], source_hash)
        # app = asys.createActor('basic_environment.BasicEnvironment',
        #                    sourceHash=source_hash)
        # asys.tell(app, "test")
        #r = asys.ask(app, sys.stdin.read().strip(), timedelta(seconds=1))