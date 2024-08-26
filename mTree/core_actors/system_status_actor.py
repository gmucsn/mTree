from thespian.actors import *
import logging

from mTree.core_actors.admin_message import AdminMessage
from mTree.core_actors.actor_process_descriptor import ActorProcessDescriptor

from thespian.initmsgs import initializing_messages

import datetime
import setproctitle
import os
import psutil

@initializing_messages([("starting", str)], initdone="init_done")
class SystemStatusActor(Actor):

    def init_done(self):
        setproctitle.setproctitle("mTree - SystemStatusActor Actor")
        logging.info("System status actor starting!")

        self.actors = ["mTree - SystemStatusActor Actor"]
        self.pids = [os.getpid()]
        self.processes = []

        self.running = False
        self.sa_running = False
        # if not(hasattr(self, 'sa_running')):
        #     print("Motto is there")
        # if not self.sa_running:
        self.registerSourceAuthority()
        logging.info("STARTING STATUS ACTOR")
        self.sa_running = True

    def register_pid(self, msg):
        if msg.payload not in self.pids:
            self.pids.append(msg.payload)
        

    def generate_status_report(self, sender):
        processes = []
        for pid in self.pids:
            try:
                process = psutil.Process(pid)
                process_report = ActorProcessDescriptor(
                    actor_address = self.myAddress,
                    actor_name = process.name(),
                    status = process.status(),
                    pid = pid,
                    cpu_usage = process.cpu_percent(),
                    memory_usage = process.memory_full_info().rss,
                    started = datetime.datetime.fromtimestamp(process.create_time())
                )
                processes.append(process_report)
            except:
                process_report = ActorProcessDescriptor(
                    actor_address = "",
                    actor_name = "",
                    status = "DEAD",
                    pid = pid,
                    cpu_usage = "",
                    memory_usage = "",
                    started = ""
                )
                processes.append(process_report)
        self.send(sender, processes)




    def system_status(self, sender):
        self.send(sender, self.running)

    def get_status(self, sender):
        self.send(sender, self.processes)

    def receiveMessage(self, msg, sender):
        logging.info("STARTING STATUS ACTOR")
        logging.info("A MESSAGE -> ", msg)
        match msg:
            case AdminMessage():
                match msg.directive:
                    case "check_status":
                        self.generate_status_report(sender)
                    case "register_pid":
                        self.register_pid(msg)
            case ValidateSource():
                logging.info("A VALIDATION REQUEST HAS BEEN RECEIVED....")
                self.send(
                    sender, ValidatedSource(msg.sourceHash, msg.sourceData, msg.sourceInfo)
                )


        # if not isinstance(msg, ActorSystemMessage):
        #     if isinstance(msg, AdminMessage):
        #         if msg.directive == "check_status":
        #             self.generate_status_report(sender)
                
        #         # elif msg.get_request() == "register_dispatcher":
        #         #     self.running = True
        #         # elif msg.get_request() == "system_running":
        #         #     self.system_status(sender)
        #         # elif msg.get_request() == "start_source_authority":
        #         #     pass
        #             # logging.info('SourceAuthority-Requested????')
        #             # # if not(hasattr(self, 'sa_running')):
        #             # #     print("Motto is there")
        #             # if not self.sa_running:
        #             #     logging.info('Running SourceAuthority-Requested')
        #             #     self.registerSourceAuthority()
        #             #     self.sa_running = True
        # elif isinstance(msg, ValidateSource):
        #     self.send(
        #         sender, ValidatedSource(msg.sourceHash, msg.sourceData, msg.sourceInfo)
        #     )
