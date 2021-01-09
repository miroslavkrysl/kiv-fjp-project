from abc import abstractmethod, ABC
from typing import List, Optional, Tuple


class Descriptor:
    @abstractmethod
    def utf8(self) -> str:
        pass

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __hash__(self):
        return hash(self.__class__)


class FieldDescriptor(Descriptor, ABC):
    pass


class SimpleFieldDescriptor(FieldDescriptor, ABC):
    pass


class ByteDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'B'

    def __str__(self):
        return 'byte'


class CharDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'C'

    def __str__(self):
        return 'char'


class DoubleDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'D'

    def __str__(self):
        return 'double'


class FloatDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'F'

    def __str__(self):
        return 'float'


class IntDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'I'

    def __str__(self):
        return 'int'


class LongDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'J'

    def __str__(self):
        return 'long'


class InstanceDesc(SimpleFieldDescriptor):
    def __init__(self, class_name: str):
        self._class_name = class_name

    def utf8(self) -> str:
        return 'L{0};'.format(self._class_name)

    def __str__(self):
        return self._class_name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._class_name == other._class_name

    def __hash__(self):
        return hash(self._class_name)


class ShortDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'S'

    def __str__(self):
        return 'short'


class BooleanDesc(SimpleFieldDescriptor):

    def utf8(self) -> str:
        return 'Z'

    def __str__(self):
        return 'boolean'


class ArrayDesc(FieldDescriptor):
    def __init__(self, dim, descriptor):
        assert 1 <= dim <= 255
        self._dim: int = dim
        self._descriptor: SimpleFieldDescriptor = descriptor

    @property
    def dim(self):
        return self._dim

    @property
    def descriptor(self):
        return self._descriptor

    def utf8(self) -> str:
        return self._dim * '[' + self._descriptor.utf8()

    def __str__(self):
        return "{0}{1}".format(self._descriptor, (self._dim * '[]'))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._dim == other._dim and self._descriptor == other._descriptor

    def __hash__(self):
        return hash((self._dim, self._descriptor))


class MethodDescriptor(Descriptor):

    def __init__(self, params_descriptor, return_descriptor):
        self._params: Tuple[FieldDescriptor] = params_descriptor
        self._ret: Optional[FieldDescriptor] = return_descriptor

    @property
    def params(self):
        return self._params

    @property
    def ret(self):
        return self._ret

    def utf8(self) -> str:
        return '({0}){1}'.format(''.join(map(lambda d: d.utf8(), self._params)),
                                 self._ret.utf8())

    def __str__(self):
        return '{0} ({1})'.format(self._ret, ', '.join(map(lambda p: str(p), self._params)))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._params == other._params and self._ret == other._ret

    def __hash__(self):
        return hash((self._params, self._ret))
