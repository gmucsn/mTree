import logging
from  pythonjsonlogger import jsonlogger
from datetime import datetime
import os
import glob
from zipfile import ZipFile

from thespian.actors import *

from mTree.microeconomic_system import *
# from mTree.server.websocket_router import WebsocketRouter
from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.web_socket_router_actor import WebSocketRouterActor
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.admin_message import AdminMessage
from mTree.microeconomic_system.system_status_actor import SystemStatusActor
from mTree.server.log_config import logcfg

# class actorLogFilter(logging.Filter):
#     def filter(self, logrecord):
#         return 'actorAddress' in logrecord.__dict__
# class notActorLogFilter(logging.Filter):
#     def filter(self, logrecord):
#         return 'actorAddress' not in logrecord.__dict__
# class informationLogFilter(logging.Filter):
#     def filter(self, logRecord):
#         return logRecord.levelno == 24
# class experimentLogFilter(logging.Filter):
#     def filter(self, logRecord):
#         return logRecord.levelno == 25


# class CustomJsonFormatter(jsonlogger.JsonFormatter):
#     def add_fields(self, log_record, record, message_dict):
#         super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
#         if not log_record.get('timestamp'):
#             # this doesn't use record.created, so it is slightly off
#             now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
#             log_record['timestamp'] = now
#         if log_record.get('message') is None:
#             log_record.pop('message', None)
#         # if log_record.get('level'):
#         #     log_record['level'] = log_record['level'].upper()
#         # else:
#         #     log_record['level'] = record.levelname

# #formatter = CustomJsonFormatter('(timestamp) (level) (name) (message)')



# logger = logging.getLogger("mTree")
# # set success level
# logger.EXPERIMENT_DATA = 27  # between WARNING and INFO
# logging.addLevelName(logger.EXPERIMENT_DATA, 'EXPERIMENT_DATA')

# logger.EXPERIMENT = 25  # between WARNING and INFO
# logging.addLevelName(logger.EXPERIMENT, 'EXPERIMENT')

# logger.MESSAGE = 24  # between WARNING and INFO
# logging.addLevelName(logger.MESSAGE, 'MESSAGE')
#setattr(logging, 'experiment', lambda message, *args: logger._log(logging.EXPERIMENT, message, args))


# class SimpleSourceAuthority(ActorTypeDispatcher):
#     def receiveMsg_str(self, msg, sender):
#         self.registerSourceAuthority()
#     def receiveMsg_ValidateSource(self, msg, sender):
#         self.send(sender, ValidatedSource(msg.sourceHash,
#                                           msg.sourceData,
#                                           msg.sourceInfo))



# logcfg = { 'version': 1,
#     'formatters': {
#         'normal': {'format': '%(levelname)-8s %(message)s'},
#         'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
#     'filters': { 'isActorLog': { '()': actorLogFilter},
#                 'notActorLog': { '()': notActorLogFilter}},
#     'handlers': { 'h1': {'class': 'logging.StreamHandler',
#                         'formatter': 'normal',
#                         'filters': ['notActorLog'],
#                         'level': logging.INFO},
#                     'h2': {'class': 'logging.StreamHandler',
#                         'formatter': 'actor',
#                         'filters': ['isActorLog'],
#                         'level': logging.INFO},},
#     'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
#     }

capabilities = dict([('Admin Port', 19000)])


# os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
# os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")

os.environ['THESPLOG_THRESHOLD'] =  'WARNING'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")


class ActorSystemStartup:
    def __init__(self, websocket=False):
        self.websocket = websocket
        self.actor_system = None

        self.system_status_actor_address = None
        self.dispatcher_address = None

        self.capabilities = dict([('Admin Port', 19000)])
        
        ####
        # !!! Should be initial startup of Thespian System !!!
        ####
        # self.actor_system = ActorSystem('multiprocTCPBase', capabilities=self.capabilities, logDefs=logcfg)
        self.actor_system = ActorSystem('multiprocTCPBase', logDefs=logcfg)

        logging.info('Checking System Status...')
        if not self.existing_system():
            logging.info('Starting Up Full System')
            self.startup()

    def existing_system(self):
        # self.sa = ActorSystem('multiprocTCPBase', capabilities=capabilities).createActor(SimpleSourceAuthority)
        # self.actor_system.tell(self.sa, True)
        status_actor = self.actor_system.createActor(SystemStatusActor, globalName = "SystemStatusActor")
        self.system_status_actor_address = status_actor

        logging.info("STATUS ACTOR STARTING... ")
        self.actor_system.tell(self.system_status_actor_address, "system_status_actor_initialization")
        
        # message = AdminMessage(request="start_source_authority")
        # self.actor_system.tell(status_actor, message)
       
        message = AdminMessage(request="system_running")
        system_status = self.actor_system.ask(status_actor, message)

            
        return system_status

    def startup(self):
        #status_actor = self.actor_system.createActor(Actor, globalName = "SystemStatusActor")
        
        logging.info("STATUS ACTOR STARTING... ")
        dispatcher = self.actor_system.createActor(Dispatcher, globalName = "Dispatcher")
        self.actor_system.tell(dispatcher, "dipatcher_initialization_message")
        
        
        start_message = Message()
        start_message.set_sender("system")
        start_message.set_directive("register_dispatcher")
        self.actor_system.tell(dispatcher, start_message)


        if self.websocket:
            # try the websocket actor
            web_socket_router_actor = self.actor_system.createActor(WebSocketRouterActor, globalName = "WebSocketRouterActor")
            self.actor_system.tell(web_socket_router_actor, "web_socket_router_initializing")
            print("Websocket actor address: " + str(web_socket_router_actor))

            #self.websocket_router = WebsocketRouter()

            # start_message = Message()
            # start_message.set_sender("websocketrouter")
            # start_message.set_directive("register_websocket_router")
            
            #self.actor_system.tell(dispatcher, start_message)
            # self.actor_system.tell(web_socket_router_actor, start_message)


    def load_base_mes(self):
        #script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "microeconomic_system")
        #script_dir = os.path.join(mes_base_dir, "mes")
        script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "microeconomic_system")
        
        #plugins_directory_path = os.path.join(os.getcwd(), 'mes')
        #print("\t plugin path: ", plugins_directory_path)
        plugin_file_paths = glob.glob(os.path.join(script_dir, "*.py"))
        #print(plugin_file_paths)
        base_components = []
        for plugin_file_path in plugin_file_paths:
            plugin_file_name = os.path.basename(plugin_file_path)
            module_name = os.path.splitext(plugin_file_name)[0]
            if module_name.startswith("__"):
                continue
            base_components.append([plugin_file_path, plugin_file_name])

    

    @staticmethod
    def shutdown():
        print('Shutting down actor system....')
        capabilities = dict([('Admin Port', 19000)])

        ActorSystem('multiprocTCPBase', capabilities).shutdown()