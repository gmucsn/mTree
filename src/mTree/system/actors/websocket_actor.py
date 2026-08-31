import datetime
import json
import logging as log
import os
import select
from collections import namedtuple
from datetime import timedelta

import websocket
from thespian.actors import Actor, ActorExitRequest, WakeupMessage
from websocket import ABNF

from mTree.microeconomic_system.message import Message
from mTree.simulation.configuration import Configuration
from mTree.simulation.human_subject_experiment_message import (
    HumanSubjectExperimentMessage,
)
from mTree.simulation.human_subject_run import HumanSubjectRun
from mTree.simulation.library import Library
from mTree.simulation.run import Run

# Message to send to open the connection
Start_Websocket = namedtuple("Start_Websocket", "ws_addr start_msg upstream")
# Message type that's sent to the 'upstream'
Websocket_Output = namedtuple("Websocket_Output", "msg")
# Message to send to send more data out the websocket
Websocket_Input = namedtuple("Websocket_Input", "msg")

# Maximum number of messages to read per wakeup ; raise this if you see
# a lot of "WebsocketClientActor not keeping up with incoming websocket data"
# messages in the log output
MAX_MSGS_PER_READ = 50


class CommandHandler:
    def __init__(self):
        self.experiment = None

    def start_experiment(self, ws_actor):
        dispatcher = ws_actor.createActor(Actor, globalName="Dispatcher")

        run_message = Message()
        run_message.set_directive("simulation_configurations")

        filepath = "/workspaces/mTree/examples/human_subject_auction/config/basic_human_subject_auction.yaml"
        configuration = Library.load_configuration_from_path(filepath)
        config_base_name = os.path.basename(filepath).split(".")[0]
        # Simulation Run ID Generator - TODO consolidate with subject ID generation

        nowtime = datetime.datetime.now().timestamp()
        nowtime_filename = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
        simulation_run_id = config_base_name + "-" + nowtime_filename
        # configuration.simulation_run_id = simulation_run_id
        run = Run(configuration=configuration, simulation_run_id=simulation_run_id)
        run_message.set_payload(run)
        ws_actor.send(
            dispatcher, run_message
        )  # createActor(Dispatcher, globalName = "Dispatcher")


class WebsocketActor(Actor):
    """
    A websocket client wrapped in an Actor

    This was originally written to support fetching streaming data via
    a websocket; the Websocket_Input bits are less stress-tested.

    Usage:

        ws_addr = "wss://ws-feed.somesite.com"
        startmsg = Start_Websocket(ws_addr, start_msg, receipient_Actor)
        self.client = self.createActor(WebsocketClientActor)
        self.send(self.client, startmsg)

    ...and recipient_Actor will start receiveing Websocket_Output messages

    """

    def __init__(self):
        # super(WebsocketActor, self).__init__()
        super().__init__()
        self.started = False
        self.running = False
        self.ws = None
        self.subject_to_actor_mapping = {}

    def message_handler(self, str_origin_message: str):
        log.info(f"WS Message received: {str_origin_message}")
        ws_origin_message = HumanSubjectExperimentMessage.model_validate_json(
            str_origin_message
        )
        log.info(f"WS loaded Message received: {ws_origin_message}")
        match ws_origin_message.action:
            case "start_experiment":
                dispatcher = self.createActor(Actor, globalName="Dispatcher")

                run_message = Message()
                run_message.set_directive("human_subject_configuration")
                nowtime_filename = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
                configuration = Configuration.model_validate(
                    ws_origin_message.payload["configuration"]
                )
                simulation_run_id = configuration.name + "-" + nowtime_filename
                run = HumanSubjectRun(
                    configuration=configuration,
                    simulation_run_id=simulation_run_id,
                    subject_ids=ws_origin_message.payload["subject_ids"],
                )
                run_message.set_payload(run)
                self.send(
                    dispatcher, run_message
                )  # createActor(Dispatcher, globalName = "Dispatcher")
            case "send_to_subject":
                self.ws.send(m.start_msg)
            case "send_to_agent":
                agent_address = self.subject_to_actor_mapping[
                    ws_origin_message.destination
                ]
                payload = ws_origin_message.payload
                new_message = Message()  # declare message
                new_message.set_sender(
                    self.myAddress
                )  # set the sender of message to this actor
                new_message.set_directive(
                    payload["directive"]
                )  # Set the directive (refer to 3. Make Messages) - has to match receiver decorator
                new_message.set_payload(payload)
                self.send(agent_address, new_message)

    def check_websocket(self):
        msgs = 0
        events = self.epoll.poll(0)
        while events and msgs < MAX_MSGS_PER_READ:
            for fileno, event in events:
                if not (event & select.EPOLLIN):
                    self.send(self.myAddress, ActorExitRequest())
                op_code, frame = self.ws.recv_data_frame(True)
                if op_code == ABNF.OPCODE_CLOSE:
                    self.send(self.myAddress, ActorExitRequest())
                elif op_code in (ABNF.OPCODE_PING, ABNF.OPCODE_PONG, ABNF.OPCODE_CONT):
                    pass  # ignore
                else:
                    msgs += 1
                    self.message_handler(frame.data)
                    # self.send(self.config.upstream, Websocket_Output(frame.data))
            events = self.epoll.poll(0)
        if msgs >= MAX_MSGS_PER_READ:
            log.critical(
                "WebsocketClientActor not keeping up with incoming websocket data"
            )

    def receiveMsg_Start_Websocket(self, m, sender):
        if self.started:  # already started
            return
        self.config = m
        self.started = True
        self.running = True

        # open the connection
        websocket.enableTrace(False)
        self.ws = websocket.create_connection(m.ws_addr)
        # set up the socket monitoring
        self.epoll = select.epoll()
        mask = select.EPOLLIN | select.EPOLLHUP | select.EPOLLERR
        self.epoll.register(self.ws.sock.fileno(), mask)

        # start checking for data
        self.send(self.myAddress, WakeupMessage(None))

    def receiveMsg_Websocket_Input(self, m, sender):
        if not self.running:  # can't send
            return
        log.debug("Websocket sending %r", m.msg)
        self.ws.send(m.msg)

    def receiveMsg_WakeupMessage(self, m, sender):
        if not self.running:  # stopped
            return
        try:
            self.check_websocket()
        except Exception as e:
            log.error("Got exception: %r", e)
            self.send(self.myAddress, ActorExitRequest())
            raise

        self.wakeupAfter(timedelta(milliseconds=20))

    def receiveMsg_ActorExitRequest(self, m, sender):
        """Stop the Websocket, and the actor"""
        log.info("Websocket exiting")
        self.running = False
        self.epoll.close()
        self.ws.close()

    def receiveMsg_HumanSubjectExperimentMessage(self, m, sender):
        log.info(f"received a human subject message {m}")
        match m.action:
            case "agent_to_subject_mapping":
                subject_id = m.payload["subject_id"]
                actor_address = m.payload["actor_address"]
                # Changing to avoid serialization
                m.payload["actor_address"] = "local"
                self.subject_to_actor_mapping[subject_id] = actor_address
                log.info(f"sending a websocket message upstream {m}")
                self.ws.send_text(m.model_dump_json())
            case "hotwire_message":
                subject_id = m.payload["subject_id"]
                actor_address = m.payload["actor_address"]
                # Changing to avoid serialization
                m.payload["actor_address"] = "local"
                self.subject_to_actor_mapping[subject_id] = actor_address
                log.info(f"sending a websocket message upstream {m}")
                final_hotwire_message = f"""<turbo-stream action="{m.payload["action"]}" target="{m.payload["target"]}">
                <template>
                                            {m.payload["template"]}
                </template>
                </turbo-stream>
                """
                final_message = {
                    "destination": subject_id,
                    "message_kind": "hotwire_message",
                    "content": final_hotwire_message,
                }

                self.ws.send_text(json.dumps(final_message))
            case _:
                pass

    def receiveMessage(self, m, sender):
        # try:
        handler = {
            WakeupMessage: self.receiveMsg_WakeupMessage,
            Start_Websocket: self.receiveMsg_Start_Websocket,
            Websocket_Input: self.receiveMsg_Websocket_Input,
            ActorExitRequest: self.receiveMsg_ActorExitRequest,
            HumanSubjectExperimentMessage: self.receiveMsg_HumanSubjectExperimentMessage,
        }.get(type(m), None)
        if handler is None:
            log.error("Unhandled message %r from %r", m, sender)
            return
        handler(m, sender)

    # except:
    #     pass
