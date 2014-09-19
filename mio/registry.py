from functools import wraps


class Registry(object):

    def __init__(self):
        self.attrs = {}

    def register(self, alias=None):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args):
                return f(*args)

            if alias is None:
                name = f.__name__
            else:
                name = alias

            self.attrs[name] = wrapped

            return wrapped

        return wrapper

    def populate(self, obj, space):
        from mio.objects.cfunction import CFunction
        for name, func in self.attrs.iteritems():
            obj.attrs[name] = CFunction(space, name, func)
