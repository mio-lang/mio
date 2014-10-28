from rpython.rlib.objectmodel import compute_unique_id


from ..registry import Registry


class W_Object(object):

    registry = Registry()

    def __init__(self, space, parent=None):
        self.space = space
        self.parent = parent

        self.attrs = {}

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__ and
            self.__dict__ == other.__dict__
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.repr()

    def __str__(self):
        return self.str()

    def repr(self):
        return "<%s attrs=%s>" % (self.type(), self.attrs.keys())

    def str(self):
        return self.repr()

    def bool(self):
        return True

    def cmp(self, other):
        id1 = self.id()
        id2 = other.id()

        if id1 == id2:
            return 0
        return -1 if id1 < id2 else 1

    def hash(self):
        return sum(map(hash, self.attrs + [self.parent]))

    def id(self):
        return compute_unique_id(self)

    def type(self):
        return self.__class__.__name__[2:]

    def lookup(self, name):
        try:
            return self.attrs[name]
        except KeyError:
            if self.parent is not None:
                return self.parent.lookup(name)

    def call(self, space, receiver, context, message):
        return self

    def clone(self):
        return W_Object(self.space, self)

    def eval(self, space, receiver, context=None):
        return self

    @registry.register("clone")
    def m_clone(self, space, receiver, context, message):
        """Create a new Object by cloning the receiver"""

        assert isinstance(receiver, W_Object)

        return receiver.clone()

    @registry.register("do")
    def m_do(self, space, receiver, context, message):
        """Evaluate the expression"""

        assert len(message.args) == 1

        args = message.args
        args[0].eval(space, receiver)

        return receiver

    @registry.register("type")
    def m_type(self, space, receiver, context, message):
        """Returns Object Type"""

        return self.space.string.clone_and_init(receiver.type())

    @registry.register("parent")
    def m_parent(self, space, receiver, context, message):
        """Returns Parent Object"""

        parent = receiver.parent
        if parent is not None:
            return parent
        return self.space.null

    @registry.register("del")
    def m_del(self, space, receiver, context, message):
        """Delete an attribute"""

        assert len(message.args) == 1

        args = message.args
        name = args[0].eval(space, context).str()

        if name in receiver.attrs:
            del receiver.attrs[name]
        return space.object

    @registry.register("get")
    def m_get(self, space, receiver, context, message):
        """Get an attribute"""

        assert len(message.args) == 1

        args = message.args
        name = args[0].eval(space, context).str()

        if name in receiver.attrs:
            return receiver.attrs[name]
        return space.object

    @registry.register("set")
    def m_set(self, space, receiver, context, message):
        """Set an attribute"""

        assert len(message.args) == 2

        args = message.args
        name = args[0].eval(space, context).str()
        value = args[1].eval(space, context)

        receiver.attrs[name] = value

        return value

    @registry.register("has")
    def m_has(self, space, receiver, context, message):
        """Test if an object has an attribute"""

        assert len(message.args) == 1

        args = message.args
        name = args[0].eval(space, context).str()

        if name in receiver.attrs:
            return self.space.true
        return self.space.false

    @registry.register("cmp")
    def m_cmp(self, space, receiver, context, message):
        """Compare objects"""

        assert len(message.args) == 1

        args = message.args
        other = args[0].eval(space, context)

        return self.space.integer.clone_and_init(receiver.cmp(other))
