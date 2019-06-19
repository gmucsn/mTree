from mTree.components.admin_message import AdminMessage
import json
import sys

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
        Registry.instance.class_list[class_name] = {"class": classobject}
        for base_class in classobject.__bases__:
            if base_class.__name__ == "Agent":
                Registry.instance.agent_list.append(class_name)
            elif base_class.__name__ == "Institution":
                Registry.instance.institution_list.append(class_name)
            elif base_class.__name__ == "Environment":
                Registry.instance.environment_list.append(class_name)

    def get_component_source_file(self, mes_class):
        classobject = Registry.instance.class_list[mes_class]["class"]
        filename = sys.modules[classobject.__module__].__file__
        contents = None
        with open(filename) as f:
            contents = f.read()
        return contents

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






