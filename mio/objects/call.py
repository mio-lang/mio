from .object import Object


class Call(Object):

    def __init__(self, space, receiver, context, message, parent=None):
        Object.__init__(self, space, parent=(parent or space.object))

        self.receiver = receiver
        self.context = context
        self.message = message

    def clone(self):
        return Call(
            self.space, self.receiver, self.context, self.message, parent=self
        )

    def clone_and_init(self, receiver, context, message):
        return Call(
            self.space, receiver, context, message, parent=self
        )
