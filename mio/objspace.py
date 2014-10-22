# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from .objects import Object, Builtins, Number, Integer, Float, String


class ObjectSpace(object):

    def __init__(self):
        self.root = Object(self)
        self.object = Object(self)
        self.object.registry.populate(self.object, self)

        self.builtins = Builtins(self)
        self.builtins.registry.populate(self.builtins, self)

        self.number = Number(self)
        self.number.registry.populate(self.number, self)

        self.integer = Integer(self)
        self.integer.registry.populate(self.integer, self)

        self.float = Float(self)
        self.float.registry.populate(self.float, self)

        self.string = String(self)
        self.string.registry.populate(self.string, self)

        self.root.attrs.update({
            "Root": self.root,
            "Object": self.object,

            "Float": self.float,
            "Number": self.number,
            "Integer": self.integer,

            "String": self.string,

            "__builtins__": self.builtins,
        })
