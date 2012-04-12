# PyHyphen - hyphenation for Python
# module: dictools
'''
This module contains convenience functions to handle hyphenation dictionaries.
'''

import os, pickle, config, hyphen
from xml.etree.ElementTree import ElementTree
from StringIO import StringIO
from urllib2 import urlopen, URLError

__all__ = ['install', 'is_installed', 'uninstall', 'list_installed', 'install_dict_info']

class DictInfo:
    'Contains metadata on a hyphenation dictionary'
    
    def __init__(self, locales, path, url = None):
        '''
        locales: a list of locales for for which the dictionary is suitable, e.g. 'en_UK'
        path: the local path including filename of the dictionary file
        url: an  optional URL where the dictionary has been downloaded from
'''

        self.filepath = filepath
        self.locales = locales
        self.url = url


def list_installed(directory = config.default_dict_path):
    '''
    Return a list of locales for which dictionaries are installed.
    Deprecated since version 2.0. Use hyphen.dict_info.keys() instead.
    '''
    return hyphen.dict_info.keys()

def is_installed(language, directory = config.default_dict_path):
    '''return True if 'directory' (default as declared in config.py)
    contains a dictionary file for 'language',
    False otherwise.
    By convention, 'language' should have the form 'll_CC'.
    Example: 'en_US' for US English.
    '''
    return (language in hyphen.dict_info.keys())

    
    
    def uninstall(language, directory = config.default_dict_path):
        '''
        Uninstall the dictionary of the specified language.
        'language': is by convention a string of the form 'll_CC' whereby ll is the
            language code and CC the country code.
        'directory' (default: config.default_dict_path'. After installation of PyHyphen
        this is the package root of 'hyphen'.
        '''

        if hyphen.dict_info:
            file_path = ''.join((directory, '/', hyphen.dict_info[language]['name'], '.dic'))
        else:
            file_path = ''.join((directory, '/', 'hyph_', language, '.dic'))
        os.remove(file_path)


def install(language, directory = config.default_dict_path,
            repos = config.default_repository, use_description = True):
    '''
    Download  and install a dictionary file.
    language: a string of the form 'll_CC'. Example: 'en_US' for English, USA
    directory: the installation directory. Defaults to the
    value given in config.py. After installation this is the package root of 'hyphen'
    repos: the url of the dictionary repository. (Default: as declared in config.py;
    after installation this is the LibreOffice repository for dictionaries.).
    '''

    # Download the dictionaries.xcu file from the LibreOffice repository if needed
    if use_description:
        # Download the metadata file of the LibreOffice dictionary extension
        # first try  full language name; it won't work in all cases...
        language_ext_name = language
        descr_url = repos + language_ext_name + '/dictionaries.xcu'

        try:
            descr_file = urlopen(descr_url)
        except URLError: 
            # OK. So try with the country code.
            language_ext_name = language[:2]
            descr_url = repos + language_ext_name + '/dictionaries.xcu'
            try: 
                descr_file = urlopen(descr_url)
            except URLError:
                descr_file = None
            
    # Parse the xml file if it is present, and extract the data.     
    if   use_description and descr_file: 
        descr_tree = ElementTree(file = descr_file)


    # Find the nodes containing meta data of hyphenation dictionaries
    # Iterate over all nodes
    for node in descr_tree.iter('node'):
        # Check if node relates to a hyphenation dict.
        # We assume this is the case if an attribute value
        # contains the substring 'hyph'
        node_values = [i[1] for i in node.items()]
        for v in node_values if 'hyph' in v.lower():
            # Found one! So extract the data and construct the local record
            for property in node.getchildren():
                prop_values = [j[1] for j in property.items()]
                for pv in prop_values:
                    if pv.lower() = 'locations':
                        # Its only child's text is a list of strings of the form %origin%<filename>
                        # For simplicity, we only use the first filename in the list.
                        raw_dict_fn = property.getchildren()[0].text.split()[0]
                        dict_fn = raw_dict_fn[7:] # strip the prefix '%origin%'
                        dict_url = '/'.join((repos, language_ext_name, dict_fn))
                        
                        break # skip any other values of this property

                    elif pv.lower() = 'locales':
                        # Its only child's text is a list of locales. .
                        dict_locales = property.getchildren()[0].text.split()
                        
                        break # skip any other values of this property

                break # skip any other property of this node

            # Install the dictionary file
            dict_str = urlopen(dict_url).read()
            filepath = directory + '/' + dict_fn
            with open(filepath, 'w')  as dict_file:
                dict_file.write(dict_str)
            
            # Save the metadata
            # Generate a record for each locale, overwrite any existing ones
            new_dict  = DictInfo(dict_locales, filepath, url = dict_url) 
            for l in dict_locales: 
                hyphen.dict_info[l]
= new_dict
            
    # handle the case that there is no xml metadata
    else:
        # Download the dictionary guessing its URL
        dict_fn = ''.join(('hyph_dict_', language, '.dic'))
        dict_url = ''.join((repos, '/', dict_fn) 
        dict_str = urlopen(dict_url).read()
        filepath = directory + '/' + dict_fn
        with open(filepath, 'w')  as dict_file:
            dict_file.write(dict_str)
        # Store the metadata
        new_dict = DictInfo([language], filepath) # the URL is thus set to None.
        hyphen.dict_info[language] = new_dict
    # Save the modified metadata
    with open(directory + '/dict_info.pickle', 'wb') as f:
        pickle.dump(hyphen.dict_info, f)
        
        

        
        
        
            