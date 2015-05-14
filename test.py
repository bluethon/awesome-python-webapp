import functools

class _Con(object):
    def __enter__(self):
        print "enter"
        #return self

    def __exit__(self, exctype, excvalue, traceback):
        print "exit"

def connection():
    return _Con()

def with_connection(func):
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)
    return _wrapper()

@with_connection
def test():
    print "test"

t = test()

t
