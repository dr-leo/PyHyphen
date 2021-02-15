import unittest
import hyphen
from hyphen import textwrap2




class TestTextwrap2(unittest.TestCase):

    def test_fill(self):
        hyphenator = hyphen.Hyphenator("en_US")
        wrapped = textwrap2.fill("A thing of beauty is a joy forever.",
                                 width=10, use_hyphenator=hyphenator)
        # Note that this wrapping depends on the content of the language dictionary
        self.assertEqual("""A thing of
beauty is
a joy for-
ever.""", wrapped)
