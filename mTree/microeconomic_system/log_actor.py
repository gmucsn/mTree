from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.outconnect import OutConnect

#from socketIO_client import SocketIO, LoggingNamespace
import traceback

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
        self.output_type = "string"
    
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_data(self, message):
        with open(os.path.join(self.data_target), "a") as file_object:
            file_object.write(str(message.get_timestamp()) + "\t" + str(message.get_content()) + "\n")

    def log_json_data(self, message):
        with open(os.path.join(self.data_target), "a") as file_object:
            output_message = message.get_content()
            #if not isinstance(output_message, dict):
            #    raise Exception("JSON Logging requires dictionary objects")
            if isinstance(output_message, str):
                temp = output_message
                output_message = {}
                output_message["content"] = temp
            output_message["timestamp"] = message.get_timestamp()
            file_object.write(json.dumps(output_message) + "\n")


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
                    self.run_number = message["run_number"]
                    self.mes_directory = message["mes_directory"]
                    self.output_type = message["data_logging"]
                    self.output_log_folder = os.path.join(self.mes_directory, "logs")
                    if not os.path.isdir(self.output_log_folder):
                        os.mkdir(self.output_log_folder)
                    self.log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.log")
                    self.data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.data")
                    self.tmp_log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.log.tmp")
                    self.tmp_data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.data.tmp")
                    
                    if "run_number" in message.keys():
                        self.run_number = message["run_number"]

                    self.simulation_configuration = message["simulation_configuration"]

                    with open(os.path.join(self.log_target), "a") as file_object:
                       file_object.write("Simulation Configuration: " + "\t" + json.dumps(self.simulation_configuration, indent=1) + "\n")


                elif type(message) is LogMessage:
                    if message.get_message_type() == "data":
                        if self.output_type == "json":
                            self.log_json_data(message)
                        else:
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
                logline = "MES CRASHING - EXCEPTION FOLLOWS - LOG ISSUE"
                log_message = LogMessage(message_type="log", content=logline)
                self.log_message(log_message)
                log_message = LogMessage(message_type="log", content=traceback.format_exc())
                self.log_message(log_message)
                self.actorSystemShutdown()
            