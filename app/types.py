from abc import ABC


# --- Our language types

class Type(ABC):
    pass


class BaseType(ABC):
    pass


class TypeInt(BaseType):
    def __repr__(self):
        return "<TypeInt>"


class TypeReal(BaseType):
    def __repr__(self):
        return "<TypeReal>"


class TypeBool(BaseType):
    def __repr__(self):
        return "<TypeBool>"


class TypeStr(BaseType):
    def __repr__(self):
        return "<TypeStr>"


class TypeArray(Type):

    def __init__(self, dim: int, inner: BaseType):
        self._dim = dim
        self._inner = inner

    @property
    def dim(self) -> int:
        return self._dim

    @property
    def inner(self) -> BaseType:
        return self._inner

    def __repr__(self):
        return f"<TypeArray(dim={self._dim}, inner={self._inner})>"
