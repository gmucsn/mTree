import logging
import os

import setproctitle
from mTree.core_actors.admin_message import AdminMessage
from mTree.microeconomic_system.address_book import AddressBook
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.initialization_messages import *
from mTree.microeconomic_system.mes_component_base import MESComponentBase
from mTree.microeconomic_system.mes_exceptions import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.simulation.component_initialization import ComponentInitialization
from thespian.actors import *
from thespian.initmsgs import initializing_messages


@initializing_messages(
    [
        ("startup", str),
        ("_component_initialization", ComponentInitialization),
        ("_address_book", AddressBook),
    ],
    initdone="invoke_prepare",
)
@directive_enabled_class
class Environment(MESComponentBase):
    def prepare(self):
        logging.info("Environment prepare invoke")

    def invoke_prepare(self):
        setproctitle.setproctitle("mTree - Environment")
        # Report pid to the system status actor
        system_status_actor = self.createActor(Actor, globalName="SystemStatusActor")
        pid = os.getpid()
        message = AdminMessage(directive="register_pid", payload=pid)
        self.send(system_status_actor, message)

        self.initialization = self._component_initialization
        self.iteration = self.initialization.iteration
        self.configuration = self.initialization.iteration.configuration

        # self._address_book = self._address_book_payload.address_book_payload
        self.initialization_dict = self._component_initialization
        self.mtree_properties = self.configuration.properties
        self.simulation_id = self.configuration.id
        self.simulation_run_id = self.configuration.simulation_run_id
        self.short_name = "ENV"  # self.initialization_dict["short_name"]
        self.log_actor = self.initialization.log_actor
        self.address_type = ""  # self.initialization_dict["address_type"]

        self.address_book = self._address_book
        self.address_book.register_component(self)

        self.num_agents = self.address_book.num_agents()

        self.container = self.initialization.mes_container
        self.debug = self.configuration.debug
        self.log_level = self.configuration.log_level

        # prepping log actor
        self.log_actor = self.createActor("log_actor.LogActor")

        log_basis = {}
        log_basis["message_type"] = "setup"

        self.short_name = ""

        # if "address_book" not in dir(self):
        #     self.address_book = AddressBook(self)

        log_basis["simulation_run_id"] = self.simulation_run_id
        log_basis["simulation_id"] = self.simulation_id
        log_basis["run_number"] = 1  # self.initialization_dict["simulation_run_number"]
        # TODO Fix references
        # log_basis["run_code"] = self.initialization_dict["run_code"]
        # log_basis["status"] = self.initialization_dict["status"]
        # log_basis["mes_directory"] = self.initialization_dict["mes_directory"]
        # log_basis["data_logging"] = self.initialization_dict["data_logging"]
        # log_basis["simulation_configuration"] = self.initialization_dict["simulation_configuration"]
        self.send(self.log_actor, log_basis)

        try:
            self.prepare()
        except:
            self.exception_logging_handler()

    # def __init__(self):
    #     self.address_book = AddressBook(self)
    #     self.short_name = None
    #     self.log_actor = None
    #     self.simulation_id = None
    #     self.run_number = None
    #     self.institutions = []
    #     self.agents = []
    #     self.agent_addresses = []
    #     self.mtree_properties = {}

    # def __str__(self):
    #     return (
    #         "<Environment: "
    #         + self.__class__.__name__
    #         + " @ "
    #         + str(self.myAddress)
    #         + ">"
    #     )

    # def __repr__(self):
    #     return self.__str__()

    @directive_decorator("update_mes_status")
    def update_mes_status(self, message: Message = None):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("update_mes_status")
        payload = message.get_payload()
        new_message.set_payload(payload)
        self.send(self.log_actor, new_message)

    @directive_decorator("shutdown_mes")
    def shutdown_mes(self, message: Message = None):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("shutdown_mes")
        payload = {}
        new_message.set_payload(payload)
        self.send(self.container, new_message)

    @directive_decorator("excepted_mes")
    def excepted_mes(self, message: Message):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("excepted_mes")
        # try:
        #     new_message.set_payload(message.get_payload())
        # except:
        new_message.set_payload(message)
        self.send(self.container, new_message)

    def close_environment(self):
        # asys.shutdown()
        pass

    # def get_simulation_property(self, name):
    #     if name not in self.mtree_properties.keys():
    #         raise Exception("Simulation property: " + str(name) + " not available")
    #     return self.mtree_properties[name]

    def end_round(self):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("end_round")
        payload = {}
        payload["agents"] = self.agent_addresses
        new_message.set_payload(payload)
        # self.dispatcher = self.createActor("Dispatcher", globalName="dispatcher")
        self.send(self.container, new_message)

        for agent in self.agent_addresses:
            new_message = Message()
            new_message.set_sender(self.myAddress)
            new_message.set_directive("store_agent_memory")
            self.send(agent, message)

    # def receiveMessage(self, message, sender):
    #     logging.info("ENV received a message")
    #     # self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
    #     if not isinstance(message, ActorSystemMessage):
    #         try:
    #             if message.get_directive() not in self._enabled_directives.keys():
    #                 raise UndefinedDirectiveException(message.get_directive())

    #             directive_handler = self._enabled_directives.get(
    #                 message.get_directive()
    #             )
    #             try:
    #                 self.log_message(
    #                     "Environment: About to enter directive: "
    #                     + message.get_directive()
    #                 )
    #             except:
    #                 pass

    #             try:
    #                 self.log_sequence_event(message)
    #             except:
    #                 pass

    #             directive_handler(self, message)
    #             try:
    #                 self.log_message(
    #                     "Environment: Exited directive: " + message.get_directive()
    #                 )
    #             except:
    #                 pass
    #         except Exception as e:
    #             error_type, error, tb = sys.exc_info()
    #             error_message = "MES ENVIRONMENT CRASHING - EXCEPTION FOLLOWS \n"
    #             error_message += "\tSource Message: " + str(message) + "\n"
    #             error_message += "\tError Type: " + str(error_type) + "\n"
    #             error_message += "\tError: " + str(error) + "\n"
    #             traces = traceback.extract_tb(tb)
    #             trace_output = "\tTrace Output: \n"
    #             for trace_line in traceback.format_list(traces):
    #                 trace_output += "\t" + trace_line + "\n"
    #             error_message += "\n"
    #             error_message += trace_output
    #             # self.log_message(error_message)
    #             self.log_message("Environment: EXCEPTION! Check exception log. ")
    #             exception_payload = {}
    #             exception_payload["error_message"] = error_message
    #             exception_payload["source_message"] = str(message)
    #             exception_payload["error_type"] = str(error_type)
    #             exception_payload["error"] = str(error)

    #             excepting_trace = traces[0]
    #             exception_payload["filename"] = excepting_trace.filename
    #             exception_payload["lineno"] = excepting_trace.lineno
    #             exception_payload["name"] = excepting_trace.name
    #             exception_payload["line"] = excepting_trace.line

    #             self.excepted_mes(exception_payload)
    #             ####
    #             # EXCEPTION HANDLING>..
    #             ####

    #             # self.log_message("MES AGENT CRASHING - EXCEPTION FOLLOWS")
    #             # self.log_message("\tSource Message: " + str(message))
    #             # filename, lineno, func_name, line = traceback.extract_tb(tb)[-1]
    #             # self.log_message("\tError Type: " + str(error_type))
    #             # self.log_message("\tError: " + str(error))
    #             # self.log_message("\tFilename: " + str(filename))
    #             # self.log_message("\tLine Number: " + str(lineno))
    #             # self.log_message("\tFunction Name: " + str(func_name))
    #             # self.log_message("\tLine: " + str(line))

    #     elif isinstance(message, WakeupMessage):
    #         try:
    #             wakeup_message = message.payload
    #             directive_handler = self._enabled_directives.get(
    #                 wakeup_message.get_directive()
    #             )
    #             directive_handler(self, wakeup_message)
    #         except Exception as e:
    #             self.log_message("MES ENVIRONMENT CRASHING - EXCEPTION FOLLOWS")
    #             self.log_message("\tSource Message: " + str(message))
    #             error_type, error, tb = sys.exc_info()
    #             self.log_message("\tError Type: " + str(error_type))
    #             self.log_message("\tError: " + str(error))
    #             traces = traceback.extract_tb(tb)
    #             trace_output = "\tTrace Output: \n"
    #             for trace_line in traceback.format_list(traces):
    #                 trace_output += "\t" + trace_line + "\n"
    #             self.log_message(trace_output)

    # def get_property(self, property_name):
    #     try:
    #         return self.mtree_properties[property_name]
    #     except:
    #         return None

    # def reminder(self, seconds_to_reminder, message, addresses=None):
    #     if addresses is None:
    #         if type(seconds_to_reminder) is timedelta:
    #             self.wakeupAfter(seconds_to_reminder, payload=message)
    #         else:
    #             # TODO if not seconds then reject
    #             self.wakeupAfter(
    #                 timedelta(seconds=seconds_to_reminder), payload=message
    #             )
    #     else:
    #         new_message = Message()
    #         new_message.set_directive("external_reminder")
    #         new_message.set_sender(self.myAddress)
    #         payload = {}
    #         payload["reminder_message"] = message
    #         payload["seconds_to_reminder"] = seconds_to_reminder
    #         new_message.set_payload(payload)

    #         for agent in addresses:
    #             self.send(agent, new_message)

    @directive_decorator("external_reminder")
    def external_reminder(self, message: Message):
        reminder_message = message.get_payload()["reminder_message"]
        seconds_to_reminder = message.get_payload()["seconds_to_reminder"]
        self.reminder(seconds_to_reminder, reminder_message)

    @directive_decorator("initialize_log_actor")
    def initialize_log_actor(self, message: Message):
        # self.log_actor = self.createActor("log_actor.LogActor")
        log_basis = {}
        log_basis["message_type"] = "setup"
        log_basis["simulation_id"] = self.simulation_id
        if hasattr(self, "run_number"):
            log_basis["run_number"] = self.run_number
        self.send(self.log_actor, log_basis)

    @directive_decorator("logger_setup")
    def logger_setup(self, message: Message):
        # self.log_actor = self.createActor("log_actor.LogActor") #, globalName="log_actor")

        log_basis = {}
        log_basis["message_type"] = "setup"

        # setting short name for environment
        # self.short_name = message.get_payload()["short_name"]

        short_name = message.get_payload()["short_name"]
        # self.short_name = "environment"

        # if "address_book" not in dir(self):
        #     self.address_book = AddressBook(self)

        # logging.info("ENVIRONMENT short name is : " + str(self.short_name))

        log_basis["simulation_run_id"] = message.get_payload()["simulation_run_id"]
        log_basis["simulation_id"] = message.get_payload()["simulation_id"]
        log_basis["run_number"] = message.get_payload()["simulation_run_number"]
        log_basis["run_code"] = message.get_payload()["run_code"]
        log_basis["status"] = message.get_payload()["status"]
        log_basis["mes_directory"] = message.get_payload()["mes_directory"]
        log_basis["data_logging"] = message.get_payload()["data_logging"]
        log_basis["simulation_configuration"] = message.get_payload()[
            "simulation_configuration"
        ]
        self.send(self.log_actor, log_basis)

    # def log_sequence_event(self, message):
    #     sequence_event = SequenceEvent(
    #         message.timestamp,
    #         message.get_short_name(),
    #         self.short_name,
    #         message.get_directive(),
    #     )
    #     self.send(self.log_actor, sequence_event)

    # def log_message(self, logline, target=None, level=None):
    #     if self.log_level is None or level is None:
    #         log_message = LogMessage(message_type="log", content=logline, target=target)
    #         self.send(self.log_actor, log_message)
    #     elif self.log_level <= level:
    #         log_message = LogMessage(message_type="log", content=logline, target=target)
    #         self.send(self.log_actor, log_message)

    # def log_data(self, logline, target=None, level=None):
    #     if self.log_level is None or level is None:
    #         log_message = LogMessage(
    #             message_type="data", content=logline, target=target
    #         )
    #         self.send(self.log_actor, log_message)
    #     elif self.log_level <= level:
    #         log_message = LogMessage(
    #             message_type="data", content=logline, target=target
    #         )
    #         self.send(self.log_actor, log_message)

    # def record_data(self, data):
    #     # self.log_actor = self.createActor(LogActor, globalName="log_actor")
    #     self.send(self.log_actor, data)

    @directive_decorator("simulation_properties")
    def simulation_properties(self, message: Message):
        self.dispatcher = message.get_sender()
        # self.log_actor = message.get_payload()["log_actor"]
        if "mtree_properties" not in dir(self):
            self.mtree_properties = {}

        self.mtree_properties = message.get_payload()["properties"]
        self.simulation_id = message.get_payload()["simulation_id"]
        self.simulation_run_id = message.get_payload()["simulation_run_id"]
        if "subjects" in message.get_payload().keys():
            self.subjects = message.get_payload()["subjects"]

        # if "subjects" in message.get_payload()["properties"].keys():
        #     self.subjects = message.get_payload()["properties"]["subjects"]
        #     logging.info("Subjects list available...")
        #     logging.info(self.subjects)
        if "run_number" in message.get_payload().keys():
            self.run_number = message.get_payload()["run_number"]

    # @directive_decorator("setup_agent_requests")
    # def setup_agent_requests(self, message:Message):
    #     # if "address_book" not in dir(self):
    #     #     self.address_book = AddressBook(self)

    #     if "agents" not in dir(self):
    #         self.agents = []
    #         self.agent_addresses = []
    #     # ensure that the actor system and institution are running...
    #     #message = MessageSpace.create_agent(agent_class)
    #     num_agents = message.get_payload().number
    #     agent_class = message.get_payload().source_class

    #     # need to check source hash for simulation
    #     source_hash = message.get_payload().source_hash

    #     # memory = False
    #     # agent_memory = None
    #     # if "agent_memory" in message.get_payload().keys():
    #     #     memory = True
    #     #     agent_memory = message.get_payload()["agent_memory"]

    #     if "subjects" in dir(self):
    #         self.subject_map = {}

    #     for i in range(num_agents):
    #         agent_number = i + 1
    #         new_agent = self.createActor(agent_class, sourceHash=source_hash)
    #         self.send(new_agent, agent_class + " " + str(agent_number) )
    #         self.agent_addresses.append(new_agent)
    #         self.agents.append([new_agent, agent_class])

    #         agent_info = {}
    #         agent_info["address_type"] = "agent"
    #         agent_info["address"] = new_agent
    #         agent_info["component_class"] = agent_class
    #         agent_info["component_number"] = agent_number
    #         agent_info["short_name"] = agent_class + " " + str(agent_number)

    #         self.address_book.add_address(agent_info["short_name"], agent_info)

    #         new_message = Message()
    #         #new_message.set_sender(self.myAddress)
    #         new_message.set_directive("simulation_properties")
    #         new_message.set_sender(self.myAddress)
    #         payload = {}
    #         #if "mtree_properties" not in dir(self):
    #         payload["log_actor"] = self.log_actor
    #         #payload["dispatcher"] = self.createActor("Dispatcher", globalName="dispatcher")
    #         payload["properties"] = self.mtree_properties
    #         payload["agent_information"] = agent_info
    #         if "subjects" in dir(self):
    #             payload["subject_id"] = self.subjects[i]["subject_id"]
    #             self.subject_map[payload["subject_id"]] = new_agent

    #         # if memory:
    #         #     payload["agent_memory"] = agent_memory
    #         new_message.set_payload(payload)
    #         self.send(new_agent, new_message)

    # @directive_decorator("distribute_address_book")
    # def distribute_address_book(self, message:Message):
    #     logging.info("Address book to distribute:")
    #     logging.info(self.address_book._export_data())

    #     logging.info("Distributing address book for setup...")
    #     for agent in self.agent_addresses:
    #         super().send(agent, AddressBookPayload(address_book_payload=self.address_book._export_data()))

    #     logging.info("Distributing address book for inst setup...")
    #     for institution in self.institutions:
    #         super().send(institution, AddressBookPayload(address_book_payload=self.address_book._export_data()))
    #     logging.info("Address Book distribution finished...")

    # @directive_decorator("setup_agents")
    # def setup_agents(self, message:Message):
    #     if "agents" not in dir(self):
    #         self.agents = []
    #         self.agent_addresses = []
    #     # ensure that the actor system and institution are running...
    #     #message = MessageSpace.create_agent(agent_class)
    #     num_agents = message.get_payload()["num_agents"]
    #     agent_class = message.get_payload()["agent_class"]

    #     # need to check source hash for simulation
    #     source_hash = message.get_payload()["source_hash"]

    #     # memory = False
    #     # agent_memory = None
    #     # if "agent_memory" in message.get_payload().keys():
    #     #     memory = True
    #     #     agent_memory = message.get_payload()["agent_memory"]

    #     if "subjects" in dir(self):
    #         self.subject_map = {}

    #     for i in range(num_agents):
    #         agent_number = i + 1
    #         new_agent = self.createActor(agent_class, sourceHash=source_hash)
    #         ###
    #         # Agent Initialization Message #1
    #         ###
    #         super().send(new_agent, agent_class + " " + str(agent_number))

    #         ###
    #         # Agent Initialization Message #2
    #         ###
    #         startup_payload = {}
    #         startup_payload["address_type"] = "agent"
    #         startup_payload["address"] = new_agent
    #         startup_payload["component_class"] = agent_class
    #         startup_payload["component_number"] = agent_number
    #         startup_payload["short_name"] = agent_class + " " + str(agent_number)
    #         startup_payload["properties"] = self.mtree_properties

    #         startup_payload["environment"] = self.myAddress
    #         startup_payload["simulation_id"] = self.simulation_id
    #         startup_payload["simulation_run_id"] = self.simulation_run_id
    #         startup_payload["log_actor"] = self.log_actor
    #         if "run_number" in dir(self):
    #             startup_payload["run_number"] = self.run_number

    #         if "subjects" in dir(self):
    #             startup_payload["subject_id"] = self.subjects[i]["subject_id"]
    #             self.subject_map[payload["subject_id"]] = new_agent
    #         ###
    #         # Agent Initialization Message #2
    #         ###

    #         super().send(new_agent, StartupPayload(startup_payload=startup_payload))

    #         ###

    #         self.agent_addresses.append(new_agent)
    #         self.agents.append([new_agent, agent_class])

    #         agent_info = {}
    #         agent_info["address_type"] = "agent"
    #         agent_info["address"] = new_agent
    #         agent_info["component_class"] = agent_class
    #         agent_info["component_number"] = agent_number
    #         agent_info["short_name"] = agent_class + " " + str(agent_number)

    #         self.address_book.add_address(agent_info["short_name"], agent_info)

    #         new_message = Message()
    #         #new_message.set_sender(self.myAddress)
    #         new_message.set_directive("simulation_properties")
    #         new_message.set_sender(self.myAddress)
    #         payload = {}
    #         #if "mtree_properties" not in dir(self):
    #         payload["log_actor"] = self.log_actor
    #         #payload["dispatcher"] = self.createActor("Dispatcher", globalName="dispatcher")
    #         payload["properties"] = self.mtree_properties
    #         payload["agent_information"] = agent_info
    #         if "subjects" in dir(self):
    #             payload["subject_id"] = self.subjects[i]["subject_id"]
    #             self.subject_map[payload["subject_id"]] = new_agent

    #         # if memory:
    #         #     payload["agent_memory"] = agent_memory
    #         new_message.set_payload(payload)
    #         #self.send(new_agent, new_message)

    @directive_decorator("agent_action_forward")
    def agent_action_forward(self, message: Message):
        subject_id = message.get_payload()["subject_id"]
        subject_agent_map = self.subject_map[subject_id]
        new_message = Message()
        new_message.set_directive(message.get_payload()["action"])
        new_message.set_sender(self.myAddress)
        new_message.set_payload(message.get_payload())
        self.send(subject_agent_map, new_message)

        # @directive_decorator("setup_institution")
        # def create_institution(self, message:Message):
        #     if "institutions" not in dir(self):
        #         self.institutions = []

        #     institution_class = message.get_payload()["institution_class"]
        #     source_hash = message.get_payload()["source_hash"]
        #     institution_order = message.get_payload()["order"]

        #     new_institution = self.createActor(institution_class, sourceHash=source_hash)

        #     ###
        #     # Insitutiton Initialization Message 1
        #     ###
        #     super().send(new_institution, institution_class + " " + str(institution_order))

        #     startup_payload = {}
        #     startup_payload["address_type"] = "institution"
        #     startup_payload["address"] = new_institution
        #     startup_payload["component_class"] = institution_class
        #     startup_payload["component_number"] = 1
        #     startup_payload["short_name"] = institution_class + " " + str(institution_order)
        #     startup_payload["properties"] = self.mtree_properties

        #     startup_payload["environment"] = self.myAddress
        #     startup_payload["simulation_id"] = self.simulation_id
        #     startup_payload["simulation_run_id"] = self.simulation_run_id
        #     startup_payload["log_actor"] = self.log_actor
        #     if "run_number" in dir(self):
        #         startup_payload["run_number"] = self.run_number

        #     ###
        #     # Insitutiton Initialization Message 2
        #     ###
        #     super().send(new_institution, StartupPayload(startup_payload=startup_payload))

        #     institution_info = {}
        #     institution_info["address_type"] = "institution"
        #     institution_info["address"] = new_institution
        #     institution_info["component_class"] = institution_class
        #     institution_info["component_number"] = 1
        #     institution_info["short_name"] = institution_class + " " + str(institution_order)
        #     self.address_book.add_address(institution_info["short_name"], institution_info)

        #     new_message = Message()
        #     #new_message.set_sender(self.myAddress)
        #     new_message.set_directive("simulation_properties")
        #     payload = {}

        #     #if "mtree_properties" not in dir(self):
        #     #payload["dispatcher"] = self.createActor("Dispatcher", globalName="dispatcher")
        #     payload["environment"] = self.myAddress
        #     payload["properties"] = self.mtree_properties
        #     payload["simulation_id"] = self.simulation_id
        #     payload["simulation_run_id"] = self.simulation_run_id
        #     payload["log_actor"] = self.log_actor
        #     if "run_number" in dir(self):
        #         payload["run_number"] = self.run_number

        #     payload["institution_info"] = institution_info

        #     new_message.set_payload(payload)
        #     #self.send(new_institution, new_message)

        #     self.institutions.append(new_institution)

        # def send_message(self, directive, receiver, payload=None):
        #     """Send message
        #     Constructs and sends a message inside the system"""
        #     new_message = Message()
        #     new_message.set_sender(self.myAddress)
        #     new_message.set_directive(directive)
        #     if payload is not None:
        #         new_message.set_payload(payload)

        #     if isinstance(receiver, list):
        #         for target_address in receiver:
        #             self.send(target_address, new_message)

        #     else:
        #         receiver_address = self.address_book.select_addresses(
        #             {"short_name": receiver}
        #         )

        #         self.send(receiver_address, new_message)

        #     # else:
        #     #     receiver_address = receiver
        #     #     # self.address_book.select_addresses(
        #     #     #                     {"short_name": receiver})

        #     #     self.send(receiver_address, new_message)

        # def send(self, targetAddress, message):
        #     if hasattr(self, "short_name") and type(message) is Message:
        #         try:
        #             message.set_short_name(self.short_name)
        #         except:
        #             message.set_short_name(self.__class__.__name__)
        #     elif type(message) is Message:
        #         try:
        #             message.set_short_name(self.__class__.__name__)
        #         except:
        #             pass

        if isinstance(message, Message):
            self.log_message(
                "Environment: sending to " + " directive: " + message.get_directive()
            )

        if type(targetAddress) is list:
            if len(targetAddress) == 0:
                raise Exception("Trying to send to an empty list of addresses.")
            for address in targetAddress:
                super().send(address, message)
        else:
            if targetAddress is not None:
                super().send(targetAddress, message)

    def list_agents(self):
        message = MessageSpace.list_agents()
        # return asys.ask(self.institutions, message, timedelta(seconds=1.5))

    def get_agents_wealth(self):
        message = MessageSpace.get_wealths()
        print("Message: {}".format(message))
        # return asys.ask(self.institutions, message, timedelta(seconds=1.5))
