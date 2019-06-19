from thespian.actors import *
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta

class MultiContainer():
    def __init__(self):
        self.environments = {}
        self.actor_system = None
        self.root_environment = None

        self.create_actor_system()


    def create_actor_system(self):
        self.actor_system = ActorSystem(None, logDefs=logcfg)

    def create_environment(self, environment_class, environment_name):
        self.environments[environment_name] = self.actor_system.createActor(environment_class)

    def setup_environment_agents(self, environment_name, agent_class, num_agents = 1):
        message = Message()
        message.set_directive("setup_agents")
        message.set_payload({"agent_class": agent_class, "num_agents": num_agents})
        self.actor_system.tell(self.environments[environment_name], message)

    def setup_environment_institution(self, environment_name, institution_class):
        message = Message()
        message.set_directive("setup_institution")
        message.set_payload({"institution_class": institution_class})
        self.actor_system.tell(self.environments[environment_name], message)

    def send_root_environment_message(self, environment_name, message):
        self.actor_system.tell(self.environments[environment_name], message)

    def kill_environment(self, environment_name):
        self.send(self.environments[environment_name], ActorExitRequest())


if __name__ == "__main__":  # This is what should be moved to the mTree level...
    container = MultiContainer()
    container.create_actor_system()

