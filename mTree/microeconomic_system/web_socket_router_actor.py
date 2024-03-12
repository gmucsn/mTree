from numpy import broadcast
from thespian import *
from thespian.actors import *
from thespian.system.messages.status import *
import time
import socketio
import logging
from mTree.microeconomic_system.dispatcher import Dispatcher
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.admin_message import AdminMessage
import json
from thespian.initmsgs import initializing_messages
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# class Wrapper_class():
#         sio = socketio.AsyncClient()

#         def __init__(self, actor_system):
#             self.actor_system = actor_system
            
#         async def setup(self):
#             self.call_backs()
#             # await self.sio.connect('http://localhost:5000', wait_timeout = 10)
#             await self.sio.connect('http://127.0.0.1:5000', wait_timeout=10, namespaces=['/developer'])

#         def loop(self): 
#             self.sio.wait()

#         def call_backs(self):
#             @self.sio.event
#             def connect():
#                 #self.sio.emit('get_system_status','admin', namespace="/admin")
#                 print('connection established')
                
#             @self.sio.on("docs")
#             def raw_data(data):
#                 print(f"Data Received {data}")


#             @self.sio.event
#             def auth(data):
#                 print(f"Data Received {data}")


#             @self.sio.event
#             def disconnect():
#                 print('disconnected from server')

#         def run(self):
#             asyncio.run(self.setup())
            
#             # self.loop()

import setproctitle


@initializing_messages([('starting', str)], initdone='init_done')
class WebSocketRouterActor(Actor):

    def logout(self):
        logging.info('WEBSOCKET THING AHPPEJd actor')
        

    def websocket_connect(self):
        try:
            self.sio = socketio.Client(reconnection=True)
            self.sio.connect('http://localhost:5000', namespaces='/developer', wait=True, wait_timeout=10)
        except:
            self.sio = None
        logging.info("Socket Status: " + str(self.sio))  

    def init_done(self):
        setproctitle.setproctitle("mTree - WebSocketRouterActor")

        # self.sio = None
        # self.websocket_connect()
        logging.info('Cliesssnt started')

    # def __init__(self) -> None:
    #     # self.sio.on("message", handler=self.logout, namespace="/developer")
    #     #self.call_backs()
    #     logging.info('Starting web actor')
    #     # self.sio = socketio.Client()
    #     # self.sio = socketio.Client()
    #     # #self.sio.connect('http://localhost:5000')
    #     # self.sio.connect('http://localhost:5000', namespaces='/developer', wait=False)
        
    #     #self.sio = socketsio.AsyncClient()
    #     logging.info('Cliesssnt started')
        
    #     # # print("ALKJFLASKJF")
    #     # #@self.sio.event
    #     # @self.sio.on('get_system_status', namespace='/developer')
    #     # def message(data):
    #     #     # dispatcher = self.createActor(Dispatcher, globalName = "Dispatcher")
    #     #     # configuration_message = Message()
    #     #     # configuration_message.set_directive("check_status")
    #     #     # response = self.send(dispatcher, configuration_message)
    #     #     logging.info('ACTOR RECIEVED **WEBSOCKET** MESSAGE')

    #     #     # return response

    #     # @self.sio.event
    #     # def connect():
    #     #     logging.info('connection established')

    #     # @self.sio.event
    #     # def my_message(data):
    #     #     print('message received with ', data)
    #     #     self.sio.emit('my response', {'response': 'my response'})
    #     #     logging.info('received from server')
    #     #     self.handle(data)
            
    #     #     logging.info("stuff configured")
    #     #     # @self.sio.on('my message')
    #     #     # def on_message(data):
    #     #     #     print('I received a message!')

    def call_backs(self):
        @self.sio.event
        def connect():
            #self.sio.emit('get_system_status','admin', namespace="/admin")
            print('connection established')
            logging.info('websocket CONNECNET')

            
        @self.sio.on("docs")
        def raw_data(data):
            logging.info('websocket DOCS')



        @self.sio.event
        def auth(data):
            logging.info('websocket DATA')


        @self.sio.event
        def disconnect():
            logging.info('websocket DISCONNECT')
        

    def emit_subject_message(self, message):
        url = 'http://127.0.0.1:5000/mes_subject_channel'
        response = requests.post(url, json=message.get_payload())


        retry_strategy = Retry(
        total=25,
        backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        response = http.post(url, json=message.get_payload())

    def emit_message(self, message):
        url = 'http://127.0.0.1:5000/mes_response_channel'
        data = {
            "message": message
            }

        response_dict = {}
        try:
            response_dict["response"] = message.get_response()
        except:
            pass

        try:
            response_dict["payload"] = message.get_payload()
        except:
            pass
        response = requests.post(url, json=response_dict)
        #print("RESPONSE", response)
        #self.sio.emit('log_message_display') #, message, namespace='/log_messages')
        #logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)
        # if not isinstance(message, ActorSystemMessage):
        #     if message.get_directive() == "simulation_configurations":
        #         self.configurations_pending = message.get_payload()
        #         self.begin_simulations()
        #     elif message.get_directive() == "end_round":
        #         self.agent_memory = []
        #         self.agents_to_wait = len(message.get_payload()["agents"])
        #     elif message.get_directive() == "store_agent_memory":
        #         if self.agents_to_wait > 1:
        #             self.agents_to_wait -= 1
        #             self.agent_memory.append(message.get_payload()["agent_memory"])
        #             self.send(sender, ActorExitRequest())
        
        #         else:
        #             self.agent_memory.append(message.get_payload()["agent_memory"])
        #             self.agents_to_wait -= 1
        #             self.agent_memory_prepared = True
        
        #             self.send(sender, ActorExitRequest())
        
        #             self.end_round()
        #             self.next_run()


    def emit_message_ws(self, message):
        logging.info('WSA Emit a message')
            
        if self.sio is None:
            logging.info('WSA Connection does not exist... create one...')
            self.websocket_connect()
        response_dict = {}
        try:
            response_dict["response"] = message.get_response()
        except:
            pass

        try:
            response_dict["payload"] = message.get_payload()
        except:
            pass

        self.sio.emit('admin_mes_response',response_dict, namespace="/developer" )


    def receiveMessage(self, message, sender):
        logging.info("Websocket Output: " + str(message))
        if not isinstance(message, ActorSystemMessage): 
            if isinstance(message, AdminMessage):
                if message.get_response() == "system_status":
                    self.emit_message(message)
                elif message.get_response() == "send_to_subject":
                    self.emit_subject_message(message)
                
                # if message.get_directive() == "system_status":
                #     logging.info('Status message about to be sent out')
                #     # self.sio.send({'status': message.get_payload()["status"]}, namespace="/developer" )
                #     logging.info('WS Should be logging this to system...')
                # else:
            else:
                # self.sio.emit('a', data={'response': 'ACTOR INTERNAL'},namespace="/developer" )
                #this.socket.emit("get_system_status", {data: "asfkl;jalskfjlkascvklj znlkjhnds"});
                logging.info('websocket actor received an internal message froim the system ')
                logging.info(message)
                
                # self.emit_message(message)
                # self.send(sender, "tests.,dmgf.sk,dmg")
                # self.wakeupAfter( 5, payload=message)    

    def handle(self, stuff):
        logging.info('Internal receive')
        logging.info(stuff)
