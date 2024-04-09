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
class SecondPriceAuctionInstitution(Institution):
    def prepare_auction(self):
        self.num_auctions_remaining = 10

        self.min_item_value = 20
        self.max_item_value = 45


        self.common_value = None
        self.error = 4

        self.value_estimate = None

        self.bids = []

    @directive_decorator("start_auction")
    def start_auction(self, message:Message):
        if message.get_payload()is not None:            
            self.prepare_auction()
            temp_address_book = message.get_payload()["address_book"]
            self.address_book.merge_addresses(temp_address_book)
        else:
            self.address_book.reset_address_groups()

        self.log_message("Starting auction..." + str(self.num_auctions_remaining))
        if self.num_auctions_remaining > 0:
            self.num_auctions_remaining -= 1

            self.common_value = random.randint(self.min_item_value, self.max_item_value)

            self.bids = []
            self.start_bidding()

    def start_bidding(self):
        agents = self.address_book.select_addresses({"address_type": "agent"})
        for agent in agents:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("start_bidding")
            value_estimate = random.uniform(self.common_value - self.error, self.common_value + self.error)
            new_message.set_payload({"value_estimate": value_estimate, "error": self.error})
            self.send(agent, new_message)

    @directive_decorator("bid_for_item")
    def bid_for_item(self, message: Message):
        bidder = message.get_sender()
        bid = int(message.get_payload()["bid"])
            
        self.bids.append((bidder, bid))

        if len(self.bids) == len(self.address_book.select_addresses({"address_type": "agent"})):
            self.complete_auction()

    def complete_auction(self):
        
        bids = sorted(self.bids, key=lambda elem: elem[1] ,reverse=True)

        winner = bids.pop(0)
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("auction_result")
        second_price = bids[0][1]
        new_message.set_payload({"status": "winner", "price": second_price, "common_value": self.common_value})

        self.send(winner[0], new_message)  # receiver_of_message, message

        for agent in bids:
            new_message = Message()  # declare message
            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
            new_message.set_directive("auction_result")
            new_message.set_payload({"status": "loser"})
            self.send(agent[0], new_message)  # receiver_of_message, message

        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("start_auction")
        self.send(self.myAddress, new_message)  # receiver_of_message, message