from app.gen.descriptor import MethodDescriptor, ClassDesc, IntDesc, BooleanDesc, DoubleDesc, ArrayDesc


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
J_MAIN_DESCRIPTOR = MethodDescriptor([ArrayDesc(1, ClassDesc(JC_STRING))])


# --- To string methods ---

JSM_INT_TO_STRING = (JC_INT, 'toString', MethodDescriptor([IntDesc()], ClassDesc(JC_STRING)))
JSM_DOUBLE_TO_STRING = (JC_DOUBLE, 'toString', MethodDescriptor([DoubleDesc()], ClassDesc(JC_STRING)))
JSM_BOOLEAN_TO_STRING = (JC_BOOLEAN, 'toString', MethodDescriptor([BooleanDesc()], ClassDesc(JC_STRING)))


# --- Parse methods ---

JSM_INT_PARSE = (JC_INT, 'parseInt', MethodDescriptor([ClassDesc(JC_STRING)], IntDesc()))
JSM_DOUBLE_PARSE = (JC_DOUBLE, 'parseDouble', MethodDescriptor([ClassDesc(JC_STRING)], DoubleDesc()))
JSM_BOOLEAN_PARSE = (JC_BOOLEAN, 'parseBoolean', MethodDescriptor([ClassDesc(JC_STRING)], BooleanDesc()))


# --- String methods ---

JM_STRING_LENGTH = (JC_STRING, 'length', MethodDescriptor([], IntDesc()))
JM_STRING_CONCAT = (JC_STRING, 'concat', MethodDescriptor([ClassDesc(JC_STRING)], ClassDesc(JC_STRING)))
JM_STRING_EQUALS = (JC_STRING, 'equals', MethodDescriptor([ClassDesc(JC_OBJECT)], BooleanDesc()))
JM_STRING_SUBSTRING = (JC_STRING, 'substring', MethodDescriptor([IntDesc(), IntDesc()], ClassDesc(JC_STRING)))


# --- IO classes---

JC_SYSTEM = 'java/lang/System'
JC_PRINT_STREAM = 'java/io/PrintStream'
JC_INPUT_STREAM = 'java/io/InputStream'
JC_BUFF_READER = 'java/io/BufferedReader'
JC_INPUT_STREAM_READER = 'java/io/InputStreamReader'

JSF_STDIN = (JC_SYSTEM, 'in', ClassDesc(JC_INPUT_STREAM))
JSF_STDOUT = (JC_SYSTEM, 'out', ClassDesc(JC_PRINT_STREAM))


# --- IO methods ---

JM_PRINT = (JC_PRINT_STREAM, 'print', MethodDescriptor([ClassDesc(JC_STRING)]))
JM_READLINE = (JC_BUFF_READER, 'readLine', MethodDescriptor([], ClassDesc(JC_STRING)))
