from typing import Tuple, Dict

from app.gen.classfile.classfile import ClassFile
from app.gen.cfcode import CodeBuilder
from app.gen.descriptor import MethodDescriptor, FieldDescriptor


class Field:
    def __init__(self, name, descriptor):
        self.name = name
        self.descriptor: MethodDescriptor = descriptor

    def __str__(self):
        return '{} {}'.format(
            self.descriptor,
            self.name)


class Method:
    def __init__(self, name, descriptor):
        self._name = name
        self._descriptor: MethodDescriptor = descriptor
        self._code: CodeBuilder = CodeBuilder()
        # TODO: initialize code locals for parameters

    @property
    def name(self) -> str:
        return self._name

    @property
    def descriptor(self) -> MethodDescriptor:
        return self._descriptor

    @property
    def code(self) -> CodeBuilder:
        return self.code

    def __str__(self):
        return '{} {}({})'.format(
            self.descriptor.ret,
            self._name,
            ', '.join(map(lambda p: str(p), self.descriptor.params)))


class Class:
    def __init__(self, name, public=False):
        self._name: str = name
        self._public: bool = public
        self._fields: Dict[Tuple[str, FieldDescriptor], Field] = {}
        self._methods: Dict[Tuple[str, MethodDescriptor], Method] = {}

    def method(self, name: str, descriptor: MethodDescriptor):
        method = self._methods.get((name, descriptor))

        if method is None:
            method = Method(name, descriptor)
            self._methods[(name, descriptor)] = method

        return method

    def field(self, name: str, descriptor: FieldDescriptor) -> Field:
        field = self._fields.get((name, descriptor))

        if field is None:
            field = Field(name, descriptor)
            self._fields[(name, descriptor)] = field

        return field

    def to_class_file(self) -> ClassFile:
        # TODO
        pass

