from ..registry import Registry

from .object import W_Object
from .message import W_Message


class W_Builtins(W_Object):
    """Builtins"""

    registry = Registry()

    @registry.register("print")
    def m_print(self, space, receiver, context, message):
        """Print to standard output"""

        args = []
        for arg in message.args:
            if isinstance(arg, W_Message):
                args.append(arg.eval(space, context).str())
            else:
                args.append(arg.str())

        print " ".join(args)

        return self.space.null

    @registry.register("method")
    def m_method(self, space, receiver, context, message):
        """Create a new bound Method Object"""

        args = message.args[:-1] if len(message.args) > 1 else []
        body = message.args[-1] if len(message.args) > 0 else None

        return self.space.method.clone_and_init(
            body, args=args, binding=receiver
        )

    @registry.register("block")
    def m_block(self, space, receiver, context, message):
        """Create a new unbound Method Object"""

        assert len(message.args) >= 1

        body = message.args[-1]
        args = message.args[:-1] if len(message.args) > 1 else []

        return self.space.method.clone_and_init(
            body, args=args, binding=context
        )

    @registry.register("bool")
    def m_bool(self, space, receiver, context, message):
        """Convert argument to a Boolean"""

        assert len(message.args) == 1

        args = message.args
        obj = args[0].eval(space, context)

        return self.space.true if obj.bool() else self.space.false

    @registry.register("not")
    def m_not(self, space, receiver, context, message):
        """Invert a Boolean"""

        assert len(message.args) == 1

        args = message.args
        obj = args[0].eval(space, context)

        return self.space.false if obj.bool() else self.space.true
