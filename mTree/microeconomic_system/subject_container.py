from thespian.actors import *
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta

class SubjectContainer():

    __instance = None

    class __SubjectContainer:
        def __init__(self):
            self.actor_system = None
            self.create_actor_system()

            self.root_environment = None
            self.environments = {}

        def create_actor_system(self):
            self.actor_system = ActorSystem(None, logDefs=logcfg)

        def create_environment(self, environment_class, environment_name):
            environment_address = self.actor_system.createActor(environment_class)
            self.environments[environment_name] = environment_address
            return environment_address

        def setup_environment_agents(self, environment_name, agent_class, num_agents=1):
            message = Message()
            message.set_directive("setup_agents")
            message.set_payload({"agent_class": agent_class, "num_agents": num_agents})
            self.actor_system.tell(self.environments[environment_name], message)

        def setup_environment_institution(self, environment_address, institution_class):
            message = Message()
            message.set_directive("setup_institution")
            message.set_payload({"institution_class": institution_class})
            self.actor_system.tell(self.environments[environment_name], message)

        def send_root_environment_message(self, environment_name, message):
            self.actor_system.tell(self.environments[environment_name], message)

        def kill_environment(self, environment_name):
            self.send(self.environments[environment_name], ActorExitRequest())

        def kill_subject_environment(self, environment_address):
            self.actor_system.tell(environment_address, ActorExitRequest())

    def __new__(self):
        if SubjectContainer.__instance is None:
            SubjectContainer.__instance = SubjectContainer.__SubjectContainer()
        return SubjectContainer.__instance


