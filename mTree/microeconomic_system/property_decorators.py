from types import FunctionType
from jsonschema import validate
from mTree.components import registry


def mtree_property(**kwargs):
    def wrapper_do_twice(func):
        if "mtree_properties" not in dir(func):
            func.mtree_properties = {}
        for property in kwargs.keys():
            func.mtree_properties[property] = kwargs[property]
        return func
    return wrapper_do_twice


def global_property(property_nane):
    def global_property_decorator(func):
        func.message_directive = property_nane
        return func
    return global_property_decorator

