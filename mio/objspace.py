# Module:   objspace
# Date:     8th September 2014
# Author:   James Mills, prologic at shortcircuit dot net dot au


"""Object Space"""


from mio.model import Object, Message, String


class ObjectSpace(object):

    def __init__(self):
        self.object = Object(self)
        self.root = Object(self)

        self.message = Message(self, None)
        self.string = String(self, "")
