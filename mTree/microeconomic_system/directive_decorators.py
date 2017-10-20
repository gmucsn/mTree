from types import FunctionType

def directive_decorator(directive_name):
    def real_decorator(func):
        func.message_directive = directive_name
        return func
    return real_decorator


def directive_enabled_class(cls):
    functions = [attr for attr in vars(cls).values()
        if isinstance(attr, FunctionType)]

    cls._enabled_directives = {}
    for func in functions:
        if getattr(func, "message_directive", False):
            cls._enabled_directives[getattr(func, "message_directive")] = func

    return cls
