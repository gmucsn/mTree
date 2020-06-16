import os
import pkg_resources

class Generate(object):
    def __init__(self):
        pass

    def construct_directory(self, project_name):
        print("Creating mTree project directory")
        if not os.path.exists(project_name):
            os.makedirs(project_name)
            os.makedirs(os.path.join(project_name, "config"))
            os.makedirs(os.path.join(project_name, "mes"))

    
    def copy_agent_template(self, project_name):
        path = 'templates/agent.py'
        f = pkg_resources.resource_stream(__name__, path)
        environment_name = "agent.py"
        with open(os.path.join(project_name, "mes/", environment_name), 'wb') as fileout:
            for line in f:
                fileout.write(line)

    def copy_institution_template(self, project_name):
        path = 'templates/institution.py'
        f = pkg_resources.resource_stream(__name__, path)
        environment_name = "institution.py"
        with open(os.path.join(project_name, "mes/", environment_name), 'wb') as fileout:
            for line in f:
                fileout.write(line)

    def copy_environment_template(self, project_name):
        path = 'templates/environment.py'
        f = pkg_resources.resource_stream(__name__, path)
        environment_name = "environment.py"
        with open(os.path.join(project_name, "mes/", environment_name), 'wb') as fileout:
            for line in f:
                fileout.write(line)
        
    def create_basic_configuration(self, project_name):
        path = 'templates/basic_simulation.json'
        f = pkg_resources.resource_stream(__name__, path)
        environment_name = "basic_simulation.json"
        with open(os.path.join(project_name, "config/", environment_name), 'wb') as fileout:
            for line in f:
                fileout.write(line)

    def build_project(self, project_name):
        self.construct_directory(project_name)
        self.copy_agent_template(project_name)
        self.copy_institution_template(project_name)
        self.copy_environment_template(project_name)
        self.create_basic_configuration(project_name)

