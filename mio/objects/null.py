from ..registry import Registry

from .object import Object


class Null(Object):

    registry = Registry()

    def repr(self):
        return "Null"
