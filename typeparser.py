import re

dictRx = re.compile("a{" \
    + "(.)" # key \
    + "([^}]+)" # value \
    + "}")

arrayStructRx = re.compile("a\(" \
    + "([^)]+)" # key \
    + "\)")

arraySimpleRx = re.compile("a(.)")

structRx = re.compile("\("
    + "([^)]+)" # key \
    + "\)")

def formatType(type):
    # FIXME: replace with proper parser
    type = dictRx.sub(r"D<\1,\2>", type)
    type = arrayStructRx.sub(r"A<(\1)>", type)
    type = arraySimpleRx.sub(r"A<\1>", type)
    type = structRx.sub(r"S(\1)", type)

    type = type.replace("D", "dict")
    type = type.replace("A", "array")
    type = type.replace("S", "struct")
    return type

# vi: ts=4 sw=4 et
