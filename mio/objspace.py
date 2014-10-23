# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from .objects import (
    W_Object, W_Call, W_Locals, W_Method, W_Builtins,
    W_Boolean, W_Null, W_Number, W_Integer, W_Float, W_String
)


class ObjectSpace(object):

    def __init__(self):
        self.object = W_Object(self)
        self.object.registry.populate(self.object, self)

        self.root = self.object.clone()

        self.call = W_Call(self, None, None, None)
        self.call.registry.populate(self.call, self)

        self.locals = W_Locals(self, None, None, None, None)
        self.locals.registry.populate(self.locals, self)

        self.method = W_Method(self)
        self.method.registry.populate(self.method, self)

        self.builtins = W_Builtins(self)
        self.builtins.registry.populate(self.builtins, self)

        self.null = W_Null(self)
        self.null.registry.populate(self.null, self)

        self.true = W_Boolean(self, True)
        self.true.registry.populate(self.true, self)

        self.false = W_Boolean(self, False)
        self.false.registry.populate(self.false, self)

        self.number = W_Number(self)
        self.number.registry.populate(self.number, self)

        self.integer = W_Integer(self)
        self.integer.registry.populate(self.integer, self)

        self.float = W_Float(self)
        self.float.registry.populate(self.float, self)

        self.string = W_String(self)
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
