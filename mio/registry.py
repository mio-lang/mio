from functools import wraps


class Registry(object):

    def __init__(self):
        self.attrs = {}

    def register(self, name):
        def wrapper(f):
            @wraps(f)
            def wrapped(*args):
                return f(*args)

            self.attrs[name] = wrapped

            return wrapped

        return wrapper

    def populate(self, obj, space):
        from mio.objects.cfunction import W_CFunction
        for name, func in self.attrs.iteritems():
            obj.attrs[name] = W_CFunction(space, name, func)
