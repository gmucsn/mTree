from thespian.actors import *
from thespian.initmsgs import initializing_messages

from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.address_book import AddressBook
from mTree.microeconomic_system.mes_exceptions import *
import uuid
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.sequence_event import SequenceEvent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.log_actor import LogActor
import logging
import json
import traceback
from datetime import datetime, timedelta
import time
import sys

@initializing_messages([('startup', str)],
                            initdone='invoke_prepare')
@directive_enabled_class
class Institution(Actor):

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
        self.log_actor = None
        self.dispatcher = None
        self.run_number = None
        self.agents = []
        self.agent_ids = []
        self.mtree_properties = {}


    def log_sequence_event(self, message):
        # logging.info("Institution should be sequence logging")
        # logging.info("ISL: " + str(message))
        sequence_event = SequenceEvent(message.timestamp, message.get_short_name(), self.short_name, message.get_directive())
        self.send(self.log_actor, sequence_event)

    def log_message(self, logline):
        log_message = LogMessage(message_type="log", content=logline)
        self.send(self.log_actor, log_message)

    def log_data(self, logline):
        log_message = LogMessage(message_type="data", content=logline)
        self.send(self.log_actor, log_message)

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]


    def __str__(self):
        return "<Institution: " + self.__class__.__name__ + ' @ ' + str(self.myAddress) + ">"

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

    def shutdown_mes(self):
        new_message = Message()
        new_message.set_directive("shutdown_mes")
        new_message.set_sender(self.myAddress)
        payload = {}
        new_message.set_payload(payload)
        self.send(self.environment, new_message)
        

    def excepted_mes(self, exception_payload):
        new_message = Message()
        new_message.set_directive("excepted_mes")
        new_message.set_sender(self.myAddress)
        new_message.set_payload(exception_payload)
        self.send(self.environment, new_message)


    @directive_decorator("external_reminder")
    def external_reminder(self, message:Message):
        reminder_message = message.get_payload()["reminder_message"]
        seconds_to_reminder = message.get_payload()["seconds_to_reminder"]
        self.reminder(seconds_to_reminder, reminder_message)

    def receiveMessage(self, message, sender):
        #self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        if not isinstance(message, ActorSystemMessage):
            try:
                if message.get_directive() not in self._enabled_directives.keys():
                    raise UndefinedDirectiveException(message.get_directive())
                directive_handler = self._enabled_directives.get(message.get_directive())
                try:
                    self.log_message("Institution (" + self.short_name + ") : About to enter directive: " + message.get_directive())
                except:
                    pass
                
                try:
                    self.log_sequence_event(message)
                except:
                    logging.info("AN EXCEPTED INSTITUTION LOG")
                    logging.info("EIL: " + str(message))
                    pass

                directive_handler(self, message)
                try:
                    self.log_message("Institution (" + self.short_name + ") : Exited directive: " + message.get_directive())
                except:
                    pass
            except Exception as e:
                error_type, error, tb = sys.exc_info()
                error_message = "MES INSITUTION CRASHING - EXCEPTION FOLLOWS \n"
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
                self.log_message("INSITUTION: EXCEPTION! Check exception log. ")
                self.log_message(error_message)
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
                self.log_message("MES CRASHING - EXCEPTION FOLLOWS")
                self.log_message("\tSource Message: " + str(message))
                
                self.log_message(traceback.format_exc())
                self.actorSystemShutdown()
        
    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def log_experiment_data(self, data):
        #self.log_actor = self.createActor(LogActor, globalName="log_actor")
        self.send(self.log_actor, data)

    @directive_decorator("address_book_update")
    def address_book_update(self, message: Message):
        addresses = message.get_payload()
        self.address_book.merge_addresses(addresses)
        

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        if "address_book" not in dir(self):
            self.address_book = AddressBook(self)
        
        self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}

        if "properties" in message.get_payload().keys():
            self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]

        if "institution_info" in message.get_payload().keys():
            self.institution_info = message.get_payload()["institution_info"]
            self.short_name = message.get_payload()["institution_info"]["short_name"]
            
        #self.log_actor = message.get_payload()["log_actor"]
        #self.dispatcher = message.get_payload()["dispatcher"]
        #self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        
        self.environment = message.get_payload()["environment"]

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
            logging.info("SHOULD BE GETTING THE ADDRESS")
            logging.info(self.address_book.addresses)
            logging.info("---> " + str(receiver_address))
            self.send(receiver_address, new_message)


    def send(self, targetAddress, message):
        if hasattr(self, 'short_name') and type(message) is Message:
            try:
                message.set_short_name(self.short_name)
            except:
                message.set_short_name(self.__class__.__name__)

        if isinstance(message, Message):
            self.log_message("Institution (" + self.short_name + ") : sending to "  + " directive: " + message.get_directive())
        super().send(targetAddress, message)


    def add_agent(self, agent_class):
        if "agents" not in dir(self):
            self.agents = []
            self.agent_ids = []

        agent_id = str(uuid.uuid1())

#        agent = asys.createActor(agent_class, globalName = agent_id)
        agent = self.createActor(agent_class)  # creates agent as child of institution
        self.agents.append(agent)
        self.agent_ids.append(agent_id)

