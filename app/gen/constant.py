from abc import ABC
from typing import Dict

from app.gen.descriptor import MethodDescriptor, FieldDescriptor
from app.gen.util import is_int, is_long


class JConst(ABC):
    pass


class JConstUtf8(JConst):
    def __init__(self, value: str):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstInt(JConst):
    def __init__(self, value: int):
        assert is_int(value)
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstLong(JConst):
    def __init__(self, value: int):
        assert is_long(value)
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstFloat(JConst):
    def __init__(self, value: float):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstDouble(JConst):
    def __init__(self, value: float):
        self.value = value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.value == other.value


class JConstString(JConst):
    def __init__(self, utf8: int):
        self.utf8 = utf8

    def __hash__(self):
        return hash(self.utf8)

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.utf8 == other.utf8


class JConstClass(JConst):
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
            index = len(self._constants)
            self._constants[const] = index

        return index

    def const_class(self, class_name: str) -> int:
        name_index = self._add(JConstUtf8(class_name))
        class_index = self._add(JConstClass(name_index))
        return class_index

    def const_field_name(self, name: str) -> int:
        return self._add(JConstUtf8(name))

    def const_field_descriptor(self, descriptor: FieldDescriptor) -> int:
        return self._add(JConstUtf8(descriptor.utf8()))

    def const_field_ref(self, class_name: str, name: str, descriptor: FieldDescriptor) -> int:
        class_index = self.const_class(class_name)
        name_index = self.const_field_name(name)
        descriptor_index = self.const_field_descriptor(descriptor)
        name_and_type_index = self._add(JConstNameAndType(name_index, descriptor_index))
        field_index = self._add(JConstMethodRef(class_index, name_and_type_index))
        return field_index

    def const_method_name(self, name: str) -> int:
        return self._add(JConstUtf8(name))

    def const_method_descriptor(self, descriptor: MethodDescriptor) -> int:
        return self._add(JConstUtf8(descriptor.utf8()))

    def const_method_ref(self, class_name: str, name: str, descriptor: MethodDescriptor) -> int:
        class_index = self.const_class(class_name)
        name_index = self.const_method_name(name)
        descriptor_index = self.const_method_descriptor(descriptor)
        name_and_type_index = self._add(JConstNameAndType(name_index, descriptor_index))
        method_index = self._add(JConstMethodRef(class_index, name_and_type_index))
        return method_index

    def const_int(self, value: int) -> int:
        return self._add(JConstInt(value))

    def const_long(self, value: int) -> int:
        return self._add(JConstLong(value))

    def const_float(self, value: float) -> int:
        return self._add(JConstFloat(value))

    def const_double(self, value: float) -> int:
        return self._add(JConstDouble(value))

    def const_string(self, value: str) -> int:
        utf8_index = self._add(JConstUtf8(value))
        string_index = self._add(JConstString(utf8_index))
        return string_index
