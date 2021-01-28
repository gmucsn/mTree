import socketio
from thespian.actors import *


class OutConnect(Actor):
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:5000', namespaces=['/log_messages'])

    def receiveMessage(self, message, sender):
        self.sio.emit('log_message_display', {'foo': 'bar'}, namespace='/log_messages')
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
