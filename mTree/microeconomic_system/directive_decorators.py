from types import FunctionType
from mTree.components import registry

def directive_decorator(directive_name):
    def real_decorator(func):
        func.message_directive = directive_name
        return func
    return real_decorator


def directive_enabled_class(cls):
    functions = [attr for attr in vars(cls).values() if isinstance(attr, FunctionType)]
    component_registry = registry.Registry()
    component_registry.add_class(cls)
    cls._enabled_directives = {}
    for func in functions:
        if getattr(func, "message_directive", False):
            cls._enabled_directives[getattr(func, "message_directive")] = func


    # now we register directives from the base class
    for base in cls.__bases__:
        functions = [attr for attr in vars(base).values() if isinstance(attr, FunctionType)]
        for func in functions:
            if getattr(func, "message_directive", False):
                cls._enabled_directives[getattr(func, "message_directive")] = func

    return cls
