# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from .objects import Object, Builtins, Number, String


class ObjectSpace(object):

    def __init__(self):
        self.root = Object(self)
        self.object = Object(self)
        self.object.registry.populate(self.object, self)

        self.builtins = Builtins(self)
        self.builtins.registry.populate(self.builtins, self)

        self.number = Number(self)
        self.number.registry.populate(self.number, self)

        self.string = String(self)
        self.string.registry.populate(self.string, self)

        self.root.attrs.update({
            "__builtins__": self.builtins,
            "Object": self.object,
            "Root": self.root,
            "Number": self.number,
            "String": self.string
        })
