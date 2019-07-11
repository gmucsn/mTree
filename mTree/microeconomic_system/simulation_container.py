from thespian.actors import *
#from thespian.system.multiprocQueueBase import
import logging
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
from mTree.components import registry

class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__
class informationLogFilter(logging.Filter):
    def filter(self, logRecord):
        return logRecord.levelno == 24
class experimentLogFilter(logging.Filter):
    def filter(self, logRecord):
        return logRecord.levelno == 25


logger = logging.getLogger("mTree")
# set success level
logger.EXPERIMENT = 25  # between WARNING and INFO
logging.addLevelName(logger.EXPERIMENT, 'EXPERIMENT')
logger.MESSAGE = 24  # between WARNING and INFO
logging.addLevelName(logger.MESSAGE, 'MESSAGE')
#setattr(logging, 'experiment', lambda message, *args: logger._log(logging.EXPERIMENT, message, args))




class SimulationContainer():
    def __init__(self):
        self.actor_system = None
        self.dispatcher = None

        self.create_actor_system()


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
                                      'level': logging.INFO},
                               'exp': {'class': 'logging.FileHandler',
                                      'filename': 'experiment.log',
                                      'formatter': 'actor',
                                      'filters': ['isActorLog'],
                                      'level': logger.EXPERIMENT},
                               },
                  'loggers': {'': {'handlers': ['h1', 'h2', 'exp'], 'level': logging.DEBUG}}
                  }

        self.actor_system = ActorSystem(None, logDefs=logcfg)
        #self.actor_system = ActorSystem('multiprocQueueBase', logDefs=logcfg)

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

