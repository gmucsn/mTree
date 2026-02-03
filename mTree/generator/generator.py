import os
from pathlib import Path

import pkg_resources
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic.types import constr
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text


class ProjectTemplate(BaseModel):
    project_name: str = Field(min_length=1)
    agent_name: str = Field(min_length=1)
    institution_name: str = Field(min_length=1)
    environment_name: str = Field(min_length=1)


class Generate(object):
    def __init__(self):
        self.console = Console()

        self.project_template = None
        if self.ask_project_questions():
            if self.construct_directory():
                self.copy_agent_template()
                self.copy_environment_template()
                self.copy_institution_template()
                self.create_basic_configuration()

    def ask_project_questions(self):
        project_name = Prompt.ask("Enter a project name")
        agent_name = Prompt.ask("Enter an agent name")
        institution_name = Prompt.ask("Enter an institution name")
        environment_name = Prompt.ask("Enter an environment name")
        try:
            self.project_template = ProjectTemplate(
                project_name=project_name,
                agent_name=agent_name,
                institution_name=institution_name,
                environment_name=environment_name,
            )
            return True
        except ValidationError as e:
            text = Text()
            text.append(
                "There are errors with your project information\n", style="bold red"
            )

            for error in e.errors():
                text.append(f"\tField: {error['loc'][0]} {error['msg']}\n")
            self.console.print(text)

    def construct_directory(self):
        self.project_directory = Path.cwd() / self.project_template.project_name

        text = Text()
        text.append(
            f"Attempting to create new project directory: {self.project_directory}\n",
            style="bold green",
        )
        self.console.print(text)

        if not self.project_directory.exists():
            self.project_directory.mkdir()
            self.config_directory = self.project_directory / "config"
            self.mes_directory = self.project_directory / "mes"
            self.config_directory.mkdir()
            self.mes_directory.mkdir()
            text = Text()
            text.append(
                f"\tThe project directory has been created: {self.project_directory}\n",
                style="bold green",
            )

            return True
        else:
            text = Text()
            text.append(
                f"The target directory already exists: {self.project_directory}\n",
                style="bold red",
            )
            self.console.print(text)

    def copy_agent_template(self):
        path = "templates/agent_template.py"
        f = pkg_resources.resource_stream(__name__, path)
        self.agent_name = self.project_template.agent_name + "_agent.py"
        self.agent_class_name = self.project_template.agent_name.title() + "Agent"
        template = f.read().decode("utf-8")
        template = template.replace("NAME", self.agent_class_name)
        with open(self.mes_directory / self.agent_name, "w") as fileout:
            fileout.write(template)

    def copy_institution_template(self):
        path = "templates/institution_template.py"
        f = pkg_resources.resource_stream(__name__, path)
        self.institution_name = (
            self.project_template.institution_name + "_institution.py"
        )
        self.institution_class_name = (
            self.project_template.institution_name.title() + "Institution"
        )
        template = f.read().decode("utf-8")
        template = template.replace("NAME", self.institution_class_name)
        with open(self.mes_directory / self.institution_name, "w") as fileout:
            fileout.write(template)

    def copy_environment_template(self):
        path = "templates/environment_template.py"
        f = pkg_resources.resource_stream(__name__, path)
        self.environment_name = (
            self.project_template.environment_name + "_environment.py"
        )
        self.environment_class_name = (
            self.project_template.environment_name.title() + "Environment"
        )
        template = f.read().decode("utf-8")
        template = template.replace("NAME", self.environment_class_name)
        with open(self.mes_directory / self.environment_name, "w") as fileout:
            fileout.write(template)

    def create_basic_configuration(self):
        path = "templates/basic_simulation_template.json"
        f = pkg_resources.resource_stream(__name__, path)
        template = f.read().decode("utf-8")
        template = template.replace("AGENTNAME", self.agent_class_name)
        template = template.replace("INSTITUTIONNAME", self.institution_class_name)
        template = template.replace("ENVIRONMENTNAME", self.environment_class_name)
        with open(self.config_directory / "basic_simulation.json", "w") as fileout:
            fileout.write(template)
