import datetime
import logging
import math
import random
import time

from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.message import Message


@directive_enabled_class
class AuctionAgent(Agent):
    def prepare(self):
        self.endowment = None
        self.institution = None

        self.bid = None

        self.auction_history = []
        self.log_message("10 TESTING THIS...", target="trial", level=10)
        self.log_message("66 TESTING THIS...", target="trial", level=66)
        if self.debug:
            self.log_message("10 TESTING THIS...", level=10)
            self.log_message("DEBUG TESTING...")

        self.log_message("TESTING THIS...", target="trial")

    @directive_decorator("set_endowment")
    def set_endowment(self, message: Message):
        self.endowment = message.get_payload()["endowment"]

    @directive_decorator("start_bidding")
    def start_bidding(self, message: Message):
        self.log_message("Agent got auction start")
        self.value_estimate = message.get_payload()["value_estimate"]

        self.error = message.get_payload()["error"]
        self.institution = message.get_sender()
        self.make_bid()

    def make_bid(self):
        self.bid = self.value_estimate
        self.log_data({"bid": self.bid})

        new_message = Message()  # declare message
        new_message.set_sender(
            self.myAddress
        )  # set the sender of message to this actor
        new_message.set_directive("bid_for_item")
        new_message.set_payload({"bid": self.bid})
        self.send(self.institution, new_message)

    @directive_decorator("auction_result")
    def auction_result(self, message: Message):
        if message.get_payload()["status"] == "winner":
            common_value = message.get_payload()["common_value"]
            self.auction_history.append(("Win", self.bid, common_value))
        else:
            self.auction_history.append(("Loss", self.bid, 0))
