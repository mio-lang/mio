from ..registry import Registry


from .object import W_Object


class W_Continuation(W_Object):

    registry = Registry()

    def __init__(self, space, receiver, context, message, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.receiver = receiver
        self.context = context
        self.message = message

    def clone(self):
        return W_Continuation(
            self.space, self.receiver, self.context, self.message, parent=self
        )

    def clone_and_init(self, receiver, context, message):
        return W_Continuation(
            self.space, receiver, context, message, parent=self
        )

    def call(self, space, receiver, context, message):
        # Empty Message
        if self.message is None:
            return self

        return self.message.eval(space, self.receiver, self.context)

    @registry.register("call")
    def m_call(self, space, receiver, context, message):
        """Call Continuation"""

        return receiver.call(space, receiver, context, message)

    @registry.register("current")
    def m_current(self, space, receiver, context, message):
        """Create and Return a New Continuation Object"""

        assert isinstance(receiver, W_Continuation)
        return receiver.clone_and_init(receiver, context, message)

    @registry.register("receiver")
    def m_receiver(self, space, receiver, context, message):
        """Return receiver"""

        return self.receiver

    @registry.register("context")
    def m_context(self, space, receiver, context, message):
        """Return context"""

        return self.context

    @registry.register("message")
    def m_message(self, space, receiver, context, message):
        """Return message"""

        return self.message
