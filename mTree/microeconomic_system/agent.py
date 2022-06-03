from thespian.actors import *
from thespian.initmsgs import initializing_messages

import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.sequence_event import SequenceEvent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
from mTree.microeconomic_system.address_book import AddressBook
from mTree.microeconomic_system.mes_exceptions import *
from mTree.microeconomic_system.admin_message import AdminMessage
#from socketIO_client import SocketIO, LoggingNamespace
import traceback
import logging
import json
from datetime import datetime, timedelta
import time
import sys
import inspect

@initializing_messages([('startup', str)],
                            initdone='invoke_prepare')
@directive_enabled_class
class Agent(Actor):

    def prepare(self):
        pass

    def invoke_prepare(self):
        # prepare for actor startup....
        try:
            self.prepare()
        except:
            pass

    def __init__(self):
        self.address_book = AddressBook(self)
        #socketIO = SocketIO('127.0.0.1', 5000, LoggingNamespace)
        self.log_actor = None
        self.mtree_properties = {}
        self.agent_memory = {}
        self.outlets = {}

    environment = None

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]

    def log_message(self, logline):
        log_message = LogMessage(message_type="log", content=logline)
        self.send(self.log_actor, log_message)

    def log_data(self, logline):
        log_message = LogMessage(message_type="data", content=logline)
        self.send(self.log_actor, log_message)

    def log_sequence_event(self, message):
        sequence_event = SequenceEvent(message.timestamp, message.get_short_name(), self.short_name, message.get_directive())
        self.send(self.log_actor, sequence_event)
        
    def __str__(self):
        return "<Agent: " + self.__class__.__name__+ ' @ ' + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def reminder(self, seconds_to_reminder, message, addresses=None):
        if addresses is None:
            if type(seconds_to_reminder) is timedelta:
                self.wakeupAfter( seconds_to_reminder, payload=message)    
            else:
                # TODO if not seconds then reject
                self.wakeupAfter( timedelta(seconds=seconds_to_reminder), payload=message)

        else:
            new_message = Message()
            new_message.set_directive("external_reminder")
            new_message.set_sender(self.myAddress)
            payload = {}
            payload["reminder_message"] = message
            payload["seconds_to_reminder"] = seconds_to_reminder
            new_message.set_payload(payload)

            for agent in addresses:
                self.send(agent, new_message)                

    @directive_decorator("external_reminder")
    def external_reminder(self, message:Message):
        reminder_message = message.get_payload()["reminder_message"]
        seconds_to_reminder = message.get_payload()["seconds_to_reminder"]
        self.reminder(seconds_to_reminder, reminder_message)
        
    def __setattr__(self, key, value):
        """
        magic function that passes change to the root object
        :param key:
        :param value:
        :return:
        """

        setter_name = inspect.stack()[1][3]
        directive_source = None
        state_change_start_value = None
        # it's possible that a function is causing a state change and not a directive
        if setter_name in self._enabled_directives_state_monitors.keys():
            if setter_name in self._enabled_functions_to_directives.keys():
                directive_source = self._enabled_functions_to_directives[setter_name]
            
            if key in self._enabled_directives_state_monitors[setter_name] or self._enabled_directives_state_monitors[setter_name] is None:
                try:
                    state_change_start_value = getattr(self, key)
                except:
                    # check for if the property does not previously exist
                    state_change_start_value = "Undeclared"
        super().__setattr__(key, value)
        if state_change_start_value is not None:
            if directive_source is not None:
                self.log_message("Agent (" + self.short_name + ") : Directive < " + directive_source + " > changing state of < " + key + " > from " + str(state_change_start_value) + " to " + str(value))
            else:
                self.log_message("Agent (" + self.short_name + ") : Function < " + setter_name + " > changing state of < " + key + " > from " + str(state_change_start_value) + " to " + str(value))
            
        if hasattr(self, 'outlets'):
            if key in self.outlets:
                # print("LETTING: " + str(self.user) + " -- " + str(self.outlets[key]) + " -- " + str(value))

                self.response.let_user(self.user_id, self.outlets[key], value)
                

    @directive_decorator("register_subject_connection")
    def register_subject_connection(self, message: Message):
        self.subject_id = "TEST!" #message.get_payload()["subject_id"]

    @directive_decorator("store_agent_memory")
    def store_agent_memory(self, message: Message):
        self.subject_id = "TEST!" #message.get_payload()["subject_id"]
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("store_agent_memory")
        new_message.set_payload({"agent_memory": self.agent_memory})
        self.send(self.dispatcher, new_message)


    def send_to_subject(self, command, payload):
        web_socket_router_actor = self.createActor(Actor, globalName = "WebSocketRouterActor")
        message_payload = {"command": command, "subject_id": self.subject_id, "payload": payload }
        message = AdminMessage(response="send_to_subject", payload=message_payload)
        
        self.send(web_socket_router_actor, message)


    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        self.address_book = AddressBook(self)
        
        self.environment = message.get_sender()
        self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}
        # if "agent_memory" not in dir(self):
        #     self.agent_memory = {}
        

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]

        if "agent_information" in message.get_payload().keys():
            self.short_name = message.get_payload()["agent_information"]["short_name"]
            self.agent_information = message.get_payload()["agent_information"]

        if "subject_id" in message.get_payload().keys():
            self.subject_id = message.get_payload()["subject_id"]


        #self.log_actor = message.get_payload()["log_actor"]
        #self.dispatcher = message.get_payload()["dispatcher"]
        #self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        
        # if "agent_memory" in message.get_payload().keys():
        #     print("setting my memory to... ", message.get_payload()["agent_memory"])
        #     self.agent_memory = message.get_payload()["agent_memory"]
        # else:
        #     self.agent_memory = {}

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def register_outlet(self, _property, target):  # _property used due to builtin use of property
        self.outlets[_property] = target


    def excepted_mes(self, exception_payload):
        new_message = Message()
        new_message.set_directive("excepted_mes")
        new_message.set_sender(self.myAddress)
        new_message.set_payload(exception_payload)
        self.send(self.environment, new_message)

    def send_message(self, directive, receiver, payload=None):
        """Send message
           Constructs and sends a message inside the system """
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive(directive)
        if payload is not None:
            new_message.set_payload(payload)
    
        if isinstance(receiver, list):
            for target_address in receiver:
                self.send(target_address, new_message)
        else:
            receiver_address = self.address_book.select_addresses(
                                {"short_name": receiver})

            self.send(receiver_address, new_message)

    def send(self, targetAddress, message):
        if hasattr(self, 'short_name') and type(message) is Message:
            try:
                message.set_short_name(self.short_name)
            except:
                message.set_short_name(self.__class__.__name__)
        
        if isinstance(message, Message):
            self.log_message("Agent (" + self.short_name + ") : sending to " +  " directive: " + message.get_directive())
        
        super().send(targetAddress, message)

    def receiveMessage(self, message, sender):
        #print("AGENT GOT MESSAGE: ", message) # + message)
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                if message.get_directive() not in self._enabled_directives.keys():
                    raise UndefinedDirectiveException(message.get_directive())
                directive_handler = self._enabled_directives.get(message.get_directive())
                try:
                    self.log_message("Agent (" + self.short_name + ") : About to enter directive: " + message.get_directive())
                except:
                    pass

                try:
                    self.log_sequence_event(message)
                except:
                   pass
                
                directive_handler(self, message)
                try:
                    self.log_message("Agent (" + self.short_name + ": Exited directive: " + message.get_directive())
                except:
                    pass
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
                #self.log_message(error_message)
                self.log_message("AGENT: EXCEPTION! Check exception log. ")

                exception_payload = {}
                exception_payload["error_message"] = error_message
                exception_payload["source_message"]= str(message)
                exception_payload["error_type"]= str(error_type)
                exception_payload["error"]= str(error)

                excepting_trace = traces[0] 
                exception_payload["filename"] = excepting_trace.filename
                exception_payload["lineno"] = excepting_trace.lineno
                exception_payload["name"] = excepting_trace.name
                exception_payload["line"] = excepting_trace.line
                
                self.excepted_mes(exception_payload)

        elif isinstance(message, WakeupMessage):
            try:
                wakeup_message = message.payload
                directive_handler = self._enabled_directives.get(wakeup_message.get_directive())
                directive_handler(self, wakeup_message)
            except Exception as e:
                error_type, error, tb = sys.exc_info()
                error_message = "MES AGENT CRASHING WAKING UP- EXCEPTION FOLLOWS \n"
                error_message += "\tSource Message: " + str(message) + "\n"
                error_message += "\tError Type: " + str(error_type) + "\n"
                error_message += "\tError: " + str(error) + "\n"
                traces = traceback.extract_tb(tb)
                trace_output = "\tTrace Output: \n"
                for trace_line in traceback.format_list(traces):
                    trace_output += "\t" + trace_line + "\n"
                error_message += "\n"
                error_message += trace_output
                self.log_message(error_message)
                
                # self.log_message("MES AGENT CRASHING - EXCEPTION FOLLOWS")
                # self.log_message("\tSource Message: " + str(message))
                # filename, lineno, func_name, line = traceback.extract_tb(tb)[-1]
                # self.log_message("\tError Type: " + str(error_type))
                # self.log_message("\tError: " + str(error))
                # self.log_message("\tFilename: " + str(filename))
                # self.log_message("\tLine Number: " + str(lineno))
                # self.log_message("\tFunction Name: " + str(func_name))
                # self.log_message("\tLine: " + str(line))
                
                
