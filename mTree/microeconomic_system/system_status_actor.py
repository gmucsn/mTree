from thespian.actors import *
import logging
from mTree.microeconomic_system.admin_message import AdminMessage
from thespian.initmsgs import initializing_messages

@initializing_messages([('starting', str)], initdone='init_done')
class SystemStatusActor(Actor):
    def init_done(self):
        self.running = False
        self.sa_running = False
        logging.info('SourceAuthority-Requested????')
        # if not(hasattr(self, 'sa_running')):
        #     print("Motto is there")
        if not self.sa_running:
            logging.info('Running SourceAuthority-Requested')
            self.registerSourceAuthority()
            self.sa_running = True            


    def system_status(self, sender):
        self.send(sender, self.running)

    def receiveMessage(self, msg, sender):      
        logging.info("SSA received a message")
        logging.info(msg)
        
        if not isinstance(msg, ActorSystemMessage): 
            
            if isinstance(msg, AdminMessage):
                if msg.get_request() == "register_dispatcher":
                    self.running = True
                elif msg.get_request() == "system_running":
                    logging.info('System running info requested...')
                    self.system_status(sender)       
                elif msg.get_request() == "start_source_authority":
                    pass
                    # logging.info('SourceAuthority-Requested????')
                    # # if not(hasattr(self, 'sa_running')):
                    # #     print("Motto is there")
                    # if not self.sa_running:
                    #     logging.info('Running SourceAuthority-Requested')
                    #     self.registerSourceAuthority()
                    #     self.sa_running = True  
        elif isinstance(msg, ValidateSource):
                self.send(sender, ValidatedSource(msg.sourceHash,
                                            msg.sourceData,
                                            msg.sourceInfo))
          