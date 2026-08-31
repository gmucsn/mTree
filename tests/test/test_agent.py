import logging
import os

import pytest
from thespian.actors import *
from thespian.actors import ActorSystem

from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.initialization_messages import (
    AddressBookPayload,
    StartupPayload,
)
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.probe_messages import ProbeMessage

# from mTree.microeconomic_system.test import *


os.environ["PYTEST"] = "1"


class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return "actorAddress" in logrecord.__dict__


class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return "actorAddress" not in logrecord.__dict__


def simpleActorTestLogging():
    """This function returns a logging dictionary that can be passed as
    the logDefs argument for ActorSystem() initialization to get
    simple stdout logging configuration.  This is not necessary for
    typical unit testing that uses the simpleActorSystemBase, but
    it can be useful for multiproc.. ActorSystems where the
    separate processes created should have a very simple logging
    configuration.
    """
    import sys

    if sys.platform == "win32":
        # Windows will not allow sys.stdout to be passed to a child
        # process, which breaks the startup/config for some of the
        # tests.
        handler = {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "nosetests.log",
            "maxBytes": 256 * 1024,
            "backupCount": 3,
        }
    else:
        handler = {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        }
    return {
        "version": 1,
        "handlers": {  #'discarder': {'class': 'logging.NullHandler' },
            "testStream": handler,
        },
        "root": {"handlers": ["testStream"]},
        "disable_existing_loggers": False,
    }
    # logcfg = { 'version': 1,
    #        'formatters': {
    #            'normal': {'format': '%(levelname)-8s %(message)s'},
    #            'actor': {'format': '%(levelname)-8s %(actorAddress)s => %(message)s'}},
    #        'filters': { 'isActorLog': { '()': actorLogFilter},
    #                     'notActorLog': { '()': notActorLogFilter}},
    #        'handlers': { 'h1': {'class': 'logging.FileHandler',
    #                             'filename': 'example.log',
    #                             'formatter': 'normal',
    #                             'filters': ['notActorLog'],
    #                             'level': logging.INFO},
    #                      'h2': {'class': 'logging.FileHandler',
    #                             'filename': 'example.log',
    #                             'formatter': 'actor',
    #                             'filters': ['isActorLog'],
    #                             'level': logging.INFO},},
    #        'loggers' : { '': {'handlers': ['h1', 'h2'], 'level': logging.DEBUG}}
    #      }
    # return logcfg


testAdminPort = None


def get_free_admin_port_random():
    global testAdminPort
    if testAdminPort is None:
        import random

        # Reserved system ports are typically below 1024. Ephemeral
        # ports typically start at either 32768 (Linux) or 49152
        # (IANA), or range from 1024-5000 (older Windows).  Pick
        # something unused outside those ranges for the admin.
        testAdminPort = random.randint(10000, 30000)
        # testAdminPort = random.randint(5,60) * 1000
    else:
        testAdminPort = testAdminPort + 1
    return testAdminPort


def get_free_admin_port():
    import random
    import socket

    for tries in range(100):
        port = random.randint(5000, 30000)
        try:
            for m, p in [
                (socket.SOCK_STREAM, socket.IPPROTO_TCP),
                (socket.SOCK_DGRAM, socket.IPPROTO_UDP),
            ]:
                s = socket.socket(socket.AF_INET, m, p)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("", port))
                s.close()
            return port
        except Exception:
            pass
    return get_free_admin_port_random()


@pytest.fixture()
def actor_system(request):
    caps = {}
    caps["Admin Port"] = get_free_admin_port()

    asys = ActorSystem(  # systemBase='multiprocTCPBase',
        capabilities=caps, logDefs=simpleActorTestLogging()
    )

    def shutdown_actor_system():
        asys.shutdown()

    request.addfinalizer(shutdown_actor_system)
    return asys


def test_starting_agent(actor_system):
    agent = actor_system.createActor(Agent)
    # actor_system.shutdown()


def test_preparing_agent(actor_system):
    agent = actor_system.createActor(Agent)
    # Test the prepare sequence of three messages
    actor_system.tell(agent, "start")
    startup_payload = {}
    startup_payload["simulation_configuration"] = {}
    startup_payload["simulation_configuration"]["debug"] = ""
    startup_payload["simulation_configuration"]["log_level"] = ""
    startup_payload["properties"] = {}
    ### ADD LOCAL PROPERTIES
    startup_payload["container"] = ""
    startup_payload["address_type"] = "environment"
    startup_payload["simulation_id"] = "2"
    startup_payload["simulation_run_id"] = "2"
    # Fix here....
    startup_payload["short_name"] = "2"
    startup_payload["run_code"] = "2"
    startup_payload["status"] = "2"
    startup_payload["environment"] = "2"

    # if self.data_logging is not None:
    #     startup_payload["data_logging"] = self.data_logging

    # if self.run_number is not None:
    #     startup_payload["run_number"] = self.run_number
    startup_payload["log_actor"] = ""
    actor_system.tell(agent, StartupPayload(startup_payload=startup_payload))
    actor_system.tell(
        agent,
        AddressBookPayload(
            address_book_payload={
                "addresses": {},
                "address_groups": {},
                "addresses_to_groups": {},
                "agents": {},
                "institutions": {},
                "environment": "",
            }
        ),
    )

    probe = actor_system.ask(agent, ProbeMessage())
    assert type(probe) == ProbeMessage


### Test Agent
@directive_enabled_class
class TestAgent(Agent):
    @directive_decorator("respond_quickly")
    def respond_quickly(self, message: Message):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("response")
        self.send(message.sender, new_message)


def test_agent_new_directive(actor_system):
    agent = actor_system.createActor(TestAgent)
    # Test the prepare sequence of three messages
    actor_system.tell(agent, "start")

    startup_payload = {}
    startup_payload["simulation_configuration"] = {}
    startup_payload["simulation_configuration"]["debug"] = ""
    startup_payload["simulation_configuration"]["log_level"] = ""
    startup_payload["properties"] = {}
    ### ADD LOCAL PROPERTIES
    startup_payload["container"] = ""
    startup_payload["address_type"] = "environment"
    startup_payload["simulation_id"] = "2"
    startup_payload["simulation_run_id"] = "2"
    # Fix here....
    startup_payload["short_name"] = "2"
    startup_payload["run_code"] = "2"
    startup_payload["status"] = "2"
    startup_payload["environment"] = "2"

    # if self.data_logging is not None:
    #     startup_payload["data_logging"] = self.data_logging

    # if self.run_number is not None:
    #     startup_payload["run_number"] = self.run_number
    startup_payload["log_actor"] = ""
    actor_system.tell(agent, StartupPayload(startup_payload=startup_payload))
    actor_system.tell(
        agent,
        AddressBookPayload(
            address_book_payload={
                "addresses": {},
                "address_groups": {},
                "addresses_to_groups": {},
                "agents": {},
                "institutions": {},
                "environment": "",
            }
        ),
    )
    new_message = Message()
    new_message.set_directive("respond_quickly")

    response_message = actor_system.ask(agent, new_message)

    assert response_message.directive == "response"


### Test Agent
@directive_enabled_class
class TestRemindAgent(Agent):
    @directive_decorator("respond")
    def respond(self, message: Message):
        new_message = message
        new_message.set_directive("respond_slowly")
        new_message.set_payload({"return_address": new_message.sender})
        self.reminder(2, new_message)

    @directive_decorator("respond_slowly")
    def respond_slowly(self, message: Message):
        new_message = Message()
        new_message.set_sender(self.myAddress)
        new_message.set_directive("response")
        self.send(message.get_payload()["return_address"], new_message)


def test_agent_directive_with_remind(actor_system):
    agent = actor_system.createActor(TestRemindAgent)
    # Test the prepare sequence of three messages
    actor_system.tell(agent, "start")

    startup_payload = {}
    startup_payload["simulation_configuration"] = {}
    startup_payload["simulation_configuration"]["debug"] = ""
    startup_payload["simulation_configuration"]["log_level"] = ""
    startup_payload["properties"] = {}
    ### ADD LOCAL PROPERTIES
    startup_payload["container"] = ""
    startup_payload["address_type"] = "environment"
    startup_payload["simulation_id"] = "2"
    startup_payload["simulation_run_id"] = "2"
    # Fix here....
    startup_payload["short_name"] = "2"
    startup_payload["run_code"] = "2"
    startup_payload["status"] = "2"
    startup_payload["environment"] = "2"

    # if self.data_logging is not None:
    #     startup_payload["data_logging"] = self.data_logging

    # if self.run_number is not None:
    #     startup_payload["run_number"] = self.run_number
    startup_payload["log_actor"] = ""
    actor_system.tell(agent, StartupPayload(startup_payload=startup_payload))
    actor_system.tell(
        agent,
        AddressBookPayload(
            address_book_payload={
                "addresses": {},
                "address_groups": {},
                "addresses_to_groups": {},
                "agents": {},
                "institutions": {},
                "environment": "",
            }
        ),
    )
    new_message = Message()
    new_message.set_directive("respond")
    actor_system.tell(agent, new_message)
    response_message = actor_system.listen(10)

    assert response_message.directive == "response"
