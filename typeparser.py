def formatType(type):
    lst = sig_to_type_list(type)
    return "".join(lst)

"""
Following code is a modified version of dbus_utils.py, d-feet source code
"""

def convert_complex_type(subsig):
    result = None
    len_consumed = 0

    c = subsig[0]

    c_lookahead = ''
    try:
        c_lookahead = subsig[1]
    except:
        c_lookahead = ''

    if c == 'a' and c_lookahead == '{':  # handle dicts as a special case array
        ss = subsig[2:]
        # account for the trailing '}'
        len_consumed = 3
        c = ss[0]
        key = convert_simple_type(c)

        ss = ss[1:]

        (r, lc) = convert_complex_type(ss)
        if r:
            subtypelist = [key, r]
            len_consumed += lc + 1
        else:
            value = convert_simple_type(ss[0])
            subtypelist = [key, value]
            len_consumed += 1

        result = 'Dict<' + ','.join(subtypelist) + '>'

    elif c == 'a':                       # handle an array 
        ss = subsig[1:]
        (r, lc) = convert_complex_type(ss)
        if r:
            subtypelist = [r]
            len_consumed = lc + 1
        else:
            subtypelist = sig_to_type_list(ss[0])
            len_consumed = 1

        result = 'Array<' + ','.join(subtypelist) + '>'
    elif c == '(':                       # handle structs
        # iterate over sig until paren_count == 0
        paren_count = 1
        i = 0
        ss = subsig[1:]
        len_ss = len(ss)
        while i < len_ss and paren_count != 0:
            if ss[i] == '(':
                paren_count+=1
            elif ss[i] == ')':
                paren_count-=1

            i+=1
        
        len_consumed = i
        ss = ss[0:i-1]
        result = 'Struct<' + ','.join(sig_to_type_list(ss)) + '>'

    return (result, len_consumed)

def convert_simple_type(c):
    result = None

    if c == 'n':
        result = 'Int16'
    elif c == 'q':
        result = 'UInt16'
    elif c == 'i':
        result = 'Int32'
    elif c == 'u':
        result = 'UInt32'
    elif c == 'x':
        result = 'Int64'
    elif c == 't':
        result = 'UInt64'
    elif c == 's':
        result = 'String'
    elif c == 'b':
        result = 'Boolean'
    elif c == 'y':
        result = 'Byte'
    elif c == 'o':
        result = 'ObjectPath'
    elif c == 'g':
        result = 'Signature'
    elif c == 'd':
        result = 'Double'
    elif c == 'v':
        result = 'Variant'

    return result

def sig_to_type_list(sig):
    i = 0
    result = []

    sig_len = len(sig)
    while i < sig_len:
        c = sig[i]
        type = convert_simple_type(c)
        if not type:
            (type, len_consumed) = convert_complex_type(sig[i:])
            if not type:
                type = 'Error(' + c + ')'

            i += len_consumed

        if isinstance(type, list):
            result.extend(type)
        else:
            result.append(type)

        i+=1

    return result

# vi: ts=4 sw=4 et
