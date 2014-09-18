from ..registry import registry

from .object import Object
from .message import Message


class Builtins(Object):
    """Builtins"""


@registry.register("builtins", "")
def c_noop(space, receiver, context, message):
    """Null Message"""

    return context


@registry.register("builtins", "delattr")
def c_delattr(space, receiver, context, message):
    """Delete an attribute on the receiver"""

    assert len(message.args) == 1

    args = message.args
    name = args[0].eval(space, context, context).str()

    if name in receiver.attrs:
        del receiver.attrs[name]

    return receiver


@registry.register("builtins", "getattr")
def c_getattr(space, receiver, context, message):
    """Get an attribute on the receiver"""

    assert len(message.args) == 1

    args = message.args
    name = args[0].eval(space, context, context).str()

    if name in receiver.attrs:
        return receiver.attrs[name]

    return receiver


@registry.register("builtins", "setattr")
def c_setattr(space, receiver, context, message):
    """Set an attribute on the receiver"""

    assert len(message.args) == 2

    args = message.args
    name = args[0].eval(space, context, context).str()
    value = args[1].eval(space, context, context)

    receiver.attrs[name] = value

    return receiver


@registry.register("builtins", "print")
def c_print(space, receiver, context, message):
    """Print to standard output"""

    args = []
    for arg in message.args:
        if isinstance(arg, Message):
            args.append(arg.eval(space, context, context).str())
        else:
            args.append(arg.str())

    print " ".join(args)

    return receiver
