import struct
from enum import IntFlag
from typing import BinaryIO

from app.gen.code import Code
from app.gen.constant import JConstUtf8, JConstInt, JConstLong, JConstFloat, JConstDouble, JConstString, JConstClass, \
    JConstFieldRef, JConstMethodRef, JConstNameAndType, JConst
from app.gen.structs import Class, Field, Method

MAGIC = 0xCAFEBABE
MINOR_VERSION = 0
MAJOR_VERSION = 55
NO_SUPER_CLASS_INDEX = 0
CODE_ATTRIBUTE_NAME = 'Code'
CODE_ATTRIBUTE_DEFAULT_SIZE = 12


class ClassFlag(IntFlag):
    ACC_PUBLIC = 0x0001
    ACC_SUPER = 0x0020


class FieldFlag(IntFlag):
    ACC_PUBLIC = 0x0001
    ACC_STATIC = 0x0008


class MethodFlag(IntFlag):
    ACC_PUBLIC = 0x0001
    ACC_STATIC = 0x0008


# binary formatting
BE = '>'
U1 = 'B'
U2 = 'H'
U4 = 'I'
U8 = 'Q'
I1 = 'b'
I2 = 'h'
I4 = 'i'
I8 = 'q'
F4 = 'f'
F8 = 'd'


def _write_magic(output: BinaryIO):
    output.write(struct.pack(BE + U4, MAGIC))


def _write_version(output: BinaryIO):
    output.write(struct.pack(BE + U2 + U2, MINOR_VERSION, MAJOR_VERSION))


def _write_utf8(output: BinaryIO, value: str):
    for c in (ord(char) for char in value):
        if c == 0x00:
            # NULL byte encoding.
            output.write(bytes([0xC0, 0x80]))
        elif c < 0x7F:
            # ASCII
            output.write(bytes(c))
        elif c < 0x7FF:
            # two-byte codepoint
            output.write(bytes([
                (0xC0 | (0x1F & (c >> 6))),
                (0x80 | (0x3F & c))
            ]))
        elif c < 0xFFFF:
            # three-byte codepoint.
            output.write(bytes([
                (0xE0 | (0x0F & (c >> 12))),
                (0x80 | (0x3F & (c >> 6))),
                (0x80 | (0x3F & c))
            ]))
        else:
            # two-times-three byte codepoint.
            c -= 0x10000
            output.write(bytes([
                0xED,
                0xA0 | ((c >> 16) & 0x0F),
                0x80 | ((c >> 10) & 0x3f),
                0xED,
                0xb0 | ((c >> 6) & 0x0f),
                0x80 | (c & 0x3f)
            ]))


def _write_constant(constant: JConst, output: BinaryIO):
    tag = constant.tag()
    output.write(struct.pack(BE + U1, tag.value))

    if isinstance(constant, JConstUtf8):
        _write_utf8(output, constant.value)
    elif isinstance(constant, JConstInt):
        output.write(struct.pack(BE + I4, constant.value))
    elif isinstance(constant, JConstLong):
        output.write(struct.pack(BE + I8, constant.value))
    elif isinstance(constant, JConstFloat):
        output.write(struct.pack(BE + F4, constant.value))
    elif isinstance(constant, JConstDouble):
        output.write(struct.pack(BE + F8, constant.value))
    elif isinstance(constant, JConstString):
        output.write(struct.pack(BE + U2, constant.utf8_index))
    elif isinstance(constant, JConstClass):
        output.write(struct.pack(BE + U2, constant.name_index))
    elif isinstance(constant, JConstFieldRef):
        output.write(struct.pack(BE + U2 + U2, constant.class_index, constant.name_and_type_index))
    elif isinstance(constant, JConstMethodRef):
        output.write(struct.pack(BE + U2 + U2, constant.class_index, constant.name_and_type_index))
    elif isinstance(constant, JConstNameAndType):
        output.write(struct.pack(BE + U2 + U2, constant.name_index, constant.descriptor_index))


def _write_constant_pool(cls: Class, output: BinaryIO):
    constants = cls.constant_pool.constants

    # cp count
    output.write(struct.pack(BE + U2, len(constants) + 1))

    for c in constants:
        _write_constant(c, output)


def _write_access_flags(cls: Class, output: BinaryIO):
    flags = ClassFlag.ACC_PUBLIC | ClassFlag.ACC_SUPER
    output.write(struct.pack(BE + U2, flags))


def _write_this_class(cls: Class, output: BinaryIO):
    output.write(struct.pack(BE + U2, cls.this_class))


def _write_super_class(output: BinaryIO):
    output.write(struct.pack(BE + U2, NO_SUPER_CLASS_INDEX))


def _write_interfaces(output):
    # interfaces count
    output.write(struct.pack(BE + U2, 0))


def _write_field(field: Field, output: BinaryIO):
    flags = FieldFlag.ACC_PUBLIC | FieldFlag.ACC_STATIC

    output.write(struct.pack(BE + U2, flags))
    output.write(struct.pack(BE + U2, field.name_index))
    output.write(struct.pack(BE + U2, field.descriptor_index))

    # attributes count
    output.write(struct.pack(BE + U2, 0))


def _write_fields(cls: Class, output: BinaryIO):
    fields = cls.fields

    # fields count
    output.write(struct.pack(BE + U2, len(fields)))

    for f in fields:
        _write_field(f, output)


def _write_instruction(i: int, instruction, inst_positions, output: BinaryIO):
    opcode = instruction[0]

    if opcode.is_jump():
        target_index = instruction[1]
        pos = inst_positions[i]
        target_pos = inst_positions[target_index]
        offset = target_pos - pos
        output.write(struct.pack(opcode.fmt, opcode, offset))
    else:
        output.write(struct.pack(opcode.fmt, *instruction))


def _write_code(code: Code, output: BinaryIO):

    # calculate absolute positions of instructions, max_stack and max locals
    code_size = 0
    inst_positions = []
    stack = 0
    max_stack = 0

    for (index, instruction) in enumerate(code.instructions):
        inst_positions.append(code_size)
        code_size += code.instruction_length(index)
        stack += code.instruction_stack_diff(index)

        if max_stack < stack:
            max_stack = stack

    max_locals = 0

    for local in code.locals:
        max_locals += local.size()

    size = CODE_ATTRIBUTE_DEFAULT_SIZE + code_size

    output.write(struct.pack(BE + U2, code.constant_pool.utf8(CODE_ATTRIBUTE_NAME)))
    output.write(struct.pack(BE + U4, size))
    output.write(struct.pack(BE + U2, max_stack))
    output.write(struct.pack(BE + U2, max_locals))
    output.write(struct.pack(BE + U4, code_size))

    # write instructions
    for (i, instruction) in enumerate(code.instructions):
        _write_instruction(i, instruction, inst_positions, output)

    # exception table length
    output.write(struct.pack(BE + U2, 0))
    # attributes count
    output.write(struct.pack(BE + U2, 0))


def _write_method(method: Method, output: BinaryIO):
    flags = MethodFlag.ACC_PUBLIC | MethodFlag.ACC_STATIC

    output.write(struct.pack(BE + U2, flags))
    output.write(struct.pack(BE + U2, method.name_index))
    output.write(struct.pack(BE + U2, method.descriptor_index))

    # attributes count
    output.write(struct.pack(BE + U2, 1))
    _write_code(method.code, output)


def _write_methods(cls: Class, output: BinaryIO):
    methods = cls.methods

    # methods count
    output.write(struct.pack(BE + U2, len(methods)))

    for m in methods:
        _write_method(m, output)


def _write_attributes(output: BinaryIO):
    # attributes count
    output.write(struct.pack(BE + U2, 0))


def create_classfile(cls: Class, output: BinaryIO):
    # collect constants and create constant pool
    _write_magic(output)
    _write_version(output)
    _write_constant_pool(cls, output)
    _write_access_flags(cls, output)
    _write_this_class(cls, output)
    _write_super_class(output)
    _write_interfaces(output)
    _write_fields(cls, output)
    _write_methods(cls, output)
    _write_attributes(output)
