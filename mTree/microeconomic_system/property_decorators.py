from types import FunctionType
from jsonschema import validate
from mTree.components import registry


def global_property(property_nane):
    def global_property_decorator(func):
        func.message_directive = property_nane
        return func
    return global_property_decorator

