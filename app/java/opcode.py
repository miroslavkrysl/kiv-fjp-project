from enum import IntEnum
from typing import Optional


class Opcode(IntEnum):
    """
    Java bytecode instructions opcodes
    """

    NOOP = 0x00
    ACONST_NULL = 0x01
    ICONST_M1 = 0x02
    ICONST_0 = 0x03
    ICONST_1 = 0x04
    ICONST_2 = 0x05
    ICONST_3 = 0x06
    ICONST_4 = 0x07
    ICONST_5 = 0x08
    LCONST_0 = 0x09
    LCONST_1 = 0x0A
    FCONST_0 = 0x0B
    FCONST_1 = 0x0C
    FCONST_2 = 0x0D
    DCONST_0 = 0x0E
    DCONST_1 = 0x0F
    BIPUSH = 0x10
    SIPUSH = 0x11
    LDC = 0x12
    LDC_W = 0x13
    LDC2_W = 0x14
    ILOAD = 0x15
    LLOAD = 0x16
    FLOAD = 0x17
    DLOAD = 0x18
    ALOAD = 0x19
    ILOAD_0 = 0x1A
    ILOAD_1 = 0x1B
    ILOAD_2 = 0x1C
    ILOAD_3 = 0x1D
    LLOAD_0 = 0x1E
    LLOAD_1 = 0x1F
    LLOAD_2 = 0x20
    LLOAD_3 = 0x21
    FLOAD_0 = 0x22
    FLOAD_1 = 0x23
    FLOAD_2 = 0x24
    FLOAD_3 = 0x25
    DLOAD_0 = 0x26
    DLOAD_1 = 0x27
    DLOAD_2 = 0x28
    DLOAD_3 = 0x29
    ALOAD_0 = 0x2A
    ALOAD_1 = 0x2B
    ALOAD_2 = 0x2C
    ALOAD_3 = 0x2D
    IALOAD = 0x2E
    LALOAD = 0x2F
    FALOAD = 0x30
    DALOAD = 0x31
    AALOAD = 0x32
    BALOAD = 0x33
    CALOAD = 0x34
    SALOAD = 0x35
    ISTORE = 0x36
    LSTORE = 0x37
    FSTORE = 0x38
    DSTORE = 0x39
    ASTORE = 0x3A
    ISTORE_0 = 0x3B
    ISTORE_1 = 0x3C
    ISTORE_2 = 0x3D
    ISTORE_3 = 0x3E
    LSTORE_0 = 0x3F
    LSTORE_1 = 0x40
    LSTORE_2 = 0x41
    LSTORE_3 = 0x42
    FSTORE_0 = 0x43
    FSTORE_1 = 0x44
    FSTORE_2 = 0x45
    FSTORE_3 = 0x46
    DSTORE_0 = 0x47
    DSTORE_1 = 0x48
    DSTORE_2 = 0x49
    DSTORE_3 = 0x4A
    ASTORE_0 = 0x4B
    ASTORE_1 = 0x4C
    ASTORE_2 = 0x4D
    ASTORE_3 = 0x4E
    IASTORE = 0x4F
    LASTORE = 0x50
    FASTORE = 0x51
    DASTORE = 0x52
    AASTORE = 0x53
    BASTORE = 0x54
    CASTORE = 0x55
    SASTORE = 0x56
    POP = 0x57
    POP2 = 0x58
    DUP = 0x59
    DUP_X1 = 0x5A
    DUP_X2 = 0x5B
    DUP2 = 0x5C
    DUP2_X1 = 0x5D
    DUP2_X2 = 0x5E
    SWAP = 0x5F
    IADD = 0x60
    LADD = 0x61
    FADD = 0x62
    DADD = 0x63
    ISUB = 0x64
    LSUB = 0x65
    FSUB = 0x66
    DSUB = 0x67
    IMUL = 0x68
    LMUL = 0x69
    FMUL = 0x6A
    DMUL = 0x6B
    IDIV = 0x6C
    LDIV = 0x6D
    FDIV = 0x6E
    DDIV = 0x6F
    IREM = 0x70
    LREM = 0x71
    FREM = 0x72
    DREM = 0x73
    INEG = 0x74
    LNEG = 0x75
    FNEG = 0x76
    DNEG = 0x77
    ISHL = 0x78
    LSHL = 0x79
    ISHR = 0x7A
    LSHR = 0x7B
    IUSHR = 0x7C
    LUSHR = 0x7D
    IAND = 0x7E
    LAND = 0x7F
    IOR = 0x80
    LOR = 0x81
    IXOR = 0x82
    LXOR = 0x83
    IINC = 0x84
    I2L = 0x85
    I2F = 0x86
    I2D = 0x87
    L2I = 0x88
    L2F = 0x89
    L2D = 0x8A
    F2I = 0x8B
    F2L = 0x8C
    F2D = 0x8D
    D2I = 0x8E
    D2L = 0x8F
    D2F = 0x90
    I2B = 0x91
    I2C = 0x92
    I2S = 0x93
    LCMP = 0x94
    FCMPL = 0x95
    FCMPG = 0x96
    DCMPL = 0x97
    DCMPG = 0x98
    IFEQ = 0x99
    IFNE = 0x9A
    IFLT = 0x9B
    IFGE = 0x9C
    IFGT = 0x9D
    IFLE = 0x9E
    IF_ICMPEQ = 0x9F
    IF_ICMPNE = 0xA0
    IF_ICMPLT = 0xA1
    IF_ICMPGE = 0xA2
    IF_ICMPGT = 0xA3
    IF_ICMPLE = 0xA4
    IF_ACMPEQ = 0xA5
    IF_ACMPNE = 0xA6
    GOTO = 0xA7
    JSR = 0xA8
    RET = 0xA9
    TABLESWITCH = 0xAA
    LOOKUPSWITCH = 0xAB
    IRETURN = 0xAC
    LRETURN = 0xAD
    FRETURN = 0xAE
    DRETURN = 0xAF
    ARETURN = 0xB0
    RETURN = 0xB1
    GETSTATIC = 0xB2
    PUTSTATIC = 0xB3
    GETFIELD = 0xB4
    PUTFIELD = 0xB5
    INVOKEVIRTUAL = 0xB6
    INVOKESPECIAL = 0xB7
    INVOKESTATIC = 0xB8
    INVOKEINTERFACE = 0xB9
    INVOKEDYNoneMIC = 0xBA
    NEW = 0xBB
    NEWARRAY = 0xBC
    ANEWARRAY = 0xBD
    ARRAYLENGTH = 0xBE
    ATHROW = 0xBF
    CHECKCAST = 0xC0
    INSTANCEOF = 0xC1
    MONITORENTER = 0xC2
    MONITOREXIT = 0xC3
    WIDE = 0xC4
    MULTIANEWARRAY = 0xC5
    IFNULL = 0xC6
    IFNONNULL = 0xC7
    GOTO_W = 0xC8
    JSR_W = 0xC9


_STACK_DIFF = {
    Opcode.NOOP: 0,
    Opcode.ACONST_NULL: 1,
    Opcode.ICONST_M1: 1,
    Opcode.ICONST_0: 1,
    Opcode.ICONST_1: 1,
    Opcode.ICONST_2: 1,
    Opcode.ICONST_3: 1,
    Opcode.ICONST_4: 1,
    Opcode.ICONST_5: 1,
    Opcode.LCONST_0: 2,
    Opcode.LCONST_1: 2,
    Opcode.FCONST_0: 1,
    Opcode.FCONST_1: 1,
    Opcode.FCONST_2: 1,
    Opcode.DCONST_0: 2,
    Opcode.DCONST_1: 2,
    Opcode.BIPUSH: 1,
    Opcode.SIPUSH: 1,
    Opcode.LDC: 1,
    Opcode.LDC_W: 1,
    Opcode.LDC2_W: 2,
    Opcode.ILOAD: 1,
    Opcode.LLOAD: 2,
    Opcode.FLOAD: 1,
    Opcode.DLOAD: 2,
    Opcode.ALOAD: 1,
    Opcode.ILOAD_0: 1,
    Opcode.ILOAD_1: 1,
    Opcode.ILOAD_2: 1,
    Opcode.ILOAD_3: 1,
    Opcode.LLOAD_0: 2,
    Opcode.LLOAD_1: 2,
    Opcode.LLOAD_2: 2,
    Opcode.LLOAD_3: 2,
    Opcode.FLOAD_0: 1,
    Opcode.FLOAD_1: 1,
    Opcode.FLOAD_2: 1,
    Opcode.FLOAD_3: 1,
    Opcode.DLOAD_0: 2,
    Opcode.DLOAD_1: 2,
    Opcode.DLOAD_2: 2,
    Opcode.DLOAD_3: 2,
    Opcode.ALOAD_0: 1,
    Opcode.ALOAD_1: 1,
    Opcode.ALOAD_2: 1,
    Opcode.ALOAD_3: 1,
    Opcode.IALOAD: -1,
    Opcode.LALOAD: 0,
    Opcode.FALOAD: -1,
    Opcode.DALOAD: 0,
    Opcode.AALOAD: -1,
    Opcode.BALOAD: -1,
    Opcode.CALOAD: -1,
    Opcode.SALOAD: -1,
    Opcode.ISTORE: -1,
    Opcode.LSTORE: -2,
    Opcode.FSTORE: -1,
    Opcode.DSTORE: -2,
    Opcode.ASTORE: -1,
    Opcode.ISTORE_0: -1,
    Opcode.ISTORE_1: -1,
    Opcode.ISTORE_2: -1,
    Opcode.ISTORE_3: -1,
    Opcode.LSTORE_0: -2,
    Opcode.LSTORE_1: -2,
    Opcode.LSTORE_2: -2,
    Opcode.LSTORE_3: -2,
    Opcode.FSTORE_0: -1,
    Opcode.FSTORE_1: -1,
    Opcode.FSTORE_2: -1,
    Opcode.FSTORE_3: -1,
    Opcode.DSTORE_0: -2,
    Opcode.DSTORE_1: -2,
    Opcode.DSTORE_2: -2,
    Opcode.DSTORE_3: -2,
    Opcode.ASTORE_0: -1,
    Opcode.ASTORE_1: -1,
    Opcode.ASTORE_2: -1,
    Opcode.ASTORE_3: -1,
    Opcode.IASTORE: -3,
    Opcode.LASTORE: -4,
    Opcode.FASTORE: -3,
    Opcode.DASTORE: -4,
    Opcode.AASTORE: -3,
    Opcode.BASTORE: -3,
    Opcode.CASTORE: -3,
    Opcode.SASTORE: -3,
    Opcode.POP: -1,
    Opcode.POP2: -2,
    Opcode.DUP: 1,
    Opcode.DUP_X1: 1,
    Opcode.DUP_X2: 1,
    Opcode.DUP2: 2,
    Opcode.DUP2_X1: 2,
    Opcode.DUP2_X2: 2,
    Opcode.SWAP: 0,
    Opcode.IADD: -1,
    Opcode.LADD: -2,
    Opcode.FADD: -1,
    Opcode.DADD: -2,
    Opcode.ISUB: -1,
    Opcode.LSUB: -2,
    Opcode.FSUB: -1,
    Opcode.DSUB: -2,
    Opcode.IMUL: -1,
    Opcode.LMUL: -2,
    Opcode.FMUL: -1,
    Opcode.DMUL: -2,
    Opcode.IDIV: -1,
    Opcode.LDIV: -2,
    Opcode.FDIV: -1,
    Opcode.DDIV: -2,
    Opcode.IREM: -1,
    Opcode.LREM: -2,
    Opcode.FREM: -1,
    Opcode.DREM: -2,
    Opcode.INEG: 0,
    Opcode.LNEG: 0,
    Opcode.FNEG: 0,
    Opcode.DNEG: 0,
    Opcode.ISHL: -1,
    Opcode.LSHL: -1,
    Opcode.ISHR: -1,
    Opcode.LSHR: -1,
    Opcode.IUSHR: -1,
    Opcode.LUSHR: -1,
    Opcode.IAND: -1,
    Opcode.LAND: -2,
    Opcode.IOR: -1,
    Opcode.LOR: -2,
    Opcode.IXOR: -1,
    Opcode.LXOR: -2,
    Opcode.IINC: 0,
    Opcode.I2L: 1,
    Opcode.I2F: 0,
    Opcode.I2D: 1,
    Opcode.L2I: -1,
    Opcode.L2F: -1,
    Opcode.L2D: 0,
    Opcode.F2I: 0,
    Opcode.F2L: 1,
    Opcode.F2D: 1,
    Opcode.D2I: -1,
    Opcode.D2L: 0,
    Opcode.D2F: -1,
    Opcode.I2B: 0,
    Opcode.I2C: 0,
    Opcode.I2S: 0,
    Opcode.LCMP: -3,
    Opcode.FCMPL: -1,
    Opcode.FCMPG: -1,
    Opcode.DCMPL: -3,
    Opcode.DCMPG: -3,
    Opcode.IFEQ: -1,
    Opcode.IFNE: -1,
    Opcode.IFLT: -1,
    Opcode.IFGE: -1,
    Opcode.IFGT: -1,
    Opcode.IFLE: -1,
    Opcode.IF_ICMPEQ: -2,
    Opcode.IF_ICMPNE: -2,
    Opcode.IF_ICMPLT: -2,
    Opcode.IF_ICMPGE: -2,
    Opcode.IF_ICMPGT: -2,
    Opcode.IF_ICMPLE: -2,
    Opcode.IF_ACMPEQ: -2,
    Opcode.IF_ACMPNE: -2,
    Opcode.GOTO: 0,
    Opcode.JSR: 1,
    Opcode.RET: 0,
    Opcode.TABLESWITCH: -1,
    Opcode.LOOKUPSWITCH: -1,
    Opcode.IRETURN: -1,
    Opcode.LRETURN: -2,
    Opcode.FRETURN: -1,
    Opcode.DRETURN: -2,
    Opcode.ARETURN: -1,
    Opcode.RETURN: 0,
    Opcode.GETSTATIC: None,
    Opcode.PUTSTATIC: None,
    Opcode.GETFIELD: None,
    Opcode.PUTFIELD: None,
    Opcode.INVOKEVIRTUAL: None,
    Opcode.INVOKESPECIAL: None,
    Opcode.INVOKESTATIC: None,
    Opcode.INVOKEINTERFACE: None,
    Opcode.INVOKEDYNAMIC: None,
    Opcode.NEW: 1,
    Opcode.NEWARRAY: 0,
    Opcode.ANEWARRAY: 0,
    Opcode.ARRAYLENGTH: 0,
    Opcode.ATHROW: None,
    Opcode.CHECKCAST: 0,
    Opcode.INSTANCEOF: 0,
    Opcode.MONITORENTER: -1,
    Opcode.MONITOREXIT: -1,
    Opcode.WIDE: None,
    Opcode.MULTIANEWARRAY: None,
    Opcode.IFNULL: -1,
    Opcode.IFNONNULL: -1,
    Opcode.GOTO_W: None,
    Opcode.JSR_W: None
}


def stack_change(opcode: Opcode) -> Optional[int]:
    """
    Returns the effect of the instruction on the size of the stack
    = slots_produced - slots_consumed.
    If the value is None, the effect depends on concrete operand
    and needs to be computed.
    """
    return _STACK_DIFF[opcode]
