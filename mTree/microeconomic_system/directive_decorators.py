from types import FunctionType
from jsonschema import validate
from mTree.components import registry

def directive_decorator(directive_name, message_schema=None, message_callback=None, ui_callback=None):
    def real_decorator(func):
        func.message_directive = directive_name
        if message_schema is not None:
            func.message_schema = message_schema
        return func
    return real_decorator

def message_source(message_name):
    def real_decorator(func):
        func.message_source = message_name
        return func
    return real_decorator



from functools import wraps

def dec(msg='default'):
    def decorator(klass):
        old_foo = klass.foo
        @wraps(klass.foo)
        def decorated_foo(self, *args ,**kwargs):
            print('@decorator pre %s' % msg)
            old_foo(self, *args, **kwargs)
            print('@decorator post %s' % msg)
        klass.foo = decorated_foo
        return klass
    return decorator


def directive_enabled_class(cls):
    functions = [attr for attr in vars(cls).values() if isinstance(attr, FunctionType)]
    component_registry = registry.Registry()

    cls._enabled_directives = {}
    cls._enabled_directives_schemas = {}
    cls._mtree_properties = {}
    cls._message_sources = {}
    for func in functions:
        if getattr(func, "message_directive", False):
            cls._enabled_directives[getattr(func, "message_directive")] = func
        if getattr(func, "message_source", False):
            cls._message_sources[getattr(func, "message_source")] = func
        if getattr(func, "mtree_properties", False):
            for property_name in getattr(func, "mtree_properties").keys():
                cls._mtree_properties[property_name] = getattr(func, "mtree_properties")[property_name]
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
