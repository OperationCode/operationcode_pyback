from typing import NamedTuple
from functools import wraps

ResponseContainer = NamedTuple('ResponseContainer', [('route', str), ('method', str), ('payload', dict)])
"""
container for holding the pre-sent api requests
"""


"""
:param module_keys: string keys for the dict of required api variables
:type module_keys: list
:param module_dict: current dict for the imported module
:type module_dict:  dict
:param module_name: text string of the module for error messages
:type module_name: string
:return: wrapped function
:rtype: function
"""

def verify_module_variable(module_keys, module_dict, module_name):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for item in module_keys:
                try:
                    module_dict[item]
                except KeyError as error:
                    raise Exception(f"missing required API value for {item} for use in {module_name}")
            return func(*args, **kwargs)

        return wrapper

    return decorator
