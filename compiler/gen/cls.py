from typing import Tuple, Dict

from compiler.gen.code import Code
from compiler.gen.constant import ConstantPool
from compiler.gen.descriptor import MethodDescriptor, FieldDescriptor, IntDesc, LongDesc, FloatDesc, DoubleDesc, ClassDesc, \
    ArrayDesc
from compiler.gen.predefined import JC_OBJECT


class Field:
    def __init__(self, name: str, descriptor: FieldDescriptor, constant_pool: ConstantPool):
        self._constant_pool = constant_pool
        self._name_index: int = constant_pool.field_name(name)
        self._descriptor_index: int = constant_pool.field_descriptor(descriptor)

    @property
    def name_index(self):
        return self._name_index

    @property
    def descriptor_index(self):
        return self._descriptor_index


class Method:
    def __init__(self, name: str, descriptor: MethodDescriptor, constant_pool: ConstantPool):
        self._constant_pool = constant_pool
        self._name_index: int = constant_pool.method_name(name)
        self._descriptor_index: int = constant_pool.method_descriptor(descriptor)
        self._code: Code = Code(constant_pool)

        # setup local variables
        for p in descriptor.params_descriptors:
            if isinstance(p, IntDesc):
                self._code.variable_int()
            elif isinstance(p, LongDesc):
                self._code.variable_long()
            elif isinstance(p, FloatDesc):
                self._code.variable_float()
            elif isinstance(p, DoubleDesc):
                self._code.variable_double()
            elif isinstance(p, ClassDesc) or isinstance(p, ArrayDesc):
                self._code.variable_reference()

    @property
    def name_index(self) -> int:
        return self._name_index

    @property
    def descriptor_index(self) -> int:
        return self._descriptor_index

    @property
    def code(self) -> Code:
        return self._code


class Class:
    def __init__(self, name):
        self._constant_pool = ConstantPool()
        self._this_class: int = self._constant_pool.class_ref(name)
        self._super_class: int = self._constant_pool.class_ref(JC_OBJECT)
        self._fields: Dict[Tuple[str, FieldDescriptor], Field] = {}
        self._methods: Dict[Tuple[str, MethodDescriptor], Method] = {}

    def method(self, name: str, descriptor: MethodDescriptor) -> Method:
        """
        Get the method by name and descriptor or create one if not exists.
        :param name: Name of the method.
        :param descriptor: Descriptor of the method.
        :return: The already existing or a newly created method.
        """
        method = self._methods.get((name, descriptor))

        if method is None:
            method = Method(name, descriptor, self._constant_pool)
            self._methods[(name, descriptor)] = method

        return method

    def field(self, name: str, descriptor: FieldDescriptor) -> Field:
        """
        Get the field by name and descriptor or create one if not exists.
        :param name: Name of the field.
        :param descriptor: Descriptor of the field.
        :return: The already existing or newly created field.
        """
        field = self._fields.get((name, descriptor))

        if field is None:
            field = Field(name, descriptor, self._constant_pool)
            self._fields[(name, descriptor)] = field

        return field

    @property
    def methods(self):
        return self._methods.items()

    @property
    def fields(self):
        return self._fields.items()

    @property
    def constant_pool(self) -> ConstantPool:
        return self._constant_pool

    @property
    def this_class(self):
        return self._this_class

    @property
    def super_class(self):
        return self._super_class
