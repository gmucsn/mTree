from thespian import *
from thespian.actors import *
from thespian.system.messages.status import *
import time
import socketio
import logging


class WebSocketRouterActor(Actor):
    def __init__(self) -> None:
        logging.info('Starting web actor')
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:5000')
        
        #self.sio = socketsio.AsyncClient()
        logging.info('Cliesssnt started')
        
        # print("ALKJFLASKJF")
        @self.sio.event
        def message(data):
            self.handle(data)
            logging.info('I received a message!')

        @self.sio.event
        def connect():
            logging.info('connection established')

        @self.sio.event
        def my_message(data):
            print('message received with ', data)
            self.sio.emit('my response', {'response': 'my response'})
            logging.info('received from server')
            self.handle(data)
        
        logging.info("stuff configured")
        # @self.sio.on('my message')
        # def on_message(data):
        #     print('I received a message!')


    def receiveMessage(self, message, sender):
        self.sio.emit('my response', {'response': 'my response'})
        logging.info('receioved ')
        # self.send(sender, "tests.,dmgf.sk,dmg")

    def handle(self, stuff):
        logging.info('Internal receive')
        logging.info(stuff)
