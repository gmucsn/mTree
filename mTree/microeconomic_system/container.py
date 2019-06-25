from thespian.actors import *
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
import atexit


class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__


class Container:
    def __init__(self):
        self.environment = None
        self.actor_system = None
        self.root_environment = None

        self.create_actor_system()
        atexit.register(self.actor_system_cleanup)

    def create_actor_system(self):
        logcfg = {'version': 1,
                  'formatters': {
                      'normal': {'format': '%(levelname)-8s %(message)s'},
                      'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
                  'filters': {'isActorLog': {'()': actorLogFilter},
                              'notActorLog': {'()': notActorLogFilter}},
                  'handlers': {'h1': {'class': 'logging.FileHandler',
                                      'filename': 'mtree.log',
                                      'formatter': 'normal',
                                      'filters': ['notActorLog'],
                                      'level': logging.INFO},
                               'h2': {'class': 'logging.FileHandler',
                                      'filename': 'mtree.log',
                                      'formatter': 'actor',
                                      'filters': ['isActorLog'],
                                      'level': logging.INFO}, },
                  'loggers': {'': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
                  }

        print("CREATING ACTOR SYSteMS")
        #self.actor_system = ActorSystem("multiprocQueueBase", logDefs=logcfg)
        print("Actor system Started")
        self.actor_system = ActorSystem(None, logDefs=logcfg)

    def actor_system_cleanup(self):
        print("EXPERIMENT SHUTTING DOWN")
        self.actor_system.shutdown()
        print("ACTOR SYSTEM SHOULD HAVE SHUTDOWN")


    def create_root_environment(self, environment_class):
        print("CREATING AN ENVIRONMENT")
        self.environment = self.actor_system.createActor(environment_class)
        print(self.environment)

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

