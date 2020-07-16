from thespian.actors import *
#from thespian.system.multiprocQueueBase import
import logging
import pythonjsonlogger
from mTree.microeconomic_system.logging import logcfg
from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
import sys
from datetime import timedelta
from mTree.components import registry
import os
import glob
import time
import traceback

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

from  pythonjsonlogger import jsonlogger
from datetime import datetime

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('message') is None:
            log_record.pop('message', None)
        # if log_record.get('level'):
        #     log_record['level'] = log_record['level'].upper()
        # else:
        #     log_record['level'] = record.levelname

formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')



logger = logging.getLogger("mTree")
# set success level
logger.EXPERIMENT_DATA = 27  # between WARNING and INFO
logging.addLevelName(logger.EXPERIMENT_DATA, 'EXPERIMENT_DATA')

logger.EXPERIMENT = 25  # between WARNING and INFO
logging.addLevelName(logger.EXPERIMENT, 'EXPERIMENT')

logger.MESSAGE = 24  # between WARNING and INFO
logging.addLevelName(logger.MESSAGE, 'MESSAGE')
#setattr(logging, 'experiment', lambda message, *args: logger._log(logging.EXPERIMENT, message, args))


class SimpleSourceAuthority(ActorTypeDispatcher):
    def receiveMsg_str(self, msg, sender):
        self.registerSourceAuthority()
    def receiveMsg_ValidateSource(self, msg, sender):
        self.send(sender, ValidatedSource(msg.sourceHash,
                                          msg.sourceData,
                                          msg.sourceInfo))


class SimulationContainer():
    def __init__(self):
        self.actor_system = None
        self.dispatcher = None
        self.log_actor = None

        self.create_actor_system()


    def zip_source(self, filename):
        zipname = 'mes.zip'
        import zipfile
        zf = zipfile.ZipFile(zipname, 'w')
        
        zf.writestr('mes.py', open(filename, 'r').read())
        zf.close()
        return zipname

    def create_actor_system(self):
        logcfg = {'version': 1,
                  'formatters': {
                      'normal': {'format': '%(levelname)-8s %(message)s'},
                      'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'},
                      "json": { "()": CustomJsonFormatter}
                      },
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
                                "json": {
                                    "class": "logging.FileHandler",
                                    "formatter": "json",
                                    'filters': ['notActorLog'],
                                    'filename': 'experiment_data.log',
                                    'level': logger.EXPERIMENT_DATA
                                }
                               },
                  'loggers': {'': {'handlers': ['h1', 'h2', 'exp', 'json'], 'level': logging.DEBUG}}
                  }

        logcfg = { 'version': 1,
           'formatters': {
               'normal': {'format': '%(levelname)-8s %(message)s'},
               'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
           'filters': { 'isActorLog': { '()': actorLogFilter},
                        'notActorLog': { '()': notActorLogFilter}},
           'handlers': { 'h1': {'class': 'logging.StreamHandler',
                                'formatter': 'normal',
                                'filters': ['notActorLog'],
                                'level': logging.INFO},
                         'h2': {'class': 'logging.StreamHandler',
                                'formatter': 'actor',
                                'filters': ['isActorLog'],
                                'level': logging.INFO},},
           'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
         }

        #self.actor_system = ActorSystem(None, logDefs=logcfg)
        #self.actor_system = ActorSystem('multiprocQueueBase', logDefs=logcfg)
        self.actor_system = ActorSystem('multiprocTCPBase',logDefs=logcfg)
        actorSys = self.actor_system or ActorSystem()
        try:
            actorSys.tell(
                actorSys.createActor(SimpleSourceAuthority),
                'register')
        except:
            print('***ERROR starting source authority')
            traceback.print_exc(limit=3)

        cwd = os.getcwd()
        sys.path.append(cwd)
        for filename in glob.iglob(os.path.join(cwd, 'mes', '*.py'), recursive=True):
            print("ADDING TO ZIP: ",filename)
            loadHash = self.actor_system.loadActorSource(self.zip_source(filename))
            time.sleep(1) # Allow source authority to authorize the load
            try:
                na = actorSys.createActor('mes.BasicEnvironment', sourceHash = loadHash)
            except:
                print ('***ERROR creating Actor t.TestActor from sourceHash %s'%(loadHash))
                traceback.print_exc(limit=3)
            else:
                N,A = self.getOrAddAddress(na)
                print ('Created new TestActor %d @ %s'%(N, str(A)))

    def create_dispatcher(self):
        try:
            self.dispatcher = ActorSystem().createActor(Dispatcher)
        except Exception as e:
            self.dispatcher = ActorSystem().createActor("Dispatcher")


    def send_dispatcher_simulation_configurations(self, configurations):
        for configuration in configurations:
            print("CREATING DISPATCHER FOR CONFIGURATION")
            
            configuration_message = Message()
            configuration_message.set_directive("simulation_configurations")
            configuration_message.set_payload(configuration)
            ActorSystem().tell(self.dispatcher, configuration_message)

    # def send_dispatcher_simulation_configurations(self, configurations):
    #     configuration_message = Message()
    #     configuration_message.set_directive("simulation_configurations")
    #     configuration_message.set_payload(configurations)
    #     self.actor_system.tell(self.dispatcher, configuration_message)



    def send_root_environment_message(self, environment_name, message):
        ActorSystem().tell(self.environments[environment_name], message)

    def shutdown_thespian(self):
        ActorSystem().shutdown()

    def kill_environment(self, environment_name):
        #self.send(self.dispatcher, ActorExitRequest())
        pass


if __name__ == "__main__":  # This is what should be moved to the mTree level...
    container = SimulationContainer()
    container.create_actor_system()

