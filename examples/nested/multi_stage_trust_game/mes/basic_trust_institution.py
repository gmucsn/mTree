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
class TrustInstitution(Institution):
    def prepare_trust_game(self):
        self.multiplier = 3
        self.groups_remaining = None
        self.rounds_remaining = 10


    @directive_decorator("start_trust")
    def start_trust(self, message:Message):
        if message.get_payload()is not None:            
            self.prepare_trust_game()
            temp_address_book = message.get_payload()["address_book"]
            self.address_book.merge_addresses(temp_address_book)
        else:
            self.address_book.reset_address_groups()
            

        if self.rounds_remaining > 0:
            self.rounds_remaining -= 1

            # code for making groups
            agents = self.address_book.select_addresses({"address_type": "agent"})
            for i in range(0, len(agents), 2): # get pairs of agents in order
                group_name = self.address_book.create_address_group()
                self.address_book.add_address_to_group(group_name, agents[i])
                self.address_book.add_address_to_group(group_name, agents[i+1])
            
            self.groups_remaining = len(self.address_book.get_all_groups())

            for group in self.address_book.get_all_groups():
                group_members = group[1]
                sender = group_members[0]
                receiver = group_members[1]

                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_payload({"group_name": group[0]})
                new_message.set_directive("make_sender")
                self.send(sender["address"], new_message)  
        
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_payload({"group_name": group[0]})
                new_message.set_directive("make_receiver")
                self.send(receiver["address"], new_message)  
    
    @directive_decorator("send_amount")
    def send_amount(self, message:Message):
        group_name = message.get_payload()["group_name"]
        amount_sent = message.get_payload()["send_amount"]
        multiplied = amount_sent * self.multiplier
        
        receiver = self.address_book.address_groups[group_name][1]

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_payload({"multiplied_amount": multiplied})
        new_message.set_directive("allocate_receiving")
        self.send(receiver["address"], new_message)  
        

    @directive_decorator("split_amount")
    def split_amount(self, message:Message):
        group_name = message.get_payload()["group_name"]
        return_amount = message.get_payload()["return_amount"]
        keep_amount = message.get_payload()["keep_amount"]
        
        sender = self.address_book.address_groups[group_name][0]    
        receiver = self.address_book.address_groups[group_name][1]

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_payload({"return_amount": return_amount})
        new_message.set_directive("allocate_sender_split")
        self.send(sender["address"], new_message)  

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_payload({"keep_amount": keep_amount})
        new_message.set_directive("allocate_receiver_split")
        self.send(receiver["address"], new_message)
        
        self.groups_remaining -= 1
        self.log_message("groups " + str(self.groups_remaining))
        if self.groups_remaining == 0:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("start_trust")
            self.send(self.myAddress, new_message)