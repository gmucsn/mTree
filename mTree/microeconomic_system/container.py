from thespian.actors import *
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
import atexit


class Container:
    def __init__(self):
        self.environment = None
        self.actor_system = None
        self.root_environment = None

        self.create_actor_system()
        atexit.register(self.actor_system_cleanup)

    def create_actor_system(self):
        logcfg = {'version': 1,  # (ref:logdef)
                  'formatters': {
                      'normal': {
                          'format': '%(levelname)-8s %(message)s'}},
                  'handlers': {
                      'h': {'class': 'logging.FileHandler',
                            'filename': 'hello.log',
                            'formatter': 'normal',
                            'level': logging.INFO}},
                  'loggers': {
                      '': {'handlers': ['h'], 'level': logging.DEBUG}}
                  }

        print("CREATING ACTOR SYSteMS")
        self.actor_system = ActorSystem("multiprocTCPBase", logDefs=logcfg)

    def actor_system_cleanup(self):
        print("EXPERIMENT SHUTTING DOWN")
        self.actor_system.shutdown()
        print("ACTOR SYSTEM SHOULD HAVE SHUTDOWN")


    def create_root_environment(self, environment_class):
        self.environment = self.actor_system.createActor(environment_class)

    def setup_environment_agents(self, agent_class, num_agents = 1):
        logging.info("AGENTS BEING SETUP FROM ENV")
        message = Message()
        message.set_directive("setup_agents")
        message.set_payload({"agent_class": agent_class, "num_agents": num_agents})
        self.actor_system.tell(self.environment, message)

    def setup_environment_institution(self, institution_class):
        message = Message()
        message.set_directive("setup_institution")
        message.set_payload({"institution_class": institution_class})
        self.actor_system.tell(self.environment, message)

    def send_root_environment_message(self, message):
        self.actor_system.tell(self.environment, message)


if __name__ == "__main__":  # This is what should be moved to the mTree level...
    container = Container()
    container.create_actor_system()

