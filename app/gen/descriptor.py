from abc import abstractmethod, ABC
from typing import List, Optional

from app.types import BaseType


# --- Java operand types ---

class JOperandType(ABC):
    pass


class JOperandTypeInt(JOperandType):
    pass


class JOperandTypeLong(JOperandType):
    pass


class JOperandTypeFloat(JOperandType):
    pass


class JOperandTypeDouble(JOperandType):
    pass


class JOperandTypeReference(JOperandType):
    pass


# # --- Java names ---
#
# class ObjectName(ABC):
#     @abstractmethod
#     def utf8(self):
#         pass
#
#
# class ClassName(ObjectName):
#     def __init__(self, name: str):
#         self.name = name
#
#     def utf8(self):
#         return f'[L{self.name};'
#
#
# class FieldName:
#     def __init__(self, name: str):
#         self.name = name
#
#     def utf8(self):
#         return self.name
#
#
# class MethodName:
#     INIT_METHOD = '<init>'
#     CLASS_INIT_METHOD = '<clinit>'
#
#     def __init__(self, name: str):
#         self.name = name
#
#     @classmethod
#     def new_init(cls):
#         cls(cls.INIT_METHOD)
#
#     @classmethod
#     def new_class_init(cls):
#         cls(cls.CLASS_INIT_METHOD)
#
#     def utf8(self):
#         return self.name


# --- Java type descriptors ---

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


class BaseDescriptor(FieldDescriptor, ABC):
    pass


class ByteDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'B'

    def __str__(self):
        return 'byte'


class CharDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'C'

    def __str__(self):
        return 'char'


class DoubleDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'D'

    def __str__(self):
        return 'double'


class FloatDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'F'

    def __str__(self):
        return 'float'


class IntDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'I'

    def __str__(self):
        return 'int'


class LongDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'J'

    def __str__(self):
        return 'long'


class ObjectDesc(BaseDescriptor):
    def __init__(self, class_name: str):
        self._class_name = class_name

    @property
    def class_name(self):
        return self._class_name

    def utf8(self) -> str:
        return f'[L{self._class_name};'

    def __str__(self):
        return self._class_name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._class_name == other._class_name

    def __hash__(self):
        return hash(self._class_name)


class ShortDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'S'

    def __str__(self):
        return 'short'


class BooleanDesc(BaseDescriptor):

    def utf8(self) -> str:
        return 'Z'

    def __str__(self):
        return 'boolean'


class ArrayDesc(FieldDescriptor):
    def __init__(self, dim, inner):
        assert 1 <= dim <= 255
        self._dim: int = dim
        self._inner: BaseDescriptor = inner

    @property
    def dim(self):
        return self._dim

    @property
    def inner(self):
        return self._inner

    def utf8(self) -> str:
        return self._dim * '[' + self._inner.utf8()

    def __str__(self):
        return "{0}{1}".format(self._inner, (self._dim * '[]'))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._dim == other._dim and self._inner == other._inner

    def __hash__(self):
        return hash((self._dim, self._inner))


class MethodDescriptor(Descriptor):

    def __init__(self, params_descriptor: List[FieldDescriptor], return_descriptor: Optional[FieldDescriptor] = None):
        self._params_descriptors: List[FieldDescriptor] = params_descriptor
        self._return_descriptor: Optional[FieldDescriptor] = return_descriptor

    @property
    def params_descriptors(self):
        return self._params_descriptors

    @property
    def return_descriptor(self):
        return self._return_descriptor

    def utf8(self) -> str:
        return '({0}){1}'.format(''.join(map(lambda d: d.utf8(), self._params_descriptors)),
                                 self._return_descriptor.utf8())

    def __str__(self):
        return '{0} ({1})'.format(self._return_descriptor, ', '.join(map(lambda p: str(p), self._params_descriptors)))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self._params_descriptors == other._params_descriptors \
            and self._return_descriptor == other._return_descriptor

    def __hash__(self):
        return hash((self._params_descriptors, self._return_descriptor))
