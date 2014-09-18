from ..registry import registry

from .object import Object


class Builtins(Object):
    """Builtins"""


@registry.register("builtins", "")
def c_noop(space, receiver, context, message):
    """NoOp Message"""

    return receiver


@registry.register("builtins")
def c_delattr(space, receiver, context, message):
    """Delete an attribute on the receiver"""

    return receiver


@registry.register("builtins")
def c_getattr(space, receiver, context, message):
    """Get an attribute on the receiver"""

    return receiver


@registry.register("builtins")
def c_setattr(space, receiver, context, message):
    """Set an attribute on the receiver"""

    return receiver


@registry.register("builtins", "print")
def c_print(space, receiver, context, message):
    """Print to standard output"""

    args = []
    for arg in message.args:
        args.append(arg.eval(space, context, context).str())

    print " ".join(args)

    return receiver
