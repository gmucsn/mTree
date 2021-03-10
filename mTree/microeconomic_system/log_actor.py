from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.outconnect import OutConnect

#from socketIO_client import SocketIO, LoggingNamespace
import os
import logging
import json

EXPERIMENT_DATA = 27


class LogActor(Actor):
    def experiment_log(self, log_message):
        #self.mTree_logger().log(25, log_message)
        pass


    def __str__(self):
        return "<LogActor: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def __init__(self):
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.message_counter = 0
        self.mtree_properties = {}
        self.simulation_id = None
        self.run_number = None
        self.message_buffer = ""
    
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_message(self, message):
        print("ANOTHER MESSAGE LOGGED....")
        #with open(os.path.join(self.mes_directory, "experiment.log"), "a") as file_object:
        #    file_object.write(message + "\n")

        # print("SHOULD BE WRITING OUT LOG LINE")
        # if self.simulation_id is not None:
        #     message["simulation_id"] = self.simulation_id
        # if self.run_number is not None:
        #     message["run_number"] = self.run_number
        # print("LOG ACTOR SHOULD LOG")   
        # logging.log(EXPERIMENT_DATA, message)

    def receiveMessage(self, message, sender):
        # outconnect = self.createActor(OutConnect, globalName = "OutConnect")
        # self.send(outconnect, message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        
        if not isinstance(message, ActorSystemMessage):
            #try:
                if type(message) is dict:
                    print(message)
                    self.simulation_id = message["simulation_id"]
                    self.mes_directory = message["mes_directory"]
                    if "run_number" in message.keys():
                        self.run_number = message["run_number"]
                else:
                    print("LOG ACTOR SHOULD LOG") 
                    print("LOG ACTOR SHOULD LOG") 
                    print("LOG ACTOR SHOULD LOG") 
                    print("LOG ACTOR SHOULD LOG") 
                    print("LOG ACTOR SHOULD LOG") 
                    print("LOG ACTOR SHOULD LOG") 
                    print(message)
                    self.log_message(message)

                # if "message_type" in message.keys():
                #     self.simulation_id = message["simulation_id"]
                #     self.mes_directory = message["mes_directory"]
                #     if "run_number" in message.keys():
                #         self.run_number = message["run_number"]
                # else:
                #     self.log_message(message)
            #except:
            #    pass            
