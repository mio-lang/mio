from .object import Object


class Locals(Object):

    def __init__(self, space, receiver, context, message, method, parent=None):
        Object.__init__(self, space, parent=(parent or space.object))

        self.receiver = receiver
        self.context = context
        self.message = message
        self.method = method

        if self.method is not None:
            self.update_args()
            self.update_call()

    def clone(self):
        return Locals(
            self.space, self.receiver, self.context,
            self.message, self.method, parent=self
        )

    def clone_and_init(self, receiver, context, message, method, parent):
        return Locals(
            self.space, receiver, context, message, method, parent=parent
        )

    def update_args(self):
        for i in xrange(len(self.method.args)):
            if i < len(self.message.args):
                name = self.method.args[i].name
                value = self.message.args[i].eval(self.space, self.context)
                self.attrs[name] = value

    def update_call(self):
        self.attrs["call"] = self.space.call.clone_and_init(
            self.receiver, self.context, self.message
        )
