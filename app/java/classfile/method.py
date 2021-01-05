from app.java.classfile.access import MethodAccess


class Method:
    def __init__(self, name_index: int, descriptor_index: int):
        self.access_flags = MethodAccess.EMPTY
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes = []

    def add_flags(self, flags: MethodAccess):
        self.access_flags |= flags

    def add_code(self, code: Code):
        self.attributes = flags

class Code:
    def __init__(self):
        self.instructions = bytearray()

    def 