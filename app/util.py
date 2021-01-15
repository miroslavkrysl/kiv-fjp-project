def is_byte(value: int) -> bool:
    return -128 <= value <= 127


def is_ubyte(value: int) -> bool:
    return 0 <= value <= 255


def is_short(value: int) -> bool:
    return -32768 <= value <= 32767


def is_ushort(value: int) -> bool:
    return 0 <= value <= 65535


def is_int(value: int) -> bool:
    return -2147483648 <= value <= 2147483647


def is_long(value: int) -> bool:
    return -9223372036854775808 <= value <= 9223372036854775807


def replace_escapes(s: str):
    esc = False
    result = ''

    for c in s:
        if esc:
            esc = False
            if c == 'n':
                result += '\n'
            if c == 't':
                result += '\t'
            if c == 'a':
                result += '\a'
            else:
                result += c
        else:
            if c == '\\':
                esc = True
            else:
                result += c

    return result

