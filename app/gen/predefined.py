from app.gen.descriptor import MethodDescriptor, ObjectDesc

JAVA_STRING_CLASS = ObjectDesc('String')
JAVA_STDIN_CLASS = ObjectDesc('System.in')
JAVA_STDOUT_CLASS = ObjectDesc('System.out')
JAVA_BUFF_READER_CLASS = ObjectDesc('java.io.BufferedReader')
JAVA_INPUT_STREAM_READER_CLASS = ObjectDesc('java.io.InputStreamReader')
JAVA_PRINT = (JAVA_STDOUT_CLASS, 'print', MethodDescriptor([JAVA_STRING_CLASS]))
JAVA_READLINE = (JAVA_BUFF_READER_CLASS, 'readLine', MethodDescriptor([], JAVA_STRING_CLASS))
