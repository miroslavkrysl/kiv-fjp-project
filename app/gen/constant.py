from abc import ABC


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


class JConstField(JConst):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def __hash__(self):
        return hash((self.class_index, self.name_and_type_index))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.class_index == other.class_index \
               and self.name_and_type_index == other.name_and_type_index


class JConstMethod(JConst):
    def __init__(self, class_index: int, name_and_type_index: int):
        self.class_index = class_index
        self.name_and_type_index = name_and_type_index

    def __hash__(self):
        return hash((self.class_index, self.name_and_type_index))

    def __eq__(self, other):
        return isinstance(other, self.__class__) \
               and self.class_index == other.class_index \
               and self.name_and_type_index == other.name_and_type_index
