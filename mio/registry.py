from functools import wraps


from mio.objects.cfunction import CFunction


class Registry(object):

    def __init__(self):
        self.registry = {}

    def register(self, object, alias=None):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args):
                print "%s called with %s" % (f.__name__, args)
                return f(*args)

            if alias is None:
                name = f.__name__
            else:
                name = alias

            attrs = self.registry.setdefault(object, {})
            attrs[name] = wrapped

            return wrapped

        return wrapper

    def populate(self, space):
        print "populating:"
        for group, attrs in self.registry.iteritems():
            obj = getattr(space, group)
            if obj is not None:
                for name, func in attrs.iteritems():
                    obj.attrs[name] = CFunction(space, name, func)


registry = Registry()
