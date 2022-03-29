from mTree.server.actor_system_startup import ActorSystemStartup
import os
import sys
from thespian.actors import *
import time
import socketio
from thespian.actors import *

os.environ['THESPLOG_THRESHOLD'] =  'DEBUG'
os.environ['THESPLOG_FILE'] =  os.path.join(os.getcwd(), "thespian.log")

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connected to server')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def hello(a, b, c):
    print(a, b, c)


from os import system, name
from thespian.actors import *


def clear():
    if name == 'nt':  # for windows
        system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        system('clear')


class MonitorClient:
    def __init__(self, handled_logging_levels):
        self.asys = ActorSystem(ACTOR_SYSTEM_BASE)
        self.match_maker_addr = self.asys.createActor(MatchMaker, globalName="MatchMaker")
        # self.game_manager_addr = self.asys.createActor(GameManager, globalName="GameManager")
        # self.logger_addr = self.asys.createActor(Logger, globalName="Logger")
        # self.m_tuples = []
        # self.handled_logging_levels = handled_logging_levels

    def start_monitoring(self):
        response = self.asys.ask(self.logger_addr, JoinMonitorMsg())
        if isinstance(response, MonitorJoinAcknowledgement):
            print("Succesfully joined logger")

        while True:
            print("Waiting for logging messages...")
            msg = self.asys.listen()
            if isinstance(msg, LogMsg):
                heapq.heappush(self.m_tuples, (msg.time.timestamp(), np.random.rand(), msg))
                clear()
                for msg_tuple in heapq.nsmallest(len(self.m_tuples), self.m_tuples, lambda m_tuple: m_tuple[0]):
                    msg = msg_tuple[2]
                    if msg.logging_level in self.handled_logging_levels:
                        print(msg)

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    
