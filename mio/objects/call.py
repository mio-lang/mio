from .object import W_Object


class W_Call(W_Object):

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
