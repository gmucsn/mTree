from thespian.actors import *
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
from mTree.components import registry

class SimulationContainer():
    def __init__(self):
        self.actor_system = None
        self.dispatcher = None

        self.create_actor_system()


    def create_actor_system(self):
        self.actor_system = ActorSystem(None, logDefs=logcfg)

    def create_dispatcher(self):
        self.dispatcher = self.actor_system.createActor(Dispatcher)


    def send_dispatcher_simulation_configurations(self, configurations):
        configuration_message = Message()
        configuration_message.set_directive("simulation_configurations")
        configuration_message.set_payload(configurations)
        self.actor_system.tell(self.dispatcher, configuration_message)

    def send_root_environment_message(self, environment_name, message):
        self.actor_system.tell(self.environments[environment_name], message)

    def kill_environment(self, environment_name):
        self.send(self.dispatcher, ActorExitRequest())


if __name__ == "__main__":  # This is what should be moved to the mTree level...
    container = SimulationContainer()
    container.create_actor_system()

