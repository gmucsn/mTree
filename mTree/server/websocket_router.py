import asyncio
import socketio

from mTree.microeconomic_system.dispatcher import Dispatcher
from thespian.actors import *


# class Async:
#     def __init__(self):
#         self.loop=asyncio.get_event_loop()

#     def async_loop(f):
#         def decorated(self, *args, **kwargs):
#             self.loop.run_until_complete(f(self, *args, **kwargs))
#         return decorated

#     @async_loop
#     async def function(self, word):
#         print(word)
#         await asyncio.sleep(1.0)

import socketio
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




class WebsocketRouter():
    __instance = None
    
    def __init__(self):
        if WebsocketRouter.__instance is None:
            
            

            capabilities = dict([('Admin Port', 19000)])
            self.actor_system = ActorSystem("multiprocTCPBase", capabilities)
            # self.wrapper = Wrapper_class(self.actor_system)
            # self.wrapper.run()
# self.sio = socketio.AsyncClient()
            # self.sio.connect('http://localhost:5000', namespaces=['/admin'])
            # self.sio.on('message',handler=self.message_handler, namespace="/admin")

            # self.loop = asyncio.get_event_loop()
            # self.loop.run_until_complete(self.system_listen())
            
            # self.dispatcher = ActorSystem("multiprocTCPBase", capabilities).createActor(Dispatcher, globalName = "Dispatcher")
            
            WebsocketRouter.__instance = self



    def message_handler(self, msg):
        print('Received message: ', msg)
        self.sio.send( 'response')
        self.sio.emit("get_system_status", {"data": "reacting on the message handler"})
        
    # @sio.on('message', namespace='/admin')
    # def message(data):
    #     print("WEBSOCKET GOT A MESSAGE FROM THE WEB APP")
    #     # dispatcher = self.createActor(Dispatcher, globalName = "Dispatcher")
    #     # configuration_message = Message()
    #     # configuration_message.set_directive("check_status")
    #     # response = self.send(dispatcher, configuration_message)
        
    #     # return response

    # @self.sio.event
    # def connect():
    #     logging.info('connection established')

    # @self.sio.event
    # def my_message(data):
    #     print('message received with ', data)
    #     self.sio.emit('my response', {'response': 'my response'})
        
    #     # @self.sio.on('my message')
    #     # def on_message(data):
    #     #     print('I received a message!')

        
    async def system_listen(self):
        r = True
        while r:
            print("WEBSOCKET RECEIVED STUFF")
            print(r)
            r = self.actor_system.listen()