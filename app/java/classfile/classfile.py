import struct

from app.java.classfile.access import ClassAccess, FieldAccess


class ClassFileVersion:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    @classmethod
    def java11(cls):
        return cls(55, 0)


class ClassFile:
    MAGIC = 0xCAFEBABE

    def __init__(self, this_class: str):
        self.minor_version = 0
        self.major_version = 0
        self.constant_pool = ConstantPool()
        self.access_flags = ClassAccess.EMPTY
        self.this_class = self.constant_pool.const_class(this_class)
        self.super_class = 0
        self.interfaces = []
        self.fields = []
        self.methods = []
        self.attributes = []

    def add_field(self, ):

    def to_binary(self):
        data = bytearray()
        data += struct.pack('>I', 0xCAFEBABE)
        data += struct.pack('>H', self.version.minor)
        data += struct.pack('>H', self.version.major)
        data += struct.pack('>H', len(self.const_pool) + 1)

        for item in self.constant_pool:
            data += item.to_binary()

        data += struct.pack('>H', self.access_flags)

        this_class = struct.unpack('!H', cf.read(2))[0]
        self.class_name = self.const_pool[this_class - 1].name

        super_class = struct.unpack('!H', cf.read(2))[0]
        self.super_class = self.const_pool[super_class - 1].name

        interface_count = struct.unpack('!H', cf.read(2))[0]
        self.interfaces = []

        for i in range(interface_count):
            iface_index = struct.unpack('!H', cf.read(2))[0]
            self.interfaces.append(self.const_pool[iface_index - 1].name)

        field_count = struct.unpack('!H', cf.read(2))[0]
        self.fields = []
        for i in range(field_count):
            f = FieldInfo().from_reader(cf)
            self.replace_indexes(f.attributes)
            self.fields.append(f)

        method_count = struct.unpack('!H', cf.read(2))[0]
        self.methods = []
        for i in range(method_count):
            m = FieldInfo().from_reader(cf)
            self.replace_indexes(m.attributes)
            self.methods.append(m)

        attr_count = struct.unpack('!H', cf.read(2))[0]
        self.attributes = []
        for i in range(attr_count):
            a = AttributeInfo().from_reader(cf)
            self.attributes.append(a)

        self.replace_indexes(self.fields)
        self.replace_indexes(self.methods)
        self.replace_indexes(self.attributes)

class FieldInfo:
    def __init__(self, access_flags, name_index, descriptor_index, attributes):
        self.access_flags = FieldAccess.EMPTY
        self.name_index = 0
        self.descriptor_index = 0
        self.attributes = []

class Method:
    pass
