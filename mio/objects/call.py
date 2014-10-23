from ..registry import Registry


from .object import W_Object


class W_Call(W_Object):

    registry = Registry()

    def __init__(self, space, receiver, context, message, parent=None):
        W_Object.__init__(self, space, parent=(parent or space.object))

        self.receiver = receiver
        self.context = context
        self.message = message

    def clone(self):
        return W_Call(
            self.space, self.receiver, self.context, self.message, parent=self
        )

    def clone_and_init(self, receiver, context, message):
        return W_Call(
            self.space, receiver, context, message, parent=self
        )

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
