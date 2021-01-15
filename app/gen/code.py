from enum import IntEnum
from typing import List, Optional, Any, Dict

from app.gen.constant import ConstantPool
from app.gen.descriptor import JOperandType, JOperandTypeInt, JOperandTypeLong, JOperandTypeFloat, JOperandTypeDouble, \
    JOperandTypeReference, FieldDescriptor, MethodDescriptor, ArrayDesc, IntDesc, LongDesc, FloatDesc, DoubleDesc, \
    ByteDesc, BooleanDesc, CharDesc, ShortDesc, ClassDesc
from app.gen.opcode import Opcode
from app.util import is_byte, is_short


class ArrayType(IntEnum):
    BOOLEAN = 4
    CHAR = 5
    FLOAT = 6
    DOUBLE = 7
    BYTE = 8
    SHORT = 9
    INT = 10
    LONG = 11


class Code:

    def __init__(self, constant_pool: ConstantPool):
        self._constant_pool = constant_pool
        self._instructions: List[Any] = []
        self._locals: List[JOperandType] = []
        self._locals_size: int = 0
        self._stack_diffs: Dict[int, int] = {}

    @property
    def instructions(self):
        return self._instructions

    @property
    def locals(self) -> List[JOperandType]:
        return self._locals

    @property
    def constant_pool(self) -> ConstantPool:
        return self._constant_pool

    def instruction_length(self, index: int):
        """
        The length of the instruction.
        :param index: The index of the instruction
        :return: Length in bytes.
        """
        instruction = self._instructions[index]

        if instruction[0].length is not None:
            return instruction[0].length

        raise NotImplementedError()

    def instruction_stack_diff(self, index: int):
        """
        The stack size difference after execution of the instruction.
        :param index: The index of the instruction.
        :return: Difference in words.
        """
        instruction = self._instructions[index]

        if instruction[0].stack_diff is not None:
            return instruction[0].stack_diff

        return self._stack_diffs[index]

    def _set_stack_diff(self, diff: int):
        pos = self.pos()
        self._stack_diffs[pos] = diff

    def _add_instruction(self, opcode: Opcode, *args):
        self._instructions.append([opcode, *args])

    def _add_variable(self, variable_type: JOperandType) -> int:
        self._locals.append(variable_type)
        index = self._locals_size
        self._locals_size += variable_type.size()
        return index

    def pos(self) -> int:
        """
        The index of the next added instruction.
        It can be used later for jump instruction.
        :return: The index of the instruction.
        """
        return len(self._instructions)

    def variable_int(self) -> int:
        """
        Create a local int variable.
        :return: The index of the variable.
        """
        return self._add_variable(JOperandTypeInt())

    def variable_long(self) -> int:
        """
        Create a local long variable.
        :return: The index of the variable.
        """
        return self._add_variable(JOperandTypeLong())

    def variable_float(self) -> int:
        """
        Create a local float variable.
        :return: The index of the variable.
        """
        return self._add_variable(JOperandTypeFloat())

    def variable_double(self) -> int:
        """
        Create a local double variable.
        :return: The index of the variable.
        """
        return self._add_variable(JOperandTypeDouble())

    def variable_reference(self) -> int:
        """
        Create a local reference variable.
        :return: The index of the variable.
        """
        return self._add_variable(JOperandTypeReference())

    def const_int(self, value: int):
        """
        Push int constant onto the stack.
        :param value: The integer value.
        """
        if value == -1:
            self._add_instruction(Opcode.ICONST_M1)
        elif value == 0:
            self._add_instruction(Opcode.ICONST_0)
        elif value == 1:
            self._add_instruction(Opcode.ICONST_1)
        elif value == 2:
            self._add_instruction(Opcode.ICONST_2)
        elif value == 3:
            self._add_instruction(Opcode.ICONST_3)
        elif value == 4:
            self._add_instruction(Opcode.ICONST_4)
        elif value == 5:
            self._add_instruction(Opcode.ICONST_5)
        elif is_byte(value):
            self._add_instruction(Opcode.BIPUSH, value)
        elif is_short(value):
            self._add_instruction(Opcode.SIPUSH, value)
        else:
            index = self._constant_pool.int(value)
            self._add_instruction(Opcode.LDC, index)

    def const_long(self, value: int):
        """
        Push long constant onto the stack.
        :param value: The long value.
        """
        if value == 0:
            self._add_instruction(Opcode.LCONST_0)
        elif value == 1:
            self._add_instruction(Opcode.LCONST_1)
        else:
            index = self._constant_pool.long(value)
            self._add_instruction(Opcode.LDC2_W, index)

    def const_float(self, value: float):
        """
        Push float constant onto the stack.
        :param value: The float value.
        """
        if value == 0:
            self._add_instruction(Opcode.FCONST_0)
        elif value == 1:
            self._add_instruction(Opcode.FCONST_1)
        elif value == 2:
            self._add_instruction(Opcode.FCONST_2)
        else:
            index = self._constant_pool.float(value)
            self._add_instruction(Opcode.LDC, index)

    def const_double(self, value: float):
        """
        Push double constant onto the stack.
        :param value: The double value.
        """
        if value == 0:
            self._add_instruction(Opcode.DCONST_0)
        elif value == 1:
            self._add_instruction(Opcode.DCONST_1)
        else:
            index = self._constant_pool.double(value)
            self._add_instruction(Opcode.LDC, index)

    def const_string(self, value: str):
        """
        Push string constant reference onto the stack.
        :param value: The string value.
        """
        index = self._constant_pool.string(value)
        self._add_instruction(Opcode.LDC, index)

    def load_int(self, index: int):
        """
        Load local variable int value onto the stack.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.ILOAD_0)
        elif index == 1:
            self._add_instruction(Opcode.ILOAD_1)
        elif index == 2:
            self._add_instruction(Opcode.ILOAD_2)
        elif index == 3:
            self._add_instruction(Opcode.ILOAD_3)
        else:
            self._add_instruction(Opcode.ILOAD, index)

    def load_long(self, index: int):
        """
        Load local variable long value onto the stack.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.LLOAD_0)
        elif index == 1:
            self._add_instruction(Opcode.LLOAD_1)
        elif index == 2:
            self._add_instruction(Opcode.LLOAD_2)
        elif index == 3:
            self._add_instruction(Opcode.LLOAD_3)
        else:
            self._add_instruction(Opcode.LLOAD, index)

    def load_float(self, index: int):
        """
        Load local variable float value onto the stack.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.FLOAD_0)
        elif index == 1:
            self._add_instruction(Opcode.FLOAD_1)
        elif index == 2:
            self._add_instruction(Opcode.FLOAD_2)
        elif index == 3:
            self._add_instruction(Opcode.FLOAD_3)
        else:
            self._add_instruction(Opcode.FLOAD, index)

    def load_double(self, index: int):
        """
        Load local variable double value onto the stack.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.DLOAD_0)
        elif index == 1:
            self._add_instruction(Opcode.DLOAD_1)
        elif index == 2:
            self._add_instruction(Opcode.DLOAD_2)
        elif index == 3:
            self._add_instruction(Opcode.DLOAD_3)
        else:
            self._add_instruction(Opcode.DLOAD, index)

    def load_reference(self, index: int):
        """
        Load local variable reference value onto the stack.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.ALOAD_0)
        elif index == 1:
            self._add_instruction(Opcode.ALOAD_1)
        elif index == 2:
            self._add_instruction(Opcode.ALOAD_2)
        elif index == 3:
            self._add_instruction(Opcode.ALOAD_3)
        else:
            self._add_instruction(Opcode.ALOAD, index)

    def store_int(self, index: int):
        """
        Store int value from the stack into the local variable.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.ISTORE_0)
        elif index == 1:
            self._add_instruction(Opcode.ISTORE_1)
        elif index == 2:
            self._add_instruction(Opcode.ISTORE_2)
        elif index == 3:
            self._add_instruction(Opcode.ISTORE_3)
        else:
            self._add_instruction(Opcode.ISTORE, index)

    def store_long(self, index: int):
        """
        Store long value from the stack into the local variable.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.LSTORE_0)
        elif index == 1:
            self._add_instruction(Opcode.LSTORE_1)
        elif index == 2:
            self._add_instruction(Opcode.LSTORE_2)
        elif index == 3:
            self._add_instruction(Opcode.LSTORE_3)
        else:
            self._add_instruction(Opcode.LSTORE, index)

    def store_float(self, index: int):
        """
        Store float value from the stack into the local variable.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.FSTORE_0)
        elif index == 1:
            self._add_instruction(Opcode.FSTORE_1)
        elif index == 2:
            self._add_instruction(Opcode.FSTORE_2)
        elif index == 3:
            self._add_instruction(Opcode.FSTORE_3)
        else:
            self._add_instruction(Opcode.FSTORE, index)

    def store_double(self, index: int):
        """
        Store double value from the stack into the local variable.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.DSTORE_0)
        elif index == 1:
            self._add_instruction(Opcode.DSTORE_1)
        elif index == 2:
            self._add_instruction(Opcode.DSTORE_2)
        elif index == 3:
            self._add_instruction(Opcode.DSTORE_3)
        else:
            self._add_instruction(Opcode.DSTORE, index)

    def store_reference(self, index: int):
        """
        Store reference value from the stack into the local variable.
        :param index: Index of the variable.
        """
        if index == 0:
            self._add_instruction(Opcode.ASTORE_0)
        elif index == 1:
            self._add_instruction(Opcode.ASTORE_1)
        elif index == 2:
            self._add_instruction(Opcode.ASTORE_2)
        elif index == 3:
            self._add_instruction(Opcode.ASTORE_3)
        else:
            self._add_instruction(Opcode.ASTORE, index)

    def array_load_int(self):
        """
        Load int value from the array onto the stack.
        """
        self._add_instruction(Opcode.IALOAD)

    def array_load_long(self):
        """
        Load long value from the array onto the stack.
        """
        self._add_instruction(Opcode.LALOAD)

    def array_load_float(self):
        """
        Load float value from the array onto the stack.
        """
        self._add_instruction(Opcode.FALOAD)

    def array_load_double(self):
        """
        Load double value from the array onto the stack.
        """
        self._add_instruction(Opcode.DALOAD)

    def array_load_reference(self):
        """
        Load reference value from the array onto the stack.
        """
        self._add_instruction(Opcode.AALOAD)

    def array_load_byte(self):
        """
        Load byte value from the array onto the stack as an int.
        """
        self._add_instruction(Opcode.BALOAD)

    def array_load_boolean(self):
        """
        Load boolean value from the array onto the stack as an int.
        """
        self._add_instruction(Opcode.BALOAD)

    def array_load_char(self):
        """
        Load char value from the array onto the stack as an int.
        """
        self._add_instruction(Opcode.CALOAD)

    def array_load_short(self):
        """
        Load short value from the array onto the stack as an int.
        """
        self._add_instruction(Opcode.SALOAD)

    def array_store_int(self):
        """
        Store int value from the stack into the array.
        """
        self._add_instruction(Opcode.IASTORE)

    def array_store_long(self):
        """
        Store long value from the stack into the array.
        """
        self._add_instruction(Opcode.LASTORE)

    def array_store_float(self):
        """
        Store float value from the stack into the array.
        """
        self._add_instruction(Opcode.FASTORE)

    def array_store_double(self):
        """
        Store double value from the stack into the array.
        """
        self._add_instruction(Opcode.DASTORE)

    def array_store_reference(self):
        """
        Store reference value from the stack into the array.
        """
        self._add_instruction(Opcode.AASTORE)

    def array_store_byte(self):
        """
        Store int value from the stack into the array as a byte.
        """
        self._add_instruction(Opcode.BASTORE)

    def array_store_boolean(self):
        """
        Store int value from the stack into the array as a boolean.
        """
        self._add_instruction(Opcode.BASTORE)

    def array_store_char(self):
        """
        Store int value from the stack into the array as a char.
        """
        self._add_instruction(Opcode.CASTORE)

    def array_store_short(self):
        """
        Store int value from the stack into the array as a short.
        """
        self._add_instruction(Opcode.SASTORE)

    def pop(self):
        """
        Pop int, float or reference from the stack.
        """
        self._add_instruction(Opcode.POP)

    def pop2(self):
        """
        Pop long or double from the stack.
        """
        self._add_instruction(Opcode.POP2)

    def dup(self):
        """
        Duplicate int, float or reference from the top of the stack.
        """
        self._add_instruction(Opcode.DUP)

    def dup_x1(self):
        """
        Duplicate int, float or reference from the top of the stack and insert
        it down before a previous int, float or reference.
        """
        self._add_instruction(Opcode.DUP_X1)

    def dup_x2(self):
        """
        Duplicate int, float or reference from the top of the stack and insert
        it down before a previous long, double, two ints, two floats or two references.
        """
        self._add_instruction(Opcode.DUP_X2)

    def dup2(self):
        """
        Duplicate long, double, two ints, two floats or two references
        from the top of the stack.
        """
        self._add_instruction(Opcode.DUP2)

    def dup2_x1(self):
        """
        Duplicate long, double, two ints, two floats or two references
        from the top of the stack and insert it down before a previous int, float or reference.
        """
        self._add_instruction(Opcode.DUP2_X1)

    def dup2_x2(self):
        """
        Duplicate long, double, two ints, two floats or two references
        from the top of the stack and insert it down before a previous
        long, double, two ints, two floats or two references.
        """
        self._add_instruction(Opcode.DUP2_X2)

    def swap(self):
        """
        Swap int, float or reference from the top of the stack
        with the lower int, float or reference.
        """
        self._add_instruction(Opcode.SWAP)

    def add_int(self):
        self._add_instruction(Opcode.IADD)

    def add_long(self):
        self._add_instruction(Opcode.LADD)

    def add_float(self):
        self._add_instruction(Opcode.FADD)

    def add_double(self):
        self._add_instruction(Opcode.DADD)

    def sub_int(self):
        self._add_instruction(Opcode.ISUB)

    def sub_long(self):
        self._add_instruction(Opcode.LSUB)

    def sub_float(self):
        self._add_instruction(Opcode.FSUB)

    def sub_double(self):
        self._add_instruction(Opcode.DSUB)

    def mul_int(self):
        self._add_instruction(Opcode.IMUL)

    def mul_long(self):
        self._add_instruction(Opcode.LMUL)

    def mul_float(self):
        self._add_instruction(Opcode.FMUL)

    def mul_double(self):
        self._add_instruction(Opcode.DMUL)

    def div_int(self):
        self._add_instruction(Opcode.IDIV)

    def div_long(self):
        self._add_instruction(Opcode.LDIV)

    def div_float(self):
        self._add_instruction(Opcode.FDIV)

    def div_double(self):
        self._add_instruction(Opcode.DDIV)

    def rem_int(self):
        self._add_instruction(Opcode.IREM)

    def rem_long(self):
        self._add_instruction(Opcode.LREM)

    def rem_float(self):
        self._add_instruction(Opcode.FREM)

    def rem_double(self):
        self._add_instruction(Opcode.DREM)

    def neg_int(self):
        self._add_instruction(Opcode.INEG)

    def neg_long(self):
        self._add_instruction(Opcode.LNEG)

    def neg_float(self):
        self._add_instruction(Opcode.FNEG)

    def neg_double(self):
        self._add_instruction(Opcode.DNEG)

    def shl_int(self):
        self._add_instruction(Opcode.ISHL)

    def shl_long(self):
        self._add_instruction(Opcode.LSHL)

    def shr_int(self):
        self._add_instruction(Opcode.ISHR)

    def shr_long(self):
        self._add_instruction(Opcode.LSHR)

    def ushr_int(self):
        self._add_instruction(Opcode.IUSHR)

    def ushr_long(self):
        self._add_instruction(Opcode.LUSHR)

    def and_int(self):
        self._add_instruction(Opcode.IAND)

    def and_long(self):
        self._add_instruction(Opcode.LAND)

    def or_int(self):
        self._add_instruction(Opcode.IOR)

    def or_long(self):
        self._add_instruction(Opcode.LOR)

    def xor_int(self):
        self._add_instruction(Opcode.IXOR)

    def xor_long(self):
        self._add_instruction(Opcode.LXOR)

    def inc_int(self, index: int, const: int):
        self._add_instruction(Opcode.IINC, index, const)

    def int_to_long(self):
        self._add_instruction(Opcode.I2L)

    def int_to_float(self):
        self._add_instruction(Opcode.I2F)

    def int_to_double(self):
        self._add_instruction(Opcode.I2D)

    def long_to_int(self):
        self._add_instruction(Opcode.L2I)

    def long_to_float(self):
        self._add_instruction(Opcode.L2F)

    def long_to_double(self):
        self._add_instruction(Opcode.L2D)

    def float_to_int(self):
        self._add_instruction(Opcode.F2I)

    def float_to_long(self):
        self._add_instruction(Opcode.F2L)

    def float_to_double(self):
        self._add_instruction(Opcode.F2D)

    def double_to_int(self):
        self._add_instruction(Opcode.D2I)

    def double_to_long(self):
        self._add_instruction(Opcode.D2L)

    def double_to_float(self):
        self._add_instruction(Opcode.D2F)

    def int_to_byte(self):
        self._add_instruction(Opcode.I2B)

    def int_to_char(self):
        self._add_instruction(Opcode.I2C)

    def int_to_short(self):
        self._add_instruction(Opcode.I2S)

    def cmp_long(self):
        self._add_instruction(Opcode.LCMP)

    def cmp_float_lt(self):
        self._add_instruction(Opcode.FCMPL)

    def cmp_float_gt(self):
        self._add_instruction(Opcode.FCMPG)

    def cmp_double_l(self):
        self._add_instruction(Opcode.DCMPL)

    def cmp_double_g(self):
        self._add_instruction(Opcode.DCMPG)

    def if_eq(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFEQ, index)

    def if_ne(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFNE, index)

    def if_lt(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFLT, index)

    def if_ge(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFGE, index)

    def if_gt(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFGT, index)

    def if_le(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IFLE, index)

    def if_cmp_int_eq(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPEQ, index)

    def if_cmp_int_ne(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPNE, index)

    def if_cmp_int_lt(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPLT, index)

    def if_cmp_int_ge(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPGE, index)

    def if_cmp_int_gt(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPGT, index)

    def if_cmp_int_le(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ICMPLE, index)

    def if_cmp_reference_eq(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ACMPEQ, index)

    def if_cmp_reference_ne(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.IF_ACMPNE, index)

    def goto(self, index: Optional[int] = None):
        return self._add_instruction(Opcode.GOTO, index)

    def update_jump(self, index: int, target: int):
        """
        Update the jump instruction.
        :param index: Index of the jump instruction.
        :param target: Index of the target instruction.
        """
        try:
            instruction = self._instructions[index]
        except IndexError:
            raise IndexError(f'No instruction on index {index}')

        if not instruction[0].is_jump():
            raise IndexError(f'No jump instruction on index {index}, {instruction[0]} found')

        instruction[1] = target

    def return_int(self):
        self._add_instruction(Opcode.IRETURN)

    def return_long(self):
        self._add_instruction(Opcode.LRETURN)

    def return_float(self):
        self._add_instruction(Opcode.FRETURN)

    def return_double(self):
        self._add_instruction(Opcode.DRETURN)

    def return_reference(self):
        self._add_instruction(Opcode.ARETURN)

    def return_void(self):
        self._add_instruction(Opcode.RETURN)

    def load_static_field(self, class_name: str, name: str, descriptor: FieldDescriptor):
        self._set_stack_diff(descriptor.operand_size())
        index = self._constant_pool.field_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.GETSTATIC, index)

    def store_static_field(self, class_name: str, name: str, descriptor: FieldDescriptor):
        self._set_stack_diff(-descriptor.operand_size())
        index = self._constant_pool.field_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.PUTSTATIC, index)

    def load_field(self, class_name: str, name: str, descriptor: FieldDescriptor):
        self._set_stack_diff(-1 + descriptor.operand_size())
        index = self._constant_pool.field_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.GETFIELD, index)

    def store_field(self, class_name: str, name: str, descriptor: FieldDescriptor):
        self._set_stack_diff(-1 - descriptor.operand_size())
        index = self._constant_pool.field_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.PUTFIELD, index)

    def invoke_virtual(self, class_name: str, name: str, descriptor: MethodDescriptor):
        args_size = sum([p.operand_size() for p in descriptor.params_descriptors])
        ret_size = 0 if descriptor.return_descriptor is None else descriptor.return_descriptor.operand_size()
        diff = -1 - args_size + ret_size
        self._set_stack_diff(diff)
        index = self._constant_pool.method_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.INVOKEVIRTUAL, index)

    def invoke_special(self, class_name: str, name: str, descriptor: MethodDescriptor):
        args_size = sum([p.operand_size() for p in descriptor.params_descriptors])
        ret_size = 0 if descriptor.return_descriptor is None else descriptor.return_descriptor.operand_size()
        diff = -1 - args_size + ret_size
        self._set_stack_diff(diff)
        index = self._constant_pool.method_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.INVOKESPECIAL, index)

    def invoke_static(self, class_name: str, name: str, descriptor: MethodDescriptor):
        args_size = sum([p.operand_size() for p in descriptor.params_descriptors])
        ret_size = 0 if descriptor.return_descriptor is None else descriptor.return_descriptor.operand_size()
        diff = -1 - args_size + ret_size
        self._set_stack_diff(diff)
        index = self._constant_pool.method_ref(class_name, name, descriptor)
        self._add_instruction(Opcode.INVOKESTATIC, index)

    def new(self, class_name: str):
        index = self._constant_pool.class_ref(class_name)
        self._add_instruction(Opcode.NEW, index)

    def new_array(self, inner_descriptor: FieldDescriptor):
        if isinstance(inner_descriptor, IntDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.INT)
        elif isinstance(inner_descriptor, LongDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.LONG)
        elif isinstance(inner_descriptor, FloatDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.FLOAT)
        elif isinstance(inner_descriptor, DoubleDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.DOUBLE)
        elif isinstance(inner_descriptor, ByteDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.BYTE)
        elif isinstance(inner_descriptor, BooleanDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.BOOLEAN)
        elif isinstance(inner_descriptor, CharDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.CHAR)
        elif isinstance(inner_descriptor, ShortDesc):
            self._add_instruction(Opcode.NEWARRAY, ArrayType.SHORT)
        elif isinstance(inner_descriptor, ClassDesc):
            index = self._constant_pool.class_ref(inner_descriptor.class_name)
            self._add_instruction(Opcode.ANEWARRAY, index)
        elif isinstance(inner_descriptor, ArrayDesc):
            index = self._constant_pool.array_ref(inner_descriptor)
            self._add_instruction(Opcode.ANEWARRAY, index)

    def array_length(self):
        self._add_instruction(Opcode.ARRAYLENGTH)

    def if_null(self, index: Optional[int] = None):
        self._add_instruction(Opcode.IFNULL, index)

    def if_non_null(self, index: Optional[int] = None):
        self._add_instruction(Opcode.IFNONNULL, index)
