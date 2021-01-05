from abc import abstractmethod, ABC
from enum import Enum
from typing import List, Union

import numpy
import struct


class ConstantTag(Enum):
    UTF8 = 1
    INTEGER = 3
    FLOAT = 4
    LONG = 5
    DOUBLE = 6
    CLASS = 7
    STRING = 8
    FIELDREF = 9
    METHODREF = 10
    INTERFACE_METHODREF = 11
    NAME_AND_TYPE = 12

    # METHOD_HANDLE = 15
    # METHOD_TYPE = 16
    # DYNAMIC = 17
    # INVOKE_DYNAMIC = 18
    # MODULE = 19
    # PACKAGE = 20

    def to_bin(self):
        return struct.pack('>B', self.tag)


class Info(ABC):
    @abstractmethod
    def tag(self) -> ConstantTag:
        pass

    @abstractmethod
    def to_bin(self) -> bytes:
        pass


class Utf8Info(Info):
    def __init__(self, value: str):
        self.value = value

    def tag(self) -> ConstantTag:
        return ConstantTag.UTF8

    def to_bin(self) -> bytes:
        data = bytearray()

        for char in self.value:
            c = ord(char)

            if c == 0x00 or (0x80 < c < 0x7FF):
                data.extend([
                    (0xC0 | (0x1F & (c >> 6))),
                    (0x80 | (0x3F & c))
                ])
            elif c < 0x7F:
                data.append(c)
            elif 0x800 < c < 0xFFFF:
                data.extend([
                    (0xE0 | (0x0F & (c >> 12))),
                    (0x80 | (0x3F & (c >> 6))),
                    (0x80 | (0x3F & c))
                ])

        return struct.pack('>H', len(data)) + data


class IntegerInfo(Info):
    def __init__(self, value: int):
        self.value = value

    def tag(self) -> ConstantTag:
        return ConstantTag.INTEGER

    def to_bin(self) -> bytes:
        return struct.pack('>i', self.value)


class FloatInfo(Info):
    def __init__(self, value: float):
        self.value = value

    def tag(self) -> ConstantTag:
        return ConstantTag.FLOAT

    def to_bin(self) -> bytes:
        return struct.pack('>f', self.value)


class LongInfo(Info):
    def __init__(self, value: int):
        self.value = value

    def tag(self) -> ConstantTag:
        return ConstantTag.LONG

    def to_bin(self) -> bytes:
        return struct.pack('>q', self.value)


class DoubleInfo(Info):
    def __init__(self, value: float):
        self.value = value

    def tag(self) -> ConstantTag:
        return ConstantTag.DOUBLE

    def to_bin(self) -> bytes:
        return struct.pack('>d', self.value)


class ClassInfo(Info):
    def __init__(self, name_index: int):
        self.name_index = name_index

    def tag(self) -> ConstantTag:
        return ConstantTag.CLASS

    def to_bin(self) -> bytes:
        return struct.pack('>H', self.name_index)


class StringInfo(Info):
    def __init__(self, string_index: int):
        self.string_index = string_index

    def tag(self) -> ConstantTag:
        return ConstantTag.STRING

    def to_bin(self) -> bytes:
        return struct.pack('>H', self.string_index)


class FieldrefInfo(Info):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def tag(self) -> ConstantTag:
        return ConstantTag.FIELDREF

    def to_bin(self) -> bytes:
        return struct.pack('>HH', self.class_index, self.name_and_type_index)


class MethodrefInfo(Info):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def tag(self) -> ConstantTag:
        return ConstantTag.METHODREF

    def to_bin(self) -> bytes:
        return struct.pack('>HH', self.class_index, self.name_and_type_index)


class InterfaceMethodrefInfo(Info):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def tag(self) -> ConstantTag:
        return ConstantTag.INTERFACE_METHODREF

    def to_bin(self) -> bytes:
        return struct.pack('>HH', self.class_index, self.name_and_type_index)


class NameAndTypeInfo(Info):
    def __init__(self, name_index: int, descriptor_index: int):
        self.name_index = name_index
        self.descriptor_index = descriptor_index

    def tag(self) -> ConstantTag:
        return ConstantTag.NAME_AND_TYPE

    def to_bin(self) -> bytes:
        return struct.pack('>HH', self.name_index, self.descriptor_index)


class ConstantPoolInfo:
    def __init__(self, tag, info):
        self.tag = tag
        self.info = info



class ConstantPool:
    def __init__(self):
        self.pool: List[Union[ConstantPoolInfo, None]] = []

    def _add(self, tag, info) -> int:
        self.pool.

    def integer(self, value: int) -> int:
        return self._add(ConstantPoolInfo(ConstantTag.INTEGER, (value,)))

    def long(self, value: int):
        self.pool.append(ConstantPoolInfo((value,)))
        self.pool.append(None)
        return len(self.pool) + 1

    def float(self, value: float) -> Float:
        """
        Creates a new :class:`ConstantFloat`, adding it to the pool and
        returning it.
        :param value: The value of the new float.
        """
        self.append((4, value))
        return self.get(self.raw_count - 1)

    def create_long(self, value: int) -> Long:
        """
        Creates a new :class:`ConstantLong`, adding it to the pool and
        returning it.
        :param value: The value of the new long.
        """
        self.append((5, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_double(self, value: float) -> Double:
        """
        Creates a new :class:`ConstantDouble`, adding it to the pool and
        returning it.
        :param value: The value of the new Double.
        """
        self.append((6, value))
        self.append(None)
        return self.get(self.raw_count - 2)

    def create_class(self, name: str) -> ConstantClass:
        """
        Creates a new :class:`ConstantClass`, adding it to the pool and
        returning it.
        :param name: The name of the new class.
        """
        self.append((
            7,
            self.create_utf8(name).index
        ))
        return self.get(self.raw_count - 1)

    def create_string(self, value: str) -> String:
        """
        Creates a new :class:`ConstantString`, adding it to the pool and
        returning it.
        :param value: The value of the new string as a UTF8 string.
        """
        self.append((
            8,
            self.create_utf8(value).index
        ))
        return self.get(self.raw_count - 1)

    def create_name_and_type(self, name: str, descriptor: str) -> NameAndType:
        """
        Creates a new :class:`ConstantNameAndType`, adding it to the pool and
        returning it.
        :param name: The name of the class.
        :param descriptor: The descriptor for `name`.
        """
        self.append((
            12,
            self.create_utf8(name).index,
            self.create_utf8(descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_field_ref(self, class_: str, field: str, descriptor: str) \
            -> FieldReference:
        """
        Creates a new :class:`ConstantFieldRef`, adding it to the pool and
        returning it.
        :param class_: The name of the class to which `field` belongs.
        :param field: The name of the field.
        :param descriptor: The descriptor for `field`.
        """
        self.append((
            9,
            self.create_class(class_).index,
            self.create_name_and_type(field, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_method_ref(self, class_: str, method: str, descriptor: str) \
            -> MethodReference:
        """
        Creates a new :class:`ConstantMethodRef`, adding it to the pool and
        returning it.
        :param class_: The name of the class to which `method` belongs.
        :param method: The name of the method.
        :param descriptor: The descriptor for `method`.
        """
        self.append((
            10,
            self.create_class(class_).index,
            self.create_name_and_type(method, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def create_interface_method_ref(self, class_: str, if_method: str,
                                    descriptor: str) -> InterfaceMethodRef:
        """
        Creates a new :class:`ConstantInterfaceMethodRef`, adding it to the
        pool and returning it.
        :param class_: The name of the class to which `if_method` belongs.
        :param if_method: The name of the interface method.
        :param descriptor: The descriptor for `if_method`.
        """
        self.append((
            11,
            self.create_class(class_).index,
            self.create_name_and_type(if_method, descriptor).index
        ))
        return self.get(self.raw_count - 1)

    def to_bin(self):
        return pack('>H', self.raw_count))

        for constant in self:
            write(constant.pack())

    def __len__(self) -> int:
        """
        The number of `Constants` in the `ConstantPool`, excluding padding.
        """
        count = 0
        for constant in self._pool:
            if constant is not None:
                count += 1
        return count

    @property
    def raw_count(self) -> int:
        """
        The number of `Constants` in the `ConstantPool`, including padding.
        """
        return len(self._pool)
