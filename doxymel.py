#!/usr/bin/env python
import sys
from optparse import OptionParser
from xml.etree import ElementTree as ET

import typeparser

DOX_TAG = "{http://www.canonical.com/dbus/dox.dtd}d"

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

def printPrototype(element):
    name = element.attrib.get("name")

    args = []
    for arg in element.findall("arg"):
        type = typeparser.formatType(arg.attrib.get("type"))
        argName = arg.attrib.get("name")
        args.append("%s %s" % (type, argName))
    argString = ", ".join(args)

    print "void %s(%s);" % (name, argString)

def printPropertyDox(element):
    name = element.attrib.get("name")
    type_ = typeparser.formatType(element.attrib.get("type"))
    access = element.attrib.get("access")
    print "/**"
    print "@property %s" % name

    doxElement = element.find(DOX_TAG)
    if doxElement is not None:
        print doxElement.text
    print
    print " @par Access:"
    print access
    print " */"
    print "Q_PROPERTY(%s %s)" % (type_, name)

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
        for name in "method", "signal":
            if name == "signal":
                print "signals:"
            elements = interface.findall(name)
            for element in elements:
                printMethodDox(element)
                printPrototype(element)

        elements = interface.findall("property")
        for element in elements:
            printPropertyDox(element)
        print "};"

    return 0


if __name__=="__main__":
    sys.exit(main())
# vi: ts=4 sw=4 et
