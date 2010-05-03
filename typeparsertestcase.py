import unittest

import typeparser

class TypeParserTestCase(unittest.TestCase):
    def testFormatType(self):
        data = [
            ("u", "UInt32"),
            ("(ii)", "Struct<Int32,Int32>"),
            ("ai", "Array<Int32>"),
            ("a{si}", "Dict<String,Int32>"),
            ("a(ii)", "Array<Struct<Int32,Int32>>"),
            ]

        for src, expected in data:
            dst = typeparser.formatType(src)
            self.assertEqual(dst, expected)

if __name__ == "__main__":
    unittest.main()
# vi: ts=4 sw=4 et
