# PyHyphen - hyphenation for Python
# module: dictools
'''
This module contains convenience functions to manage hyphenation dictionaries.
'''
from __future__ import unicode_literals

import json
import os

import appdirs
from six.moves import urllib


__all__ = ['install', 'is_installed', 'uninstall', 'list_installed']


DEFAULT_DICT_PATH = appdirs.user_data_dir("pyhyphen", appauthor=False)
DEFAULT_REPOSITORY = 'http://cgit.freedesktop.org/libreoffice/dictionaries/plain/'
# This is a list of languages supported by PyHyphen. In the following, language
# codes are assumed to be in this list.
LANGUAGES = ['af_ZA', 'an_ES', 'ar', 'be_BY', 'bg_BG', 'bn_BD', 'br_FR', 'ca',
             'cs_CZ', 'da_DK', 'de', 'el_GR', 'en', 'es_ES', 'et_EE', 'fr_FR',
             'gd_GB', 'gl', 'gu_IN', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU',
             'it_IT', 'ku_TR', 'lt_LT', 'lv_LV', 'ne_NP', 'nl_NL', 'no',
             'oc_FR', 'pl_PL', 'prj', 'pt_BR', 'pt_PT', 'ro', 'ru_RU', 'si_LK',
             'sk_SK', 'sl_SI', 'sr', 'sv_SE', 'sw_TZ', 'te_IN', 'th_TH',
             'uk_UA', 'zu_ZA']


class Dictionaries(object):

    def __init__(self, directory=None):
        self.directory = directory or DEFAULT_DICT_PATH
        self._data = None

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @property
    def path(self):
        return os.path.join(self.directory, 'dictionaries.json')

    @property
    def data(self):
        if self._data is None:
            if os.path.exists(self.path):
                with open(self.path) as f:
                    self._data = json.load(f)
            else:
                self._data = {}
        return self._data

    def installed_languages(self):
        return sorted(self.data.keys())

    def is_installed(self, language):
        return language in self.data

    def filepath(self, language):
        return os.path.join(self.directory, self.data[language]["file"])

    def add(self, language, content, locales, url):
        """
        Return the path to which the file was saved.
        """
        # Save to file
        filename = 'hyph_' + language + ".dic"
        filepath = os.path.join(self.directory, filename)
        with open(filepath, 'wb') as f:
            f.write(content)

        # Add file to configuration
        for locale in locales:
            self.data[locale] = {
                "file": filename,
                "url": url
            }
        self.save()

        return filepath

    def remove(self, language):
        """
        Remove language and all languages that share the same file.
        """
        if language not in self.data:
            return

        # Remove languages from file
        filename = self.data[language]["file"]
        languages = [language for language,
                     props in self.data.items() if props["file"] == filename]
        for locale in languages:
            self.data.pop(locale)
        self.save()

        # Remove file
        filepath = os.path.join(self.directory, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    def save(self):
        # Access data to make sure it's properly loaded
        data = self.data
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    def reload(self):
        self._data = None


def list_installed(directory=None):
    '''
    Return a list of locales for which dictionaries are installed.
    '''
    return Dictionaries(directory).installed_languages()


def is_installed(language, directory=None):
    '''Return True if the dictionary was already installed in the 'directory'.
    False otherwise.

    By convention, 'language' should have the form 'll_CC'.
    Example: 'en_US' for US English.
    '''
    return Dictionaries(directory).is_installed(language)


def uninstall(language, directory=None):
    '''
    Uninstall the dictionary of the specified language from the directory.

    'language': is by convention a string of the form 'll_CC' whereby ll is the
        language code and CC the country code.
    '''
    Dictionaries(directory).remove(language)


def install(language, directory=None, repos=None, use_description=True, overwrite=False):
    '''
    Download  and install a dictionary file.

    language (str): code of the form 'll_CC'. Example: 'en_US' for English, USA
    directory (str): the installation directory. (Default: user data directory)
    repos (str): the url of the dictionary repository. (Default: the
        libreoffice dictionary repo)
    use_description (bool): if True, parse dictionaries.xcu file to
        automatically find the appropriate dictionary.
    overwrite (bool): if True, overwrite any existing dictionary. Default: False

    Return the path to the file that was downloaded or is already installed.
    '''
    if not overwrite:
        dictionaries = Dictionaries(directory)
        if dictionaries.is_installed(language):
            return dictionaries.filepath(language)

    if not repos:
        repos = DEFAULT_REPOSITORY

    dict_url = None
    if use_description:
        # Find the dictionary location from the dictionaries.xcu description
        dict_url, locales = find_dictionary_location(repos, language)
    if not dict_url:
        # handle the case that there is no xml metadata: we just guess its url
        dict_url = repos + 'hyph_dict_' + language + '.dic'
        locales = [language]

    # Install the dictionary file
    dict_content = urllib.request.urlopen(dict_url).read()
    return Dictionaries(directory).add(language, dict_content, locales, dict_url)


def find_dictionary_location(repos, language):
    '''
    Find the location of a language dictionary from an xcu file from the LibreOffice repo.
    Raise an IOError if the dictionary location could not be found in the xcu file.
    '''
    # Download the dictionaries.xcu file from the LibreOffice repository if needed
    # This is an XML file that lists all the available dictionaries for that language.
    # First, try full language name; it won't work in all cases...
    origin_url = repos + language
    descr_file = _download_dictionaries_xcu(origin_url)
    if descr_file is None and len(language) > 2:
        # OK. So try with the country code.
        origin_url = repos + language[:2]
        descr_file = _download_dictionaries_xcu(origin_url)

    if not descr_file:
        return None, []

    # Parse the xml file if it is present, and extract the data.
    dict_url, locales = parse_dictionary_location(
        descr_file, origin_url, language)

    if not dict_url:
        # Catch the case that there is no hyphenation dict
        # for this language:
        raise IOError(
            'Cannot find hyphenation dictionary for language ' + language + '.')

    return dict_url, locales


def parse_dictionary_location(descr_file, origin_url, language):
    '''
    Parse the dictionaries.xcu file to find the url of the most appropriate
    hyphenation dictionary.

    Args:
        descr_file (file object)
        origin_url (unicode): base url from which the xcu file was downloaded
        language (unicode): language code
    Return:
        url (unicode)
        locales (unicode list)
    '''
    try:
        from xml.etree.cElementTree import ElementTree
    except ImportError:
        from xml.etree.ElementTree import ElementTree

    descr_tree = ElementTree(file=descr_file)

    # Find the nodes containing meta data of hyphenation dictionaries
    # Iterate over all nodes
    for node in descr_tree.iter('node'):
        # Check if node relates to a hyphenation dict.
        # We assume this is the case if an attribute value
        # contains the substring 'hyphdic'
        node_is_hyphen = any(
            [name for name, value in node.items() if 'hyphdic' in value.lower()])

        if not node_is_hyphen:
            continue

        # Found a hyphenation dict! So extract the data and construct the local
        # record
        locales = []
        dict_location = None
        for prop in node.getchildren():
            for _pk, pv in prop.items():
                if pv.lower() == 'locations':
                    # Its only child's text is a list of strings of the form %origin%<filename>
                    # For simplicity, we only use the first filename in the
                    # list.
                    dict_location = prop.getchildren()[0].text.split()[0]
                elif pv.lower() == 'locales':
                    # Its only child's text is a list of locales.
                    locales = prop.getchildren()[0].text.replace(
                        '-', '_').split()
                    # break # skip any other values of this property
        if language in locales and dict_location:
            # strip the prefix '%origin%'
            dict_url = origin_url + '/' + dict_location[9:]
            return dict_url, locales

    return None, []


def _download_dictionaries_xcu(origin_url):
    '''
    Try to download dictionaries.xcu from the url. In case of error, return None.
    '''
    url = origin_url + '/dictionaries.xcu'
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError:
        return None
