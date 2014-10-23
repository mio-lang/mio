from ..registry import Registry

from .object import W_Object


class W_Null(W_Object):

    registry = Registry()

    def repr(self):
        return "Null"
