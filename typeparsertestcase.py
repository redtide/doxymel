import unittest

import typeparser

class TypeParserTestCase(unittest.TestCase):
    def testFormatType(self):
        data = [
            ("u", "u"),
            ("(ii)", "struct(ii)"),
            ("ai", "array<i>"),
            ("a{si}", "dict<s,i>"),
            ("a(ii)", "array<struct(ii)>"),
            ]

        for src, expected in data:
            dst = typeparser.formatType(src)
            self.assertEqual(dst, expected)

if __name__ == "__main__":
    unittest.main()
# vi: ts=4 sw=4 et
