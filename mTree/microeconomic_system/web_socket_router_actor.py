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



class WebSocketRouterActor(Actor):
    def logout(self):
        logging.info('WEBSOCKET THING AHPPEJd actor')
        

    def __init__(self) -> None:
        # self.sio.on("message", handler=self.logout, namespace="/developer")
        #self.call_backs()
        logging.info('Starting web actor')
        # self.sio = socketio.Client()
        self.sio = socketio.Client()
        #self.sio.connect('http://localhost:5000')
        self.sio.connect('http://localhost:5000', namespaces='/developer', wait=False)
        
        #self.sio = socketsio.AsyncClient()
        logging.info('Cliesssnt started')
        
        # # print("ALKJFLASKJF")
        # #@self.sio.event
        # @self.sio.on('get_system_status', namespace='/developer')
        # def message(data):
        #     # dispatcher = self.createActor(Dispatcher, globalName = "Dispatcher")
        #     # configuration_message = Message()
        #     # configuration_message.set_directive("check_status")
        #     # response = self.send(dispatcher, configuration_message)
        #     logging.info('ACTOR RECIEVED **WEBSOCKET** MESSAGE')

        #     # return response

        # @self.sio.event
        # def connect():
        #     logging.info('connection established')

        # @self.sio.event
        # def my_message(data):
        #     print('message received with ', data)
        #     self.sio.emit('my response', {'response': 'my response'})
        #     logging.info('received from server')
        #     self.handle(data)
            
        #     logging.info("stuff configured")
        #     # @self.sio.on('my message')
        #     # def on_message(data):
        #     #     print('I received a message!')

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
        


    def receiveMessage(self, message, sender):
        if isinstance(message, AdminMessage):
            logging.info('ADmin message websocket outbound')
            if message.get_response() == "system_status":
                logging.info('==== admin message returning')
                logging.info(message)
                self.sio.emit('admin_mes_response',{'response': message.get_response(), 'payload': message.get_payload()}, namespace="/developer" )

        else:
            if message.get_directive() == "system_status":
                self.sio.send({'status': message.get_payload()["status"]}, namespace="/developer" )
                logging.info('WS Should be logging this to system...')
            else:
                self.sio.emit('a', data={'response': 'ACTOR INTERNAL'},namespace="/developer" )
                #this.socket.emit("get_system_status", {data: "asfkl;jalskfjlkascvklj znlkjhnds"});
                logging.info('websocket actor received an internal message froim the system ')
                logging.info(message)
                # self.send(sender, "tests.,dmgf.sk,dmg")
                # self.wakeupAfter( 5, payload=message)    

    def handle(self, stuff):
        logging.info('Internal receive')
        logging.info(stuff)
