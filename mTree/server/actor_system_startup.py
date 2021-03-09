import logging
import pythonjsonlogger
from thespian.actors import *
from mTree.microeconomic_system import *
from mTree.microeconomic_system.dispatcher import Dispatcher


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

#formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')



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

capabilities = dict([('Admin Port', 1900)])

import os
import glob
from zipfile import ZipFile
from thespian.actors import *
from mTree.microeconomic_system import *


class SimpleSourceAuthority(Actor):
    def receiveMessage(self, msg, sender):
        if msg is True:
            self.registerSourceAuthority()
        if isinstance(msg, ValidateSource):
            self.send(sender,
                      ValidatedSource(msg.sourceHash,
                                      msg.sourceData,
                                      # Thespian pre 3.2.0 has no sourceInfo
                                      getattr(msg, 'sourceInfo', None)))


class ActorSystemStartup:
    def __init__(self):
        self.actor_system = None
        print("ACTOR SYSTEM STARTING")
        self.actor_system = ActorSystem('multiprocTCPBase', capabilities)
        self.sa = self.actor_system.createActor(SimpleSourceAuthority)
        self.actor_system.tell(self.sa, True)
        self.load_base_mes()

    def load_base_mes(self):
        script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "microeconomic_system")
        print(script_dir)
        #plugins_directory_path = os.path.join(os.getcwd(), 'mes')
        #print("\t plugin path: ", plugins_directory_path)
        plugin_file_paths = glob.glob(os.path.join(script_dir, "*.py"))
        base_components = []
        for plugin_file_path in plugin_file_paths:
            print("\t\t !--> ", plugin_file_path)
            plugin_file_name = os.path.basename(plugin_file_path)
            module_name = os.path.splitext(plugin_file_name)[0]
            if module_name.startswith("__"):
                continue
            print("PLUGIN SHOULD LOAD...", plugin_file_path)
            base_components.append([plugin_file_path, plugin_file_name])

        with ZipFile('temp_components.zip', 'w') as zipObj2:
            for component in base_components:
                zipObj2.write(component[0],arcname=component[1])

        asys = ActorSystem('multiprocTCPBase', capabilities)
        source_hash = asys.loadActorSource('temp_components.zip')
        asys.createActor("live_dispatcher.LiveDispatcher",sourceHash=source_hash, globalName="dispatcher")

        #                    
        
    @staticmethod
    def shutdown():
        print('Shutting down actor system....')
        ActorSystem('multiprocTCPBase', capabilities).shutdown()