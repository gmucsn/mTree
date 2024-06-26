from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random
import logging
import time
import datetime

@directive_enabled_class
class TrustAgent(Agent):
    def prepare_agent(self):
        self.endowment = None
        self.institution = None
        self.group_name = None
        self.role = None
        self.split_amount = None
        
    @directive_decorator("set_endowment")
    def set_endowment(self, message: Message):
        self.prepare_agent()
        self.endowment = message.get_payload()["endowment"]
        
    @directive_decorator("make_sender")
    def set_endowmake_senderment(self, message: Message):
        self.group_name = message.get_payload()["group_name"]
        self.institution = message.get_sender()
        self.role = "sender"
        self.decide_split()
        

    @directive_decorator("make_receiver")
    def make_receiver(self, message: Message):
        self.group_name = message.get_payload()["group_name"]
        self.institution = message.get_sender()
        self.role = "receiver"
        

    def decide_split(self):
        self.split_amount = random.randint(0, self.endowment)
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("send_amount")
        new_message.set_payload({"send_amount": self.split_amount, "group_name": self.group_name})
        self.send(self.institution, new_message)  
    
    @directive_decorator("allocate_receiving")
    def allocate_receiving(self, message: Message):
        multiplied_amount = message.get_payload()["multiplied_amount"]
        return_amount = random.randint(0, multiplied_amount)
        keep_amount = multiplied_amount - return_amount

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("split_amount")
        new_message.set_payload({"return_amount": return_amount, "keep_amount": keep_amount, "group_name": self.group_name})
        self.send(self.institution, new_message)  
        
    
    @directive_decorator("allocate_sender_split")
    def allocate_sender_split(self, message: Message):
        return_amount = message.get_payload()["return_amount"]
        self.endowment += return_amount
        self.log_message("New Endowment: " + str(self.endowment) + " Return Amount: " + str(return_amount))

    @directive_decorator("allocate_receiver_split")
    def allocate_receiver_split(self, message: Message):
        keep_amount = message.get_payload()["keep_amount"]
        self.endowment += keep_amount
        self.log_message("New Endowment: " + str(self.endowment) + " Keep Amount: " + str(keep_amount))
        
    