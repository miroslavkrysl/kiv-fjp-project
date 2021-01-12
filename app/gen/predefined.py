from app.gen.descriptor import MethodDescriptor, ObjectDesc, IntDesc, BooleanDesc, DoubleDesc, ArrayDesc


# --- Types ---

JC_OBJECT = 'java/lang/Object'
JC_INT = 'java/lang/Integer'
JC_DOUBLE = 'java/lang/Double'
JC_BOOLEAN = 'java/lang/Boolean'
JC_STRING = 'java/lang/String'


# --- Basic ---

J_CLINIT_NAME = '<clinit>'
J_CLINIT_DESCRIPTOR = MethodDescriptor([])
J_MAIN_NAME = 'main'
J_MAIN_DESCRIPTOR = MethodDescriptor([ArrayDesc(1, ObjectDesc(JC_STRING))])


# --- To string methods ---

JSM_INT_TO_STRING = (JC_INT, 'toString', MethodDescriptor([IntDesc()], ObjectDesc(JC_STRING)))
JSM_DOUBLE_TO_STRING = (JC_DOUBLE, 'toString', MethodDescriptor([DoubleDesc()], ObjectDesc(JC_STRING)))
JSM_BOOLEAN_TO_STRING = (JC_BOOLEAN, 'toString', MethodDescriptor([BooleanDesc()], ObjectDesc(JC_STRING)))


# --- Parse methods ---

JSM_INT_PARSE = (JC_INT, 'parseInt', MethodDescriptor([ObjectDesc(JC_STRING)], IntDesc()))
JSM_DOUBLE_PARSE = (JC_DOUBLE, 'parseDouble', MethodDescriptor([ObjectDesc(JC_STRING)], DoubleDesc()))
JSM_BOOLEAN_PARSE = (JC_BOOLEAN, 'parseBoolean', MethodDescriptor([ObjectDesc(JC_STRING)], BooleanDesc()))


# --- String methods ---

JM_STRING_LENGTH = (JC_STRING, 'length', MethodDescriptor([], IntDesc()))
JM_STRING_CONCAT = (JC_STRING, 'concat', MethodDescriptor([ObjectDesc(JC_STRING)], ObjectDesc(JC_STRING)))
JM_STRING_EQUALS = (JC_STRING, 'equals', MethodDescriptor([ObjectDesc(JC_OBJECT)], BooleanDesc()))
JM_STRING_SUBSTRING = (JC_STRING, 'substring', MethodDescriptor([IntDesc(), IntDesc()], ObjectDesc(JC_STRING)))


# --- IO classes---

JC_SYSTEM = 'java/lang/System'
JC_PRINT_STREAM = 'java/io/PrintStream'
JC_INPUT_STREAM = 'java/io/InputStream'
JC_BUFF_READER = 'java/io/BufferedReader'
JC_INPUT_STREAM_READER = 'java/io/InputStreamReader'

JSF_STDIN = (JC_SYSTEM, 'in', ObjectDesc(JC_INPUT_STREAM))
JSF_STDOUT = (JC_SYSTEM, 'out', ObjectDesc(JC_PRINT_STREAM))


# --- IO methods ---

JM_PRINT = (JC_PRINT_STREAM, 'print', MethodDescriptor([ObjectDesc(JC_STRING)]))
JM_READLINE = (JC_BUFF_READER, 'readLine', MethodDescriptor([], ObjectDesc(JC_STRING)))
