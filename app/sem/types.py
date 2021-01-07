from abc import ABC


class Type(ABC):
    pass


class SimpleType(Type, ABC):
    pass


class Int(SimpleType):
    pass


class Real(SimpleType):
    pass


class Bool(SimpleType):
    pass


class Str(SimpleType):
    pass


class Array:

    def __init__(self, inner: SimpleType, dim: int):
        self.inner = inner
        self.dim = dim
