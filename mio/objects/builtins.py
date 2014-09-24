from ..registry import Registry


from .method import Method
from .object import Object
from .message import Message


class Builtins(Object):
    """Builtins"""

    registry = Registry()

    @registry.register("")
    def null(self, space, receiver, context, message):
        """Null Message"""

        return context

    @registry.register()
    def delete(self, space, receiver, context, message):
        """Delete an attribute on the receiver"""

        assert len(message.args) == 1

        args = message.args
        name = args[0].eval(space, context, context).str()

        if name in receiver.attrs:
            del receiver.attrs[name]

        return receiver

    @registry.register()
    def get(self, space, receiver, context, message):
        """Get an attribute on the receiver"""

        assert len(message.args) == 1

        args = message.args
        name = args[0].eval(space, context, context).str()

        if name in receiver.attrs:
            return receiver.attrs[name]

        return receiver

    @registry.register()
    def set(self, space, receiver, context, message):
        """Set an attribute on the receiver"""

        assert len(message.args) == 2

        args = message.args
        name = args[0].eval(space, context, context).str()
        value = args[1]

        receiver.attrs[name] = value

        return receiver

    @registry.register("print")
    def c_print(self, space, receiver, context, message):
        """Print to standard output"""

        args = []
        for arg in message.args:
            if isinstance(arg, Message):
                args.append(arg.eval(space, context, context).str())
            else:
                args.append(arg.str())

        print " ".join(args)

        return receiver

    @registry.register()
    def method(self, space, receiver, context, message):
        """Creates a new Method object"""

        assert len(message.args) >= 1

        body = message.args[-1]
        args = message.args[:-1] if len(message.args) > 1 else []

        return Method(space, body, args=args)

        return receiver
