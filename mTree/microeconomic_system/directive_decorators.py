from types import FunctionType
from jsonschema import validate
from mTree.components import registry

def directive_decorator(directive_name, schema=None):
    def real_decorator(func):
        func.message_directive = directive_name
        if schema is not None:
            func.schema = schema
        return func
    return real_decorator


def directive_enabled_class(cls):
    functions = [attr for attr in vars(cls).values() if isinstance(attr, FunctionType)]
    component_registry = registry.Registry()

    cls._enabled_directives = {}
    cls._enabled_directives_schemas = {}
    for func in functions:
        if getattr(func, "message_directive", False):
            cls._enabled_directives[getattr(func, "message_directive")] = func
        if getattr(func, "schema", False):
            cls._enabled_directives_schemas[getattr(func, "message_directive")] = getattr(func, "schema")

    # now we register directives from the base class
    for base in cls.__bases__:
        functions = [attr for attr in vars(base).values() if isinstance(attr, FunctionType)]
        for func in functions:
            if getattr(func, "message_directive", False):
                cls._enabled_directives[getattr(func, "message_directive")] = func
            if getattr(func, "schema", False):
                cls._enabled_directives_schemas[getattr(func, "message_directive")] = getattr(func, "schema")
    component_registry.add_class(cls)

    return cls
