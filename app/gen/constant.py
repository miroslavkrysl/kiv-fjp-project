from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

from app.gen.descriptor import MethodDescriptor, FieldDescriptor, ArrayDesc, ClassDesc
from app.gen.util import is_int, is_long

class Tag(Enum):
    UTF8 = 1
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    CLASS = 7
    STRING = 8
    FIELD_REF = 9
    METHOD_REF = 10
    NAME_AND_TYPE = 12


class JConst(ABC):

    @abstractmethod
    def tag(self) -> Tag:
        pass


class JConstUtf8(JConst):
    def __init__(self, value: str):
        self.value = value

    def tag(self) -> Tag:
        return Tag.UTF8

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstInt(JConst):
    def __init__(self, value: int):
        assert is_int(value)
        self.value = value

    def tag(self) -> int:
        return Tag.INT

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstLong(JConst):
    def __init__(self, value: int):
        assert is_long(value)
        self.value = value

    def tag(self) -> Tag:
        return Tag.LONG

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstFloat(JConst):
    def __init__(self, value: float):
        self.value = value

    def tag(self) -> Tag:
        return Tag.FLOAT

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstDouble(JConst):
    def __init__(self, value: float):
        self.value = value

    def tag(self) -> Tag:
        return Tag.DOUBLE

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstString(JConst):
    def __init__(self, utf8_index: int):
        self.utf8_index = utf8_index

    def tag(self) -> Tag:
        return Tag.STRING

    def __hash__(self):
        return hash(self.utf8_index)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.utf8_index == other.utf8_index


class JConstClass(JConst):
    def tag(self) -> Tag:
        return Tag.CLASS

    def __init__(self, name_index: int):
        self.name_index = name_index

    def __hash__(self):
        return hash((self.name_index,))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.name_index == other.name_index


class JConstNameAndType(JConst):
    def __init__(self, name_index: int, descriptor_index: int):
        self.name_index = name_index
        self.descriptor_index = descriptor_index

    def tag(self) -> Tag:
        return Tag.NAME_AND_TYPE

    def __hash__(self):
        return hash((self.name_index, self.descriptor_index))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.name_index == other.name_index \
               and self.descriptor_index == other.descriptor_index


class JConstFieldRef(JConst):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def tag(self) -> Tag:
        return Tag.FIELD_REF

    def __hash__(self):
        return hash((self.class_index, self.name_and_type_index))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.class_index == other.class_index \
               and self.name_and_type_index == other.name_and_type_index


class JConstMethodRef(JConst):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def tag(self) -> Tag:
        return Tag.METHOD_REF

    def __hash__(self):
        return hash((self.class_index, self.name_and_type_index))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.class_index == other.class_index \
               and self.name_and_type_index == other.name_and_type_index


class ConstantPool:
    def __init__(self):
        self._constants: Dict[JConst, int] = {}

    def _add(self, const: JConst) -> int:
        index = self._constants.get(const)

        if index is None:
            index = len(self._constants) + 1    # constant pool is indexed from 1
            self._constants[const] = index

        return index

    @property
    def constants(self):
        return self._constants

    def utf8(self, value: str) -> int:
        return self._add(JConstUtf8(value))

    def class_ref(self, class_name: str) -> int:
        class_name = ClassDesc(class_name)
        name_index = self.utf8(class_name.utf8())
        class_index = self._add(JConstClass(name_index))
        return class_index

    def array_ref(self, descriptor: ArrayDesc) -> int:
        name_index = self.utf8(descriptor.utf8())
        class_index = self._add(JConstClass(name_index))
        return class_index

    def field_name(self, name: str) -> int:
        return self.utf8(name)

    def field_descriptor(self, descriptor: FieldDescriptor) -> int:
        return self.utf8(descriptor.utf8())

    def field_ref(self, class_name: str, name: str, descriptor: FieldDescriptor) -> int:
        class_index = self.class_ref(class_name)
        name_index = self.field_name(name)
        descriptor_index = self.field_descriptor(descriptor)
        name_and_type_index = self._add(JConstNameAndType(name_index, descriptor_index))
        field_index = self._add(JConstMethodRef(class_index, name_and_type_index))
        return field_index

    def method_name(self, name: str) -> int:
        return self.utf8(name)

    def method_descriptor(self, descriptor: MethodDescriptor) -> int:
        return self.utf8(descriptor.utf8())

    def method_ref(self, class_name: str, name: str, descriptor: MethodDescriptor) -> int:
        class_index = self.class_ref(class_name)
        name_index = self.method_name(name)
        descriptor_index = self.method_descriptor(descriptor)
        name_and_type_index = self._add(JConstNameAndType(name_index, descriptor_index))
        method_index = self._add(JConstMethodRef(class_index, name_and_type_index))
        return method_index

    def int(self, value: int) -> int:
        return self._add(JConstInt(value))

    def long(self, value: int) -> int:
        return self._add(JConstLong(value))

    def float(self, value: float) -> int:
        return self._add(JConstFloat(value))

    def double(self, value: float) -> int:
        return self._add(JConstDouble(value))

    def string(self, value: str) -> int:
        utf8_index = self.utf8(value)
        string_index = self._add(JConstString(utf8_index))
        return string_index
