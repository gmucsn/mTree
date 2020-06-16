from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import logging
import random

EXPERIMENT = 25

@directive_enabled_class
class BasicEnvironment(Environment):
    def __init__(self):
        pass