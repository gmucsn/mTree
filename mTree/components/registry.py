from mTree.components.admin_message import AdminMessage
import json
import sys
import inspect


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
            print("\t", i)
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
            print(Registry.instance.class_list[target])
        
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

            print(sys.modules[module_name])

         
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
            if directive in Registry.instance.class_list[mes_class]["class"]._enabled_directives_schemas.keys():
                schema =  Registry.instance.class_list[mes_class]["class"]._enabled_directives_schemas[directive]
            directives_schemas.append((directive, schema))
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






