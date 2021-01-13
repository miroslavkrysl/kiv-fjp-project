import struct
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Optional

from app.gen.opcode import Opcode, stack_change
from app.gen.util import is_short, is_byte, is_ubyte, is_ushort






class ConstInt(JConstant):
    def tag(self) -> int:
        pass

    def __init__(self, value: int):
        self.value = value


class ConstDouble(JConstant):
    def __init__(self, value: float):
        self.value = value


class ConstString(JConstant):
    def __init__(self, value: str):
        self.value = value


class CodeOverflowError(Exception):

    def __str__(self) -> str:
        return 'The code has exceeded the maximal length 65535'


class OperandStackOverflowError(Exception):
    def __init__(self, stack: int):
        self.stack = stack

    def __str__(self) -> str:
        return f'The stack ({self.stack}) has overflowed the allowed size 0 - 65535'


class TooManyLocalsError(Exception):

    def __str__(self) -> str:
        return f'Size of the local variables array has exceeded max size 255'


class TooLongJumpError(Exception):
    def __init__(self, src: int, dest: int):
        self.src = src
        self.dest = dest

    def __str__(self) -> str:
        return f'The jump from instruction {self.src} to {self.dest} is too long ({self.dest - self.src})'


class CodeBuilder(ABC):

    def __init__(self):
        self._constants = None
        self._instructions: []
        self._current_stack: int = 0
        self._max_stack: int = 0
        self._locals: int = 0

    def _update_stack(self, diff: int):
        new_stack = self._current_stack + diff

        if not is_ushort(new_stack):
            raise OperandStackOverflowError(new_stack)

        self._current_stack = new_stack

    def _add_normal_instruction(self, opcode: Opcode, fmt: str = '', *operands):
        stack_diff = stack_change(opcode)

        if stack_diff is None:
            raise NotImplementedError()

        self._add_instruction(opcode, stack_diff, fmt, operands)

    def _add_instruction(self, opcode: Opcode, stack_diff: int, fmt: str = '', *operands):
        instruction = struct.pack('>B', opcode)
        if fmt:
            instruction += struct.pack('>' + fmt, operands)

        if not is_ushort(len(self._instructions) + len(instruction)):
            raise CodeOverflowError()

        self._update_stack(stack_diff)
        self._instructions.extend(instruction)

    def position(self) -> int:
        """
        The position of the next added instruction.

        :return: Position of the instruction first byte from the code beginning.
        """
        return len(self._instructions)

    def add_local(self, size: int) -> int:
        index = self._locals
        self._locals += size
        return index

    def add_const(self, value) -> int:
        # TODO
        pass

    def set_jump_index(self, src: int, dest: int):
        assert is_ushort(src)
        assert is_ushort(dest)
        diff = dest - src

        if not is_short(diff):
            raise TooLongJumpError(src, dest)

        self._instructions[src + 1:src + 3] = struct.pack('>h', diff)

    def NOOP(self):
        self._add_normal_instruction(Opcode.NOOP)

    def ACONST_NULL(self):
        self._add_normal_instruction(Opcode.ACONST_NULL)

    def constant(self, value: JConstant) -> int:
        self._constants.append(value)
        return len(self._constants)


    def LCONST_0(self):
        self._add_normal_instruction(Opcode.LCONST_0)

    def LCONST_1(self):
        self._add_normal_instruction(Opcode.LCONST_1)

    def FCONST_0(self):
        self._add_normal_instruction(Opcode.FCONST_0)

    def FCONST_1(self):
        self._add_normal_instruction(Opcode.FCONST_1)

    def FCONST_2(self):
        self._add_normal_instruction(Opcode.FCONST_2)

    def DCONST_0(self):
        self._add_normal_instruction(Opcode.DCONST_0)

    def DCONST_1(self):
        self._add_normal_instruction(Opcode.DCONST_1)

    def BIPUSH(self, value: int):
        assert is_byte(value)
        self._add_normal_instruction(Opcode.BIPUSH, 'b', value)

    def SIPUSH(self, value: int):
        assert is_short(value)
        self._add_normal_instruction(Opcode.SIPUSH, 'h', value)

    def LDC(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.LDC, 'B', index)

    def LDC_W(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.LDC_W, 'H', index)

    def LDC2_W(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.LDC2_W, 'H', index)

    def ILOAD(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.ILOAD, 'B', index)

    def LLOAD(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.LLOAD, 'B', index)

    def FLOAD(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.FLOAD, 'B', index)

    def DLOAD(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.DLOAD, 'B', index)

    def ALOAD(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.ALOAD, 'B', index)

    def ILOAD_0(self):
        self._add_normal_instruction(Opcode.ILOAD_0)

    def ILOAD_1(self):
        self._add_normal_instruction(Opcode.ILOAD_1)

    def ILOAD_2(self):
        self._add_normal_instruction(Opcode.ILOAD_2)

    def ILOAD_3(self):
        self._add_normal_instruction(Opcode.ILOAD_3)

    def LLOAD_0(self):
        self._add_normal_instruction(Opcode.LLOAD_0)

    def LLOAD_1(self):
        self._add_normal_instruction(Opcode.LLOAD_1)

    def LLOAD_2(self):
        self._add_normal_instruction(Opcode.LLOAD_2)

    def LLOAD_3(self):
        self._add_normal_instruction(Opcode.LLOAD_3)

    def FLOAD_0(self):
        self._add_normal_instruction(Opcode.FLOAD_0)

    def FLOAD_1(self):
        self._add_normal_instruction(Opcode.FLOAD_1)

    def FLOAD_2(self):
        self._add_normal_instruction(Opcode.FLOAD_2)

    def FLOAD_3(self):
        self._add_normal_instruction(Opcode.FLOAD_3)

    def DLOAD_0(self):
        self._add_normal_instruction(Opcode.DLOAD_0)

    def DLOAD_1(self):
        self._add_normal_instruction(Opcode.DLOAD_1)

    def DLOAD_2(self):
        self._add_normal_instruction(Opcode.DLOAD_2)

    def DLOAD_3(self):
        self._add_normal_instruction(Opcode.DLOAD_3)

    def ALOAD_0(self):
        self._add_normal_instruction(Opcode.ALOAD_0)

    def ALOAD_1(self):
        self._add_normal_instruction(Opcode.ALOAD_1)

    def ALOAD_2(self):
        self._add_normal_instruction(Opcode.ALOAD_2)

    def ALOAD_3(self):
        self._add_normal_instruction(Opcode.ALOAD_3)

    def IALOAD(self):
        self._add_normal_instruction(Opcode.IALOAD)

    def LALOAD(self):
        self._add_normal_instruction(Opcode.LALOAD)

    def FALOAD(self):
        self._add_normal_instruction(Opcode.FALOAD)

    def DALOAD(self):
        self._add_normal_instruction(Opcode.DALOAD)

    def AALOAD(self):
        self._add_normal_instruction(Opcode.AALOAD)

    def BALOAD(self):
        self._add_normal_instruction(Opcode.BALOAD)

    def CALOAD(self):
        self._add_normal_instruction(Opcode.CALOAD)

    def SALOAD(self):
        self._add_normal_instruction(Opcode.SALOAD)

    def ISTORE(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.ISTORE, 'B', index)

    def LSTORE(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.LSTORE, 'B', index)

    def FSTORE(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.FSTORE, 'B', index)

    def DSTORE(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.DSTORE, 'B', index)

    def ASTORE(self, index: int):
        assert is_ubyte(index)
        self._add_normal_instruction(Opcode.ASTORE, 'B', index)

    def ISTORE_0(self):
        self._add_normal_instruction(Opcode.ISTORE_0)

    def ISTORE_1(self):
        self._add_normal_instruction(Opcode.ISTORE_1)

    def ISTORE_2(self):
        self._add_normal_instruction(Opcode.ISTORE_2)

    def ISTORE_3(self):
        self._add_normal_instruction(Opcode.ISTORE_3)

    def LSTORE_0(self):
        self._add_normal_instruction(Opcode.LSTORE_0)

    def LSTORE_1(self):
        self._add_normal_instruction(Opcode.LSTORE_1)

    def LSTORE_2(self):
        self._add_normal_instruction(Opcode.LSTORE_2)

    def LSTORE_3(self):
        self._add_normal_instruction(Opcode.LSTORE_3)

    def FSTORE_0(self):
        self._add_normal_instruction(Opcode.FSTORE_0)

    def FSTORE_1(self):
        self._add_normal_instruction(Opcode.FSTORE_1)

    def FSTORE_2(self):
        self._add_normal_instruction(Opcode.FSTORE_2)

    def FSTORE_3(self):
        self._add_normal_instruction(Opcode.FSTORE_3)

    def DSTORE_0(self):
        self._add_normal_instruction(Opcode.DSTORE_0)

    def DSTORE_1(self):
        self._add_normal_instruction(Opcode.DSTORE_1)

    def DSTORE_2(self):
        self._add_normal_instruction(Opcode.DSTORE_2)

    def DSTORE_3(self):
        self._add_normal_instruction(Opcode.DSTORE_3)

    def ASTORE_0(self):
        self._add_normal_instruction(Opcode.ASTORE_0)

    def ASTORE_1(self):
        self._add_normal_instruction(Opcode.ASTORE_1)

    def ASTORE_2(self):
        self._add_normal_instruction(Opcode.ASTORE_2)

    def ASTORE_3(self):
        self._add_normal_instruction(Opcode.ASTORE_3)

    def IASTORE(self):
        self._add_normal_instruction(Opcode.IASTORE)

    def LASTORE(self):
        self._add_normal_instruction(Opcode.LASTORE)

    def FASTORE(self):
        self._add_normal_instruction(Opcode.FASTORE)

    def DASTORE(self):
        self._add_normal_instruction(Opcode.DASTORE)

    def AASTORE(self):
        self._add_normal_instruction(Opcode.AASTORE)

    def BASTORE(self):
        self._add_normal_instruction(Opcode.BASTORE)

    def CASTORE(self):
        self._add_normal_instruction(Opcode.CASTORE)

    def SASTORE(self):
        self._add_normal_instruction(Opcode.SASTORE)

    def POP(self):
        self._add_normal_instruction(Opcode.POP)

    def POP2(self):
        self._add_normal_instruction(Opcode.POP2)

    def DUP(self):
        self._add_normal_instruction(Opcode.DUP)

    def DUP_X1(self):
        self._add_normal_instruction(Opcode.DUP_X1)

    def DUP_X2(self):
        self._add_normal_instruction(Opcode.DUP_X2)

    def DUP2(self):
        self._add_normal_instruction(Opcode.DUP2)

    def DUP2_X1(self):
        self._add_normal_instruction(Opcode.DUP2_X1)

    def DUP2_X2(self):
        self._add_normal_instruction(Opcode.DUP2_X2)

    def SWAP(self):
        self._add_normal_instruction(Opcode.SWAP)

    def IADD(self):
        self._add_normal_instruction(Opcode.IADD)

    def LADD(self):
        self._add_normal_instruction(Opcode.LADD)

    def FADD(self):
        self._add_normal_instruction(Opcode.FADD)

    def DADD(self):
        self._add_normal_instruction(Opcode.DADD)

    def ISUB(self):
        self._add_normal_instruction(Opcode.ISUB)

    def LSUB(self):
        self._add_normal_instruction(Opcode.LSUB)

    def FSUB(self):
        self._add_normal_instruction(Opcode.FSUB)

    def DSUB(self):
        self._add_normal_instruction(Opcode.DSUB)

    def IMUL(self):
        self._add_normal_instruction(Opcode.IMUL)

    def LMUL(self):
        self._add_normal_instruction(Opcode.LMUL)

    def FMUL(self):
        self._add_normal_instruction(Opcode.FMUL)

    def DMUL(self):
        self._add_normal_instruction(Opcode.DMUL)

    def IDIV(self):
        self._add_normal_instruction(Opcode.IDIV)

    def LDIV(self):
        self._add_normal_instruction(Opcode.LDIV)

    def FDIV(self):
        self._add_normal_instruction(Opcode.FDIV)

    def DDIV(self):
        self._add_normal_instruction(Opcode.DDIV)

    def IREM(self):
        self._add_normal_instruction(Opcode.IREM)

    def LREM(self):
        self._add_normal_instruction(Opcode.LREM)

    def FREM(self):
        self._add_normal_instruction(Opcode.FREM)

    def DREM(self):
        self._add_normal_instruction(Opcode.DREM)

    def INEG(self):
        self._add_normal_instruction(Opcode.INEG)

    def LNEG(self):
        self._add_normal_instruction(Opcode.LNEG)

    def FNEG(self):
        self._add_normal_instruction(Opcode.FNEG)

    def DNEG(self):
        self._add_normal_instruction(Opcode.DNEG)

    def ISHL(self):
        self._add_normal_instruction(Opcode.ISHL)

    def LSHL(self):
        self._add_normal_instruction(Opcode.LSHL)

    def ISHR(self):
        self._add_normal_instruction(Opcode.ISHR)

    def LSHR(self):
        self._add_normal_instruction(Opcode.LSHR)

    def IUSHR(self):
        self._add_normal_instruction(Opcode.IUSHR)

    def LUSHR(self):
        self._add_normal_instruction(Opcode.LUSHR)

    def IAND(self):
        self._add_normal_instruction(Opcode.IAND)

    def LAND(self):
        self._add_normal_instruction(Opcode.LAND)

    def IOR(self):
        self._add_normal_instruction(Opcode.IOR)

    def LOR(self):
        self._add_normal_instruction(Opcode.LOR)

    def IXOR(self):
        self._add_normal_instruction(Opcode.IXOR)

    def LXOR(self):
        self._add_normal_instruction(Opcode.LXOR)

    def IINC(self, index: int, const: int):
        assert is_ubyte(index)
        assert is_byte(const)
        self._add_normal_instruction(Opcode.IINC, 'Bb', index, const)

    def I2L(self):
        self._add_normal_instruction(Opcode.I2L)

    def I2F(self):
        self._add_normal_instruction(Opcode.I2F)

    def I2D(self):
        self._add_normal_instruction(Opcode.I2D)

    def L2I(self):
        self._add_normal_instruction(Opcode.L2I)

    def L2F(self):
        self._add_normal_instruction(Opcode.L2F)

    def L2D(self):
        self._add_normal_instruction(Opcode.L2D)

    def F2I(self):
        self._add_normal_instruction(Opcode.F2I)

    def F2L(self):
        self._add_normal_instruction(Opcode.F2L)

    def F2D(self):
        self._add_normal_instruction(Opcode.F2D)

    def D2I(self):
        self._add_normal_instruction(Opcode.D2I)

    def D2L(self):
        self._add_normal_instruction(Opcode.D2L)

    def D2F(self):
        self._add_normal_instruction(Opcode.D2F)

    def I2B(self):
        self._add_normal_instruction(Opcode.I2B)

    def I2C(self):
        self._add_normal_instruction(Opcode.I2C)

    def I2S(self):
        self._add_normal_instruction(Opcode.I2S)

    def LCMP(self):
        self._add_normal_instruction(Opcode.LCMP)

    def FCMPL(self):
        self._add_normal_instruction(Opcode.FCMPL)

    def FCMPG(self):
        self._add_normal_instruction(Opcode.FCMPG)

    def DCMPL(self):
        self._add_normal_instruction(Opcode.DCMPL)

    def DCMPG(self):
        self._add_normal_instruction(Opcode.DCMPG)

    def _jump(self, opcode: Opcode, index: Optional[int] = None) -> int:
        assert is_short(index)
        if index is None:
            index = 0

        pos = len(self._instructions)
        self._add_normal_instruction(opcode, 'h', index)
        return pos

    def IFEQ(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFEQ, index)

    def IFNE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFNE, index)

    def IFLT(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFLT, index)

    def IFGE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFGE, index)

    def IFGT(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFGT, index)

    def IFLE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFLE, index)

    def IF_ICMPEQ(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPEQ, index)

    def IF_ICMPNE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPNE, index)

    def IF_ICMPLT(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPLT, index)

    def IF_ICMPGE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPGE, index)

    def IF_ICMPGT(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPGT, index)

    def IF_ICMPLE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ICMPLE, index)

    def IF_ACMPEQ(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ACMPEQ, index)

    def IF_ACMPNE(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IF_ACMPNE, index)

    def GOTO(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.GOTO, index)

    # --- DEPRECATED ---
    # def JSR(self):
    #     pass
    #
    # def RET(self):
    #     pass

    # --- Not needed yet ---
    # def TABLESWITCH(self):
    #     raise NotImplementedError()
    #
    # def LOOKUPSWITCH(self):
    #     raise NotImplementedError()

    def IRETURN(self):
        self._add_normal_instruction(Opcode.IRETURN)

    def LRETURN(self):
        self._add_normal_instruction(Opcode.LRETURN)

    def FRETURN(self):
        self._add_normal_instruction(Opcode.FRETURN)

    def DRETURN(self):
        self._add_normal_instruction(Opcode.DRETURN)

    def ARETURN(self):
        self._add_normal_instruction(Opcode.ARETURN)

    def RETURN(self):
        self._add_normal_instruction(Opcode.RETURN)

    def GETSTATIC(self, index: int, op_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.GETSTATIC, op_size - 1, 'H', index)

    def PUTSTATIC(self, index: int, op_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.PUTSTATIC, op_size - 1, 'H', index)

    def GETFIELD(self, index: int, op_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.GETFIELD, op_size - 1, 'H', index)

    def PUTFIELD(self, index: int, op_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.PUTFIELD, op_size - 1, 'H', index)

    def INVOKEVIRTUAL(self, index: int, args_size: int, ret_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.INVOKEVIRTUAL, ret_size - (1 + args_size), 'H', index)

    def INVOKESPECIAL(self, index: int, args_size: int, ret_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.INVOKESPECIAL, ret_size - (1 + args_size), 'H', index)

    def INVOKESTATIC(self, index: int, args_size: int, ret_size: int):
        assert is_ushort(index)
        self._add_instruction(Opcode.INVOKESTATIC, ret_size - (1 + args_size), 'H', index)

    # --- Not needed yet
    # def INVOKEINTERFACE(self, index: int, count: int, ret_size: ReturnSize):
    #     assert is_ushort(index)
    #     assert is_ushort(count)
    #     self._add_normal_instruction(Opcode.INVOKEINTERFACE, 'HBB', index, count, 0)

    # --- Not needed yet ---
    # def INVOKEDYNAMIC(self, index: int):
    #     raise NotImplementedError()

    def NEW(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.NEW)

    def NEWARRAY(self, array_type: ArrayType):
        self._add_normal_instruction(Opcode.NEWARRAY, 'B', array_type)

    def ANEWARRAY(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.ANEWARRAY, 'H', index)

    def ARRAYLENGTH(self):
        self._add_normal_instruction(Opcode.ARRAYLENGTH)

    def ATHROW(self):
        self._add_instruction(Opcode.ATHROW, 1 - self._current_stack)

    def CHECKCAST(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.CHECKCAST, 'H', index)

    def INSTANCEOF(self, index: int):
        assert is_ushort(index)
        self._add_normal_instruction(Opcode.INSTANCEOF, 'H', index)

    def MONITORENTER(self):
        self._add_normal_instruction(Opcode.MONITORENTER)

    def MONITOREXIT(self):
        self._add_normal_instruction(Opcode.MONITOREXIT)

    # --- Not needed yet ---
    # def WIDE(self):
    #     raise NotImplementedError()

    def MULTIANEWARRAY(self, index: int, dim: int, count: int):
        assert is_ushort(index)
        assert is_ubyte(dim)
        self._add_instruction(Opcode.MULTIANEWARRAY, 1 - count, 'HB', index, dim)

    def IFNULL(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFNULL, index)

    def IFNONNULL(self, index: Optional[int] = None) -> int:
        return self._jump(Opcode.IFNONNULL, index)

    # --- Not needed yet ---
    # def GOTO_W(self, index: Optional[int] = None):
    #     raise NotImplementedError()

    # --- DEPRECATED ---
    # def JSR_W(self):
    #     raise NotImplementedError()
