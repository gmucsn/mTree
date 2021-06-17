from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
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

    def log_data(self, message):
        
        with open(os.path.join(self.data_target), "a") as file_object:
           file_object.write(str(message.get_timestamp()) + "\t" + str(message.get_content()) + "\n")

    def log_message(self, message):
        with open(os.path.join(self.log_target), "a") as file_object:
           file_object.write(str(message.get_timestamp()) + "\t" + str(message.get_content()) + "\n")

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
            try:
                if type(message) is dict:
                    self.simulation_id = message["simulation_id"]
                    self.simulation_run_id = message["simulation_run_id"]
                    self.mes_directory = message["mes_directory"]
                    self.output_log_folder = os.path.join(self.mes_directory, "logs")
                    if not os.path.isdir(self.output_log_folder):
                        os.mkdir(self.output_log_folder)
                    self.log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-experiment.log")
                    self.data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-experiment.data")
                    self.tmp_log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-experiment.log.tmp")
                    self.tmp_data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-experiment.data.tmp")
                    

                    if "run_number" in message.keys():
                        self.run_number = message["run_number"]
                elif type(message) is LogMessage:
                    if message.get_message_type() == "data":
                        self.log_data(message)
                    elif message.get_message_type() == "log":
                        self.log_message(message)

                # if "message_type" in message.keys():
                #     self.simulation_id = message["simulation_id"]
                #     self.mes_directory = message["mes_directory"]
                #     if "run_number" in message.keys():
                #         self.run_number = message["run_number"]
                # else:
                #     self.log_message(message)
            except Exception as e:
                self.log_message("MES LOG ACTOR CRASHING - EXCEPTION FOLLOWS")
                self.log_message(traceback.format_exc())
                self.actorSystemShutdown()       
