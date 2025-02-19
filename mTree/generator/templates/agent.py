import logging
import random

from mTree.microeconomic_system.agent import Agent
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message

EXPERIMENT = 25


@directive_enabled_class
class BasicAgent(Agent):
    def __init__(self):
        pass
