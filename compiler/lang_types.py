from abc import ABC


# --- Our language types

class Type(ABC):
    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.__class__)

    def is_array_any(self) -> bool:
        return isinstance(self, TypeArray) and self.inner == TypeAny()


class BaseType(Type):
    pass


class TypeInt(BaseType):
    def __repr__(self):
        return "<TypeInt>"

    def __str__(self):
        return "Int"


class TypeReal(BaseType):
    def __repr__(self):
        return "<TypeReal>"

    def __str__(self):
        return 'Real'


class TypeBool(BaseType):
    def __repr__(self):
        return "<TypeBool>"

    def __str__(self):
        return 'Bool'


class TypeStr(BaseType):
    def __repr__(self):
        return "<TypeStr>"

    def __str__(self):
        return 'Str'


class TypeAny(BaseType):
    def __repr__(self):
        return "<TypeAny>"

    def __str__(self):
        return 'Any'


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

    def __str__(self):
        return '[' * self._dim + str(self._inner) + ']' * self._dim

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
            and self.dim == other.dim \
            and (self.inner == other.inner or self.inner == TypeAny() or other.inner == TypeAny())

    def __hash__(self):
        return hash((self._dim, self._inner))


class TypeVoid(BaseType):
    def __repr__(self):
        return "<TypeVoid>"

    def __str__(self):
        return 'Void'
