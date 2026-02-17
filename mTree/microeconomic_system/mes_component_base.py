import json
import sys
import traceback
from datetime import timedelta

import dill
from mTree.microeconomic_system.log_message import LogMessage
from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.probe_messages import ProbeMessage
from thespian.actors import *
from thespian.initmsgs import initializing_messages


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


class MESComponentBase(Actor):
    """
    This is a mixin class. It is meant to provide a set of basic communication functions
    useful for the individual MES components to communicate and provide basic services.

    This class should not be subclassed by itself and only mixed in.
    """

    def get_simulation_property(self, name):
        if name not in self.mtree_properties.keys():
            raise Exception("Simulation property: " + str(name) + " not available")
        return self.mtree_properties[name]

    def log_message(self, logline, target=None, level=None):
        if self.log_level is None or level is None:
            log_message = LogMessage(message_type="log", content=logline, target=target)
            self.send(self.log_actor, log_message)
        elif self.log_level <= level:
            log_message = LogMessage(message_type="log", content=logline, target=target)
            self.send(self.log_actor, log_message)

    def log_data(self, logline, target=None, level=None):
        if self.log_level is None or level is None:
            log_message = LogMessage(
                message_type="data", content=logline, target=target
            )
            self.send(self.log_actor, log_message)
        elif self.log_level <= level:
            log_message = LogMessage(
                message_type="data", content=logline, target=target
            )
            self.send(self.log_actor, log_message)

    def log_sequence_event(self, message):
        sequence_event = SequenceEvent(
            message.timestamp,
            message.get_short_name(),
            self.short_name,
            message.get_directive(),
        )
        self.send(self.log_actor, sequence_event)

    def __str__(self):
        return "<Agent: " + self.__class__.__name__ + " @ " + str(self.myAddress) + ">"

    def __repr__(self):
        return self.__str__()

    def reminder(self, seconds_to_reminder, message, addresses=None):
        if addresses is None:
            if type(seconds_to_reminder) is timedelta:
                self.wakeupAfter(seconds_to_reminder, payload=message)
            else:
                # TODO if not seconds then reject
                self.wakeupAfter(
                    timedelta(seconds=seconds_to_reminder), payload=message
                )

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

            if (
                key in self._enabled_directives_state_monitors[setter_name]
                or self._enabled_directives_state_monitors[setter_name] is None
            ):
                try:
                    state_change_start_value = getattr(self, key)
                except:
                    # check for if the property does not previously exist
                    state_change_start_value = "Undeclared"
        super().__setattr__(key, value)
        if state_change_start_value is not None:
            if directive_source is not None:
                self.log_message(
                    "Agent ("
                    + self.short_name
                    + ") : Directive < "
                    + directive_source
                    + " > changing state of < "
                    + key
                    + " > from "
                    + str(state_change_start_value)
                    + " to "
                    + str(value)
                )
            else:
                self.log_message(
                    "Agent ("
                    + self.short_name
                    + ") : Function < "
                    + setter_name
                    + " > changing state of < "
                    + key
                    + " > from "
                    + str(state_change_start_value)
                    + " to "
                    + str(value)
                )

        if hasattr(self, "outlets"):
            if key in self.outlets:
                # print("LETTING: " + str(self.user) + " -- " + str(self.outlets[key]) + " -- " + str(value))

                # self.response.let_user(self.user_id, self.outlets[key], value)
                self.send_to_subject("outlet", {"property": key, "value": value})

    def get_property(self, property_name):
        try:
            return self.mtree_properties[property_name]
        except:
            return None

    def excepted_mes(self, exception_payload):
        new_message = Message()
        new_message.set_directive("excepted_mes")
        new_message.set_sender(self.myAddress)
        new_message.set_payload(exception_payload)
        self.send(self.container, new_message)

    def send_message(self, directive, receiver, payload=None):
        """Send message
        Constructs and sends a message inside the system"""
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
                {"short_name": receiver}
            )

            self.send(receiver_address, new_message)

    def exception_logging_handler(self):
        error_type, error, tb = sys.exc_info()
        error_message = "MES CRASHING IN PREPARATION - EXCEPTION FOLLOWS \n"
        error_message += "\tError Type: " + str(error_type) + "\n"
        error_message += "\tError: " + str(error) + "\n"
        traces = traceback.extract_tb(tb)
        trace_output = "\tTrace Output: \n"
        for trace_line in traceback.format_list(traces):
            trace_output += "\t" + trace_line + "\n"
        error_message += "\n"
        error_message += trace_output
        # self.log_message(error_message)
        self.log_message(
            "Agent: PREPARATION EXCEPTION! Check exception log. --- " + error_message
        )
        self.log_message(error_message)
        exception_payload = {}
        exception_payload["error_message"] = error_message
        exception_payload["error_type"] = str(error_type)
        exception_payload["error"] = str(error)

        excepting_trace = traces[0]
        exception_payload["filename"] = excepting_trace.filename
        exception_payload["lineno"] = excepting_trace.lineno
        exception_payload["name"] = excepting_trace.name
        exception_payload["line"] = excepting_trace.line

        self.excepted_mes(exception_payload)

    def receiveMessage(self, message, sender):
        # print("AGENT GOT MESSAGE: ", message) # + message)
        # self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
        # # if isinstance(message, ProbeMessage):
        # t = 1
        # probe = vars(self)
        # test = [ mthd for mthd in dir(self) if not inspect.ismethod(self.__getattribute__(mthd))  ]
        # output = {}

        # bad_fields = dill.detect.badtypes(self, depth=1).keys()
        # logging.warn(output)
        # for i in test:
        #     if i not in bad_fields:
        #         # logging.warn(i)
        #         # if not is_jsonable(self.__getattribute__(i)):
        #         #     next
        #         output[i] = self.__getattribute__(i)
        # # self.send(sender, ProbeMessage(state_response=json.dumps(output, default=str)))
        # self.send(sender, output)

        match message:
            case ProbeMessage():
                # self.mTree_logger().log(24, "{!s} got {!s}".format(self, message))
                # if isinstance(message, ProbeMessage):
                t = 1
                probe = vars(self)
                test = [
                    mthd
                    for mthd in dir(self)
                    if not inspect.ismethod(self.__getattribute__(mthd))
                ]
                output = {}

                bad_fields = dill.detect.badtypes(self, depth=1).keys()
                logging.warn(output)
                for i in test:
                    if i not in bad_fields:
                        # logging.warn(i)
                        # if not is_jsonable(self.__getattribute__(i)):
                        #     next
                        output[i] = self.__getattribute__(i)
                self.send(
                    sender, ProbeMessage(state_response=json.dumps(output, default=str))
                )
            case WakeupMessage():
                try:
                    wakeup_message = message.payload
                    directive_handler = self._enabled_directives.get(
                        wakeup_message.get_directive()
                    )
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
            case Message():
                try:
                    if message.get_directive() not in self._enabled_directives.keys():
                        raise UndefinedDirectiveException(message.get_directive())
                    directive_handler = self._enabled_directives.get(
                        message.get_directive()
                    )
                    # # try:
                    # #     self.log_message(
                    # #         "Agent ("
                    # #         + self.short_name
                    # #         + ") : About to enter directive: "
                    # #         + message.get_directive()
                    # #     )
                    # # except:
                    # #     pass

                    # try:
                    #     self.log_sequence_event(message)
                    # except:
                    #     pass

                    if message.sender == "":
                        message.sender = sender

                    directive_handler(self, message)
                    # try:
                    #     self.log_message(
                    #         "Agent ("
                    #         + self.short_name
                    #         + ": Exited directive: "
                    #         + message.get_directive()
                    #     )
                    # except:
                    #     pass
                except Exception as e:
                    self.exception_logging_handler()
            case ActorExitRequest():
                return
            case PoisonMessage():
                return
            case ChildActorExited():
                return
            case _:
                print(message)
                exception_payload = {}
                exception_payload["error_message"] = ""
                exception_payload["source_message"] = ""
                exception_payload["error_type"] = ""
                exception_payload["error"] = ""
                exception_payload["filename"] = ""
                exception_payload["lineno"] = ""
                exception_payload["name"] = ""
                exception_payload["line"] = ""

                self.excepted_mes(exception_payload)
