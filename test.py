import re

a = "\comenzar_conversacion"
print(a)

pattern = "\\\\\S+"
print(pattern)
print(re.match(pattern,a))