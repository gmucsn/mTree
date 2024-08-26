import logging
import time, datetime
from thespian.actors import *
# from mTree.microeconomic_system.test import *


import unittest
import pytest
import logging
import time
from thespian.actors import ActorSystem

from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.initialization_messages import StartupPayload, AddressBookPayload
from mTree.microeconomic_system.probe_messages import ProbeMessage

import os
os.environ["PYTEST"] = "1"

class actorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' in logrecord.__dict__
class notActorLogFilter(logging.Filter):
    def filter(self, logrecord):
        return 'actorAddress' not in logrecord.__dict__

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
    if sys.platform == 'win32':
        # Windows will not allow sys.stdout to be passed to a child
        # process, which breaks the startup/config for some of the
        # tests.
        handler = { 'class': 'logging.handlers.RotatingFileHandler',
                    'filename': 'nosetests.log',
                    'maxBytes': 256*1024,
                    'backupCount':3,
        }
    else:
        handler = { 'class': 'logging.StreamHandler',
                    'stream': sys.stdout,
        }
    return {
        'version' : 1,
        'handlers': { #'discarder': {'class': 'logging.NullHandler' },
            'testStream' : handler,
        },
        'root': { 'handlers': ['testStream'] },
        'disable_existing_loggers': False,
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
        #testAdminPort = random.randint(5,60) * 1000
    else:
        testAdminPort = testAdminPort + 1
    return testAdminPort

def get_free_admin_port():
    import socket
    import random
    for tries in range(100):
        port = random.randint(5000, 30000)
        try:
            for m,p in [ (socket.SOCK_STREAM, socket.IPPROTO_TCP),
                         (socket.SOCK_DGRAM, socket.IPPROTO_UDP),
            ]:
                s = socket.socket(socket.AF_INET, m, p)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('',port))
                s.close()
            return port
        except Exception:
            pass
    return get_free_admin_port_random()

import inspect
import json



@pytest.fixture()
def asys():
    caps = {}
    caps['Admin Port'] = get_free_admin_port()
    
    asys = ActorSystem(systemBase='multiprocTCPBase',
        capabilities=caps, 
        logDefs=simpleActorTestLogging())
    return asys



class TestFuncSimpleActorOperations(object):
    def testCreateActorSystem(self, asys):
        pass

    def testStartingAgent(self, asys):
        agent = asys.createActor(Environment)
        asys.shutdown()

    # def testPreparingAgent(self, asys, capfd):
    #     agent = asys.createActor(Environment)
    #     # Test the prepare sequence of three messages
    #     asys.tell(agent, "start")
    #     startup_payload = StartupPayload(startup_payload={})
    #     asys.tell(agent, StartupPayload(startup_payload=startup_payload))
    #     asys.tell(agent, AddressBookPayload(address_book_payload=startup_payload))
    #     # print(caplog.messages)
    #     # print("(!*&$!(*@&$(*)))")
    #     # print("SLTKJ")
    #     # print(caplog.text)
    #     # print("ASKLFJ")
    #     probe = asys.ask(agent, ProbeMessage())
    #     print("(!*^&$@(*&))")
    #     print(probe)
    #     print("OIAEUWTOIUAETOIUs")
    #     asys.shutdown()
    #     assert type(probe) == ProbeMessage
    #     # print("asfkjl", caplog.messages, "aslkjfh")
    #     # print("&&&&")
    #     # print(captured.err)
    #     # print("Agent" in caplog.messages)

    # def testSimpleActorTell(self, asys):
    #     clooney = asys.createActor(Clooney)
    #     asys.tell(clooney, 'hello')
    #     time.sleep(0.02)  # allow tell to work before ActorSystem shutdown

    # def testSimpleActorTellAbort(self, asys):
    #     clooney = asys.createActor(Clooney)
    #     asys.tell(clooney, 'hello')
    #     # no waiting: attempt system shutdown immediately which may or
    #     # may not occur before clooney is fully greeted.

    # def testSimpleActorAsk(self, asys):
    #     clooney = asys.createActor(Clooney)
    #     r = asys.ask(clooney, 'hello', 3.5)
    #     assert r == 'Greetings.'

    # def testSimpleActorAskTimeout(self, asys):
    #     clooney = asys.createActor(Clooney)
    #     t1 = datetime.datetime.now()
    #     r = asys.ask(clooney, 'Silence!', 0.5)
    #     assert r == None
    #     # Could test that it waited the proper amount of time, but
    #     # that doesn't allow an ActorSystems that knows there will be
    #     # no response to run more quickly (e.g. simpleActorSystem).
    #     #
    #     # t2 = datetime.datetime.now()
    #     # self.assertGreaterEqual(t2 - t1, datetime.timedelta(microseconds=500*1000))

    # def testSendTupleToSelf(self, asys):
    #     hamlet = asys.createActor(Hamlet)
    #     r = asys.ask(hamlet, 'Alas, poor Yorick!', 3)
    #     assert r == 'That is the question.'