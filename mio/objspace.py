# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from .objects import (
    Object, Call, Locals, Method, Builtins,
    Boolean, Null, Number, Integer, Float, String
)


class ObjectSpace(object):

    def __init__(self):
        self.object = Object(self)
        self.object.registry.populate(self.object, self)

        self.root = self.object.clone()

        self.call = Call(self, None, None, None)
        self.call.registry.populate(self.call, self)

        self.locals = Locals(self, None, None, None, None)
        self.locals.registry.populate(self.locals, self)

        self.method = Method(self)
        self.method.registry.populate(self.method, self)

        self.builtins = Builtins(self)
        self.builtins.registry.populate(self.builtins, self)

        self.null = Null(self)
        self.null.registry.populate(self.null, self)

        self.true = Boolean(self, True)
        self.true.registry.populate(self.true, self)

        self.false = Boolean(self, True)
        self.false.registry.populate(self.false, self)

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

            "Null": self.null,
            "True": self.true,
            "False": self.false,

            "Float": self.float,
            "Number": self.number,
            "Integer": self.integer,

            "String": self.string,

            "Call": self.call,
            "Locals": self.locals,
            "Method": self.method,

            "__builtins__": self.builtins,
        })
