#!/usr/bin/env python
import sys
import re
from optparse import OptionParser
from xml.etree import ElementTree as ET

DOX_TAG = "{http://www.ayatana.org/dbus/dox.dtd}d"

def printDox(element):
    for doxElement in element.findall(DOX_TAG):
        print "/**"
        print doxElement.text
        print " */"

def printMethodDox(element):
    print "/**"

    doxElement = element.find(DOX_TAG)
    if doxElement is not None:
        print doxElement.text

    for arg in element.findall("arg"):
        name = arg.attrib.get("name")
        direction = arg.attrib.get("direction")
        doc = arg.findtext(DOX_TAG, "")
        print "@param[%s] %s %s" % (direction, name, doc)

    print " */"

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

def printPrototype(element):
    name = element.attrib.get("name")

    args = []
    for arg in element.findall("arg"):
        type = formatType(arg.attrib.get("type"))
        argName = arg.attrib.get("name")
        args.append("%s %s" % (type, argName))
    argString = ", ".join(args)

    print "void %s(%s);" % (name, argString)

def main():
    parser = OptionParser("usage: %prog [options] <path/to/dbus.xml>")
    (options, args) = parser.parse_args()
    name = args[0]

    tree = ET.parse(name)
    printDox(tree)

    interfaces = tree.findall("interface")
    for interface in interfaces:
        printDox(interface)
        name = interface.attrib.get("name")
        print "class %s {" % name
        print "public:"
        for name in "property", "method", "signal":
            if name == "signal":
                print "signals:"
            elements = interface.findall(name)
            for element in elements:
                printMethodDox(element)
                printPrototype(element)
        print "};"

    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
