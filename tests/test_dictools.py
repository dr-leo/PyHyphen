from __future__ import unicode_literals
import os
import shutil
import tempfile
import unittest

import hyphen.dictools

class TestDictools(unittest.TestCase):

    def setUp(self):
        self.directory = tempfile.mkdtemp(prefix='pyhyphen')

    def tearDown(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

    def test_dict_directory_is_created_on_save(self):
        directory = os.path.join(self.directory, "mydir")
        self.assertFalse(os.path.exists(directory))
        dictionaries = hyphen.dictools.Dictionaries(directory)
        dictionaries.save()

        self.assertTrue(os.path.exists(directory))
        self.assertTrue(os.path.exists(dictionaries.path))

    def test_dict_directory_is_created_on_add(self):
        directory = os.path.join(self.directory, "mydir")
        self.assertFalse(os.path.exists(directory))
        dictionaries = hyphen.dictools.Dictionaries(directory)
        dictionaries.add("en", "content", ["en_US", "en_GB"], "http://source.com")

        self.assertTrue(os.path.exists(directory))
        self.assertTrue(os.path.exists(dictionaries.path))

    def test_list_installed(self):
        dictionaries = hyphen.dictools.Dictionaries(self.directory)
        dictionaries.add("fr_FR", b"content", ['fr_BE', 'fr_FR'], "http://pouac.com")

        self.assertTrue(hyphen.dictools.is_installed('fr_FR', directory=self.directory))
        self.assertEqual(['fr_BE', 'fr_FR'], hyphen.dictools.list_installed(self.directory))

    def test_uninstall(self):
        dictionaries = hyphen.dictools.Dictionaries(self.directory)
        dictionaries.add("fr_FR", b"content", ['fr_BE', 'fr_FR'], "http://pouac.com")

        hyphen.dictools.uninstall('fr_FR', directory=self.directory)
        self.assertFalse(hyphen.dictools.is_installed('fr_FR', directory=self.directory))

    def test_parse_dictionary_location(self):
        origin_url = "http://pouac.com"

        with open(os.path.join(os.path.dirname(__file__), "fixtures", "en", "dictionaries.xcu")) as xcu:
            url, locales = hyphen.dictools.parse_dictionary_location(xcu, origin_url, "en_US")
            self.assertEqual("http://pouac.com/hyph_en_US.dic", url)
            self.assertEqual(["en_US", "en_PH"], locales)

        with open(os.path.join(os.path.dirname(__file__), "fixtures", "fr_FR", "dictionaries.xcu")) as xcu:
            url, locales = hyphen.dictools.parse_dictionary_location(xcu, origin_url, "fr_FR")
            self.assertEqual("http://pouac.com/hyph_fr.dic", url)
            self.assertEqual(["fr_FR", "fr_BE", "fr_CA", "fr_CH", "fr_MC", "fr_LU"], locales)
