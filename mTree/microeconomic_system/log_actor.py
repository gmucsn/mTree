from thespian.actors import *
from thespian.initmsgs import initializing_messages
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.outconnect import OutConnect
from mTree.microeconomic_system.sequence_event import SequenceEvent
from mTree.microeconomic_system.initialization_messages import *
#from socketIO_client import SocketIO, LoggingNamespace
import traceback

import os
import sys
import logging
import json

EXPERIMENT_DATA = 27

@initializing_messages([('_log_actor_configuration', LogActorConfigurationPayload)],
                            initdone='prepare_log_actor')
class LogActor(Actor):
    def prepare_log_actor(self):
        self.simulation_id = self._log_actor_configuration.log_actor_configuration_payload["simulation_id"]
        self.simulation_run_id = self._log_actor_configuration.log_actor_configuration_payload["simulation_run_id"]
        self.run_number = self._log_actor_configuration.log_actor_configuration_payload["run_number"]
        self.run_code = self._log_actor_configuration.log_actor_configuration_payload["run_code"]
        self.status = self._log_actor_configuration.log_actor_configuration_payload["status"]
        self.mes_directory = self._log_actor_configuration.log_actor_configuration_payload["mes_directory"]
        self.output_type = self._log_actor_configuration.log_actor_configuration_payload["data_logging"]
        self.simulation_configuration = self._log_actor_configuration.log_actor_configuration_payload["simulation_configuration"]
        self.setup_log_files_folder()
        self.create_mes_status_file()
        self.targets = {}
        

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
        with open(os.path.join(self.tmp_data_target), "a") as file_object:
            json_data = ""
            try:
                json_data = json.dumps(message.get_content())
            except:
                json_data = message.get_content()
            file_object.write(str(message.get_timestamp()) + "\t" + json_data + "\n")

    def log_json_data(self, message):
        with open(os.path.join(self.tmp_data_target), "a") as file_object:
            output_message = message.get_content()
            #if not isinstance(output_message, dict):
            #    raise Exception("JSON Logging requires dictionary objects")
            if isinstance(output_message, str):
                temp = output_message
                output_message = {}
                output_message["content"] = temp
            output_message["timestamp"] = message.get_timestamp()
            file_object.write(json.dumps(output_message) + "\n")


    def log_sequence_event(self, message):
        sequence_line = ""
        try:
            sequence_line = str(message.timestamp)  + "\t" + message.sender + "->" + message.receiver + ": " + message.directive    
        except:
            pass

        with open(os.path.join(self.sequence_target_tmp), "a") as file_object:
            file_object.write(sequence_line + "\n")


    def log_message(self, message):
        if message.target is not None:
            log_target = self.get_log_target(message.get_target())
            with open(os.path.join(log_target), "a") as file_object:
                            file_object.write(str(message.get_timestamp()) + "\t" + str(message.get_content()).replace("\n", "  ") + "\n")

        else:
            with open(os.path.join(self.tmp_log_target), "a") as file_object:
                file_object.write(str(message.get_timestamp()) + "\t" + str(message.get_content()).replace("\n", "  ") + "\n")

        # print("SHOULD BE WRITING OUT LOG LINE")
        # if self.simulation_id is not None:
        #     message["simulation_id"] = self.simulation_id
        # if self.run_number is not None:
        #     message["run_number"] = self.run_number
        # print("LOG ACTOR SHOULD LOG")   
        # logging.log(EXPERIMENT_DATA, message)

    def get_log_target(self, target):
        if target not in self.targets.keys():
            new_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-" + target.strip() + ".log")
            self.targets[target] = new_target
            
        return self.targets[target]
            
    def setup_log_files_folder(self):
        # first check to see if the MES contains an appropriate logs directory
        log_container_directory = os.path.join(self.mes_directory, "logs") 
        if not os.path.isdir(log_container_directory):
            os.mkdir(log_container_directory)

        # setup directory for simulation run's log files
        self.output_log_folder = os.path.join(log_container_directory, self.simulation_run_id + "-R" + str(self.run_number))
        if not os.path.isdir(self.output_log_folder):
            os.mkdir(self.output_log_folder)

        
        # setup various paths to files for writing log information to 
        self.log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.log")
        self.data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.data")
        self.tmp_log_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.log.tmp")
        self.tmp_data_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-experiment.data.tmp")
        
        self.sequence_target_tmp = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-sequence.log.tmp")
        self.sequence_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-sequence.log")
        
        # if "run_number" in message.keys():
        #     self.run_number = message["run_number"]

        # self.simulation_configuration = message["simulation_configuration"]

        self.configuration_target = os.path.join(self.output_log_folder, self.simulation_run_id + "-R" + str(self.run_number) + "-configuration.json")
        with open(os.path.join(self.configuration_target), "a") as file_object:
            file_object.write(json.dumps(self.simulation_configuration, indent=4))

    
    def create_mes_status_file(self):
        '''
            This method creates a hidden json file that contains the status of an mtree mes run
            The intention is for this file to be used to watch an mes while running or to look
            at a previous run
        '''
        self.mtree_mes_status_file = os.path.join(self.output_log_folder, ".mtree_mes_status.json")

        mes_information = {}
        mes_information["simulation_id"] = self.simulation_id
        mes_information["simulation_run_id"] = self.simulation_run_id
        mes_information["run_number"] = self.run_number
        mes_information["run_code"] = self.run_code
        # !! note that these directory locations could be out of date if folders are moved !!
        mes_information["mes_directory"] = self.mes_directory
        mes_information["mes_log_directory"] = self.output_log_folder
        mes_information["status"] = self.status
        mes_information["start_time"] = None
        
        with open(os.path.join(self.mtree_mes_status_file), "a") as file_object:
            file_object.write(json.dumps(mes_information, indent=4))

    def write_mes_exception(self, exception_payload):
        self.mtree_mes_exception_file = os.path.join(self.output_log_folder, "mes_exception_information.json")
        
        with open(os.path.join(self.mtree_mes_exception_file), "w") as file_object:
            file_object.write(json.dumps(exception_payload, indent=4))

    def update_mes_status(self, status_dict):
        '''
            Method to take limited information about the status of the mes and write to the hidden status file
        '''
        if "status" in status_dict.keys() and status_dict["status"] == "Exception!":
            self.write_mes_exception(status_dict["exception_payload"])

        status_file = open (self.mtree_mes_status_file, "r")
        mes_information = json.loads(status_file.read())
        status_file.close()


        # for key in status_dict.keys():
        #     mes_information[key] = status_dict[key]
        mes_information.update(status_dict)
        
        with open(os.path.join(self.mtree_mes_status_file), "w") as file_object:
            file_object.write(json.dumps(mes_information, indent=4))

    def finalize_mes_status(self, status_dict):
        logging.info("RECEIVING A FINALIZATION REQUEST")
        logging.info(status_dict)
        
        configuration_object = status_dict["configuration_object"]
        exception_payload = None
        if "exception_payload" in status_dict:
            exception_payload = status_dict["exception_payload"]

        if exception_payload is not None:
            self.write_mes_exception(exception_payload)

        status_file = open (self.mtree_mes_status_file, "r")
        mes_information = json.loads(status_file.read())
        status_file.close()

        output_information = {}
        output_information["status"] = configuration_object.status
        output_information["start_time"] = configuration_object.start_time
        output_information["end_time"] = configuration_object.end_time


        # for key in status_dict.keys():
        #     mes_information[key] = status_dict[key]
        mes_information.update(output_information)
        
        with open(os.path.join(self.mtree_mes_status_file), "w") as file_object:
            file_object.write(json.dumps(mes_information, indent=4, default=str))


    def write_sequence_file(self):
        '''
            Method to write out a sequence file useful for producing sequence diagrams
        '''

        # first read the temp sequence file to sort based on timestamp
        sequence_events = []
        with open(os.path.join(self.sequence_target_tmp), "r") as file_object:
            for line in file_object:
                sequence_events.append(line.strip())
        sorted_events = sorted(sequence_events)

        # write the content of the sequence file out in sequential order
        with open(os.path.join(self.sequence_target), "a") as file_object:
            for event in sorted_events:
                try:
                    output = event.split("\t")[1]
                    file_object.write(output + "\n")
                except:
                    pass

        os.remove(self.sequence_target_tmp)


    def complete_log_target(self, target):
         #####

        sequence_events = []
        with open(os.path.join(target), "r") as file_object:
            for line in file_object:
                sequence_events.append(line.strip())
        sorted_events = sorted(sequence_events)

        #####
        logging.info("Completing Log Target File...")

        with open(os.path.join(self.data_target), "w") as file_object:
            for event in sorted_events:
                file_object.write(event + "\n")





    def complete_log_files(self):
        '''
            Method to close all log files and other records created for a run of an MES
        '''

        logging.info("Completing Log Files...")

        try:
            self.write_sequence_file()
        except:
            pass

        #####
        logging.info("Completing Log Sequence Files...")

        sequence_events = []
        try:
            with open(os.path.join(self.tmp_log_target), "r") as file_object:
                for line in file_object:
                    sequence_events.append(line.strip())
            sorted_events = sorted(sequence_events)
        except:
            pass

        # 
        logging.info("Completing Log Event Files...")
        try:
            with open(os.path.join(self.log_target), "a") as file_object:
                for event in sorted_events:
                    file_object.write(event + "\n")

            os.remove(self.tmp_log_target)
        except:
            pass

        #####

        sequence_events = []
        try:
            with open(os.path.join(self.tmp_data_target), "r") as file_object:
                for line in file_object:
                    sequence_events.append(line.strip())
            sorted_events = sorted(sequence_events)
        except:
            pass
        #####
        logging.info("Completing Log Data Files...")
        try:
            with open(os.path.join(self.data_target), "a") as file_object:
                for event in sorted_events:
                    file_object.write(event + "\n")

            os.remove(self.tmp_data_target)
        except:
            pass

        if len(list(self.targets.keys())) > 0:
            for target in self.targets.keys():
                self.complete_log_target(target)



    def receiveMessage(self, message, sender):
        # outconnect = self.createActor(OutConnect, globalName = "OutConnect")
        # self.send(outconnect, message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                # DEPRECATE
                if type(message) is dict:
                    logging.info("SHOULD BE SETTING UP LOGGER")
                    self.simulation_id = message["simulation_id"]
                    self.simulation_run_id = message["simulation_run_id"]
                    self.run_number = message["run_number"]
                    self.run_code = message["run_code"]
                    self.status = message["status"]
                    self.mes_directory = message["mes_directory"]
                    self.output_type = message["data_logging"]
                    self.simulation_configuration = message["simulation_configuration"]
                    self.setup_log_files_folder()
                    self.create_mes_status_file()

                elif type(message) is LogMessage:
                    if message.get_message_type() == "data":
                        if self.output_type == "json":
                            self.log_json_data(message)
                        else:
                            self.log_data(message)
                    elif message.get_message_type() == "log":
                        self.log_message(message)

                elif type(message) is SequenceEvent:
                    self.log_sequence_event(message)
                
                elif type(message) is Message:
                    if message.get_directive() == "update_mes_status":
                        self.update_mes_status(message.get_payload())
                    elif message.get_directive() == "finalize_mes_status":
                        self.finalize_mes_status(message.get_payload())
                    
                # if "message_type" in message.keys():
                #     self.simulation_id = message["simulation_id"]
                #     self.mes_directory = message["mes_directory"]
                #     if "run_number" in message.keys():
                #         self.run_number = message["run_number"]
                # else:
                #     self.log_message(message)
            except Exception as e:
                logging.info("LOGGING CRASHED")
                logging.info(traceback.format_exc())
                logline = "MES CRASHING - EXCEPTION FOLLOWS - LOG ISSUE"
                log_message = LogMessage(message_type="log", content=logline)
                self.log_message(log_message)
                log_message = LogMessage(message_type="log", content=traceback.format_exc())
                self.log_message(log_message)
                self.actorSystemShutdown()

        elif isinstance(message, ActorExitRequest):
            # clean up logs before exit
            try:
                self.complete_log_files()
            except Exception as e:
                error_type, error, tb = sys.exc_info()
                error_message = "MES AGENT CRASHING - EXCEPTION FOLLOWS \n"
                error_message += "\tSource Message: " + str(message) + "\n"
                error_message += "\tError Type: " + str(error_type) + "\n"
                error_message += "\tError: " + str(error) + "\n"
                traces = traceback.extract_tb(tb)
                trace_output = "\tTrace Output: \n"
                                
                for trace_line in traceback.format_list(traces):
                    trace_output += "\t" + trace_line + "\n"
                error_message += "\n"
                error_message += trace_output
                
                logging.info("LOGGING CRASHED DURING COMPLETION STAGE")
                logging.info(error_message)
                
