from ..registry import registry

from .object import Object


class Builtins(Object):
    """Builtins"""


@registry.register("builtins", "")
def noop(space, receiver, context, message):
    """NoOp Message"""


@registry.register("builtins")
def setattr(space, receiver, context, message):
    """Set an attribute on the receiver"""
