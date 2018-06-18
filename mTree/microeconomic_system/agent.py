from thespian.actors import *
import numpy as np

from mTree.microeconomic_system.message_space import Message
from mTree.microeconomic_system.message_space import MessageSpace
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.directive_decorators import *


@directive_enabled_class
class Agent(Actor):
    def __init__(self):
        print("Agent started")

    def receiveMessage(self, message, sender):
        directive_handler = self._enabled_directives.get(message.get_directive())
        directive_handler(self, message)
