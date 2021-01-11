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
        self.dim = dim
        self.inner = inner

    def __repr__(self):
        return f"<TypeArray(dim={self.dim}, inner={self.inner})>"
