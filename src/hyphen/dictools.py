# PyHyphen - hyphenation for Python
# module: dictools
'''
This module contains convenience functions to manage hyphenation dictionaries.
'''

import json
import os
import appdirs
import  requests 


__all__ = ['install', 'is_installed', 'uninstall', 'list_installed']

# default location to store hyphenation dictionaries
DEFAULT_DICT_PATH = appdirs.user_data_dir("pyhyphen", appauthor=False)

# Where PyHyphen tries to retrieve dictionaries for download
DEFAULT_REPOSITORY = 'https://cgit.freedesktop.org/libreoffice/dictionaries/plain/'

# Incomplete list of languages for which there are dictionaries in the 
# default repository.
LANGUAGES = [
    "af_ZA", "be_BY", "bg_BG", "cs_CZ", 
    "da_DK", "de_AT", "de_CH", "de_DE", 
    "el_GR", "en_GB", "en_US", "es", "et_EE", 
    "fr", "gl", "hr_HR", "hu_HU", "id_ID", "is", 
    "it_IT", "lt", "lv_LV", "nl_NL", "nb_NO", 
    "nn_NO", "pl_PL", "pt_BR", "pt_PT", 
    "ro_RO", "ru_RU", "sk_SK", "sl_SI",
    "sq_AL", "sr-Latn", "sr", "sv", 
    "te_IN", "uk_UA", "zu_ZA"
]


class Dictionaries:

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
                with open(self.path, 'rb') as f:
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
        with open(self.path, "wt") as f:
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


def install(language, directory=None, repos=None, use_description=True, overwrite=False, 
    **request_args):
    '''
    Download  and install a dictionary file.

    language (str): code of the form 'll_CC'. Example: 'en_US' for English, USA
    directory (str): the installation directory. (Default: user data directory)
    repos (str): the url of the dictionary repository. (Default: the
        libreoffice dictionary repo)
    use_description (bool): if True, parse dictionaries.xcu file to
        automatically find the appropriate dictionary.
    overwrite (bool): if True, overwrite any existing dictionary. Default: False
    **request_args: additional kwargs to be passed to `requests.get()` for HTTP configuration

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
        dict_url, locales = find_dictionary_location(repos, language, **request_args)
    if not dict_url:
        # handle the case that there is no xml metadata: we just guess its url
        dict_url = '/'.join((repos, language, 'hyph_' + language + '.dic'))
        locales = [language]

    # Install the dictionary file
    response = requests.get(dict_url, **request_args)
    response.raise_for_status()
    dict_content = response.content
    return Dictionaries(directory).add(language, dict_content, locales, dict_url)


def find_dictionary_location(repos, language, **request_args):
    '''
    Find the location of a language dictionary from an xcu file from the LibreOffice repo.
    Any kwargs will be passed to `requests.get()` to configure the HTTP connection.
    Raise an IOError if the dictionary location could not be found in the xcu file.
    '''
    # Download the dictionaries.xcu file from the LibreOffice repository if needed
    # This is an XML file that lists all the available dictionaries for that language.
    # First, try full language name; it won't work in all cases...
    origin_url = repos + language
    descr_file = _download_dictionaries_xcu(origin_url, **request_args)
    if descr_file is None and len(language) > 2:
        # OK. So try with the country code.
        origin_url = repos + language[:2]
        descr_file = _download_dictionaries_xcu(origin_url, **request_args)

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
    from xml.etree import ElementTree 

    descr_tree = ElementTree.fromstring(descr_file)

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
        for prop in node:
            for _pk, pv in prop.items():
                if pv.lower() == 'locations':
                    # Its only child's text is a list of strings of the form %origin%<filename>
                    # For simplicity, we only use the first filename in the
                    # list.
                    dict_location = prop[0].text.split()[0]
                elif pv.lower() == 'locales':
                    # Its only child's text is a list of locales.
                    locales = prop[0].text.replace(
                        '-', '_').split()
                    # break # skip any other values of this property
        if language in locales and dict_location:
            # strip the prefix '%origin%'
            dict_url = origin_url + '/' + dict_location[9:]
            return dict_url, locales

    return None, []


def _download_dictionaries_xcu(origin_url, **request_args):
    '''
    Try to download dictionaries.xcu from the url. In case of error, return None.
    Any **request_args are passed to `requests.get()` to configure the HTTP connection.
    '''
    url = origin_url + '/dictionaries.xcu'
    response = requests.get(url, **request_args)
    # Return the content if received.
    # In case of an HTTP error, return the response.
    # HTTP errors are silently dropped. Fix this?
    if response.status_code == 200:
        return response.content 
