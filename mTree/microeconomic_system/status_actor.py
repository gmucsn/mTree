from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.outconnect import OutConnect

#from socketIO_client import SocketIO, LoggingNamespace

import logging
import json

import setproctitle


class StatusActor(Actor):
    def __str__(self):
        return "<StatusActor: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        setproctitle.setproctitle("mTree - StatusActor")
        self.configurations_pending = []
        self.configurations_finished = []
        self.agent_memory = {}
        


    def receiveMessage(self, message, sender):
        #outconnect = ActorSystem("multiprocTCPBase").createActor(OutConnect, globalName = "OutConnect")
        #self.send(outconnect, message)
        #logging.info("MESSAGE RCVD: %s DIRECTIVE: %s SENDER: %s", self, message, sender)
        # with open("/Users/Shared/repos/mTree_auction_examples/sample_output", "a") as file_object:
        #     file_object.write("SHOULD BE RUNNING SIMULATION" + str(message) +  "\n")
    
        if not isinstance(message, ActorSystemMessage):
            if message.get_directive() == "simulation_configurations":
                self.configurations_pending = message.get_payload()
                self.begin_simulations()
            elif message.get_directive() == "end_round":
                self.agent_memory = []
                self.agents_to_wait = len(message.get_payload()["agents"])
            elif message.get_directive() == "store_agent_memory":
                if self.agents_to_wait > 1:
                    self.agents_to_wait -= 1
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                    self.send(sender, ActorExitRequest())
        
                else:
                    self.agent_memory.append(message.get_payload()["agent_memory"])
                    self.agents_to_wait -= 1
                    self.agent_memory_prepared = True
        
                    self.send(sender, ActorExitRequest())
        
                    self.end_round()
                    self.next_run()

