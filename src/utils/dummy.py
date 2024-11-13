class DummyObject:
    """Dummy object, that has infinite attributes."""

    def __getattribute__(self, name):
        return DummyObject()

    def __getattr__(self, name):
        return DummyObject()

    def __call__(self, *args, **kwargs):
        return DummyObject()

    def __getitem__(self, key):
        return DummyObject()

    def __add__(self, other):
        return DummyObject()

    def __iadd__(self, other):
        return DummyObject()

    def __sub__(self, other):
        return DummyObject()

    def __isub__(self, other):
        return DummyObject()

    def __mul__(self, other):
        return DummyObject()

    def __imul__(self, other):
        return DummyObject()

    def __truediv__(self, other):
        return DummyObject()

    def __itruediv__(self, other):
        return DummyObject()

    def __floordiv__(self, other):
        return DummyObject()

    def __ifloordiv__(self, other):
        return DummyObject()

    def __mod__(self, other):
        return DummyObject()

    def __imod__(self, other):
        return DummyObject()

    def __pow__(self, other):
        return DummyObject()

    def __ipow__(self, other):
        return DummyObject()

    def __lshift__(self, other):
        return DummyObject()

    def __ilshift__(self, other):
        return DummyObject()

    def __rshift__(self, other):
        return DummyObject()

    def __irshift__(self, other):
        return DummyObject()

    def __and__(self, other):
        return DummyObject()

    def __iand__(self, other):
        return DummyObject()

    def __or__(self, other):
        return DummyObject()

    def __ior__(self, other):
        return DummyObject()

    def __xor__(self, other):
        return DummyObject()

    def __ixor__(self, other):
        return DummyObject()

    def __neg__(self):
        return DummyObject()

    def __pos__(self):
        return DummyObject()

    def __abs__(self):
        return DummyObject()

    def __invert__(self):
        return DummyObject()

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __eq__(self, other):
        return True

    def __ne__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __len__(self):
        return 0

    def __iter__(self):
        return [DummyObject()].__iter__()

    def __next__(self):
        return DummyObject()

    def __contains__(self, item):
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def __bool__(self):
        return True

    def __repr__(self):
        return "DummyObject()"

    def __str__(self):
        return "DummyObject()"

    def __hash__(self):
        return 0

    def __dir__(self):
        return []

    def __delattr__(self, name):
        return DummyObject()

    def __setattr__(self, name, value):
        return DummyObject()

    def __delitem__(self, key):
        return DummyObject()

    def __setitem__(self, key, value):
        return DummyObject()

    def __format__(self, format_spec):
        return "DummyObject()"

    def __index__(self):
        return 0

    def __copy__(self):
        return DummyObject()

    def __deepcopy__(self, memo):
        return DummyObject()

    def __reversed__(self):
        return DummyObject()

    def __await__(self):
        return DummyObject()

    def __aiter__(self):
        return [DummyObject()].__iter__()

    def __anext__(self):
        return DummyObject()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        return False