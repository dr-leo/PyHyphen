import unittest
from hyphen import Hyphenator


class TestHyphenator(unittest.TestCase):

    def test_beautiful(self):
        h_en = Hyphenator('en_US')

        self.assertEqual(
            [['beau', 'tiful'], ['beauti', 'ful']],
            h_en.pairs('beautiful')
        )

        self.assertEqual(
            ['beau-', 'tiful'],
            h_en.wrap('beautiful', 6)
        )

        self.assertEqual(
            ['beauti-', 'ful'],
            h_en.wrap('beautiful', 7)
        )

        self.assertEqual(
            ['beau', 'ti', 'ful'],
            h_en.syllables('beautiful')
        )
