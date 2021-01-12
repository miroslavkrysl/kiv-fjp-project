from app.gen.descriptor import MethodDescriptor, ObjectDesc, IntDesc, BooleanDesc, DoubleDesc

# --- Types ---

JC_OBJECT = ObjectDesc('java/lang/Object')
JC_INT = ObjectDesc('java/lang/Integer')
JC_DOUBLE = ObjectDesc('java/lang/Double')
JC_BOOLEAN = ObjectDesc('java/lang/Boolean')
JC_STRING = ObjectDesc('java/lang/String')


# --- To string methods ---

JSM_INT_TO_STRING = (JC_INT, 'toString', MethodDescriptor([IntDesc()], JC_STRING))
JSM_DOUBLE_TO_STRING = (JC_DOUBLE, 'toString', MethodDescriptor([DoubleDesc()], JC_STRING))
JSM_BOOLEAN_TO_STRING = (JC_BOOLEAN, 'toString', MethodDescriptor([BooleanDesc()], JC_STRING))


# --- Parse methods ---

JSM_INT_PARSE = (JC_INT, 'parseInt', MethodDescriptor([JC_STRING], JC_INT))
JSM_DOUBLE_PARSE = (JC_DOUBLE, 'parseDouble', MethodDescriptor([JC_STRING], JC_DOUBLE))
JSM_BOOLEAN_PARSE = (JC_BOOLEAN, 'parseBoolean', MethodDescriptor([JC_STRING], JC_BOOLEAN))


# --- String methods ---

JM_STRING_LENGTH = (JC_STRING, 'length', MethodDescriptor([], IntDesc()))
JM_STRING_CONCAT = (JC_STRING, 'concat', MethodDescriptor([JC_STRING], JC_STRING))
JM_STRING_EQUALS = (JC_STRING, 'equals', MethodDescriptor([JC_OBJECT], BooleanDesc()))
JM_STRING_SUBSTRING = (JC_STRING, 'substring', MethodDescriptor([IntDesc(), IntDesc()], JC_STRING))


# --- IO classes---

JC_SYSTEM = ObjectDesc('java/lang/System')
JC_PRINT_STREAM = ObjectDesc('java/io/PrintStream')
JC_INPUT_STREAM = ObjectDesc('java/io/InputStream')
JC_BUFF_READER = ObjectDesc('java/io/BufferedReader')
JC_INPUT_STREAM_READER = ObjectDesc('java/io/InputStreamReader')

JSF_STDIN = (JC_SYSTEM, 'in', JC_INPUT_STREAM)
JSF_STDOUT = (JC_SYSTEM, 'out', JC_PRINT_STREAM)


# --- IO methods ---

JM_PRINT = (JC_PRINT_STREAM, 'print', MethodDescriptor([JC_STRING]))
JM_READLINE = (JC_BUFF_READER, 'readLine', MethodDescriptor([], JC_STRING))
