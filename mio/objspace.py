# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from .objects import Object, Builtins, Message, Method, Number, String


class ObjectSpace(object):

    def __init__(self):
        self.object = Object(self)
        self.root = Object(self)

        self.builtins = Builtins(self)

        self.root.attrs.update({
            "__builtins__": self.builtins,
            "Object": self.object,
            "Root": self.root,

            "Message": Message(self),
            "Method": Method(self),
            "Number": Number(self),
            "String": String(self),
        })
