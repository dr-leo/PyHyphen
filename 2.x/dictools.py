# PyHyphen - hyphenation for Python
# module: dictools
'''
This module contains convenience functions to handle hyphenation dictionaries.
'''

import os, urllib2, csv, pickle, config, hyphen
from StringIO import StringIO
from  zipfile import ZipFile

__all__ = ['install', 'is_installed', 'uninstall', 'list_installed', 'install_dict_info']



def list_installed(directory = config.default_dict_path):
    '''Return a list of strings containing language and country codes of the
    dictionaries installed in 'directory' (default as declared in config.py).
    Example: file name = 'hyph_en_US.dic'. Return value: ['en_US']'''
    return [d[5:-4] for d in os.listdir(directory)
            if (d.startswith('hyph_') and d.endswith('.dic'))]

def is_installed(language, directory = config.default_dict_path):
    '''return True if 'directory' (default as declared in config.py)
    contains a dictionary file for 'language',
    False otherwise.
    By convention, 'language' should have the form 'll_CC'.
    Example: 'en_US' for US English.
    '''
    return (language in list_installed(directory))


def install(language, directory = config.default_dict_path,
            repos = config.default_repository):
    '''
    Download  and install a dictionary file.
    language: a string of the form 'll_CC'. Example: 'en_US' for English, USA
    directory: the installation directory. Defaults to the
    value given in config.py. After installation this is the package root of 'hyphen'
    repos: the url of the dictionary repository. (Default: as declared in config.py;
    after installation this is the OpenOffice repository for dictionaries.).'''
    url = ''.join((repos, hyphen.dict_info[language]['file_name']))
    s = urllib2.urlopen(url).read()
    z = ZipFile(StringIO(s))
    if z.testzip():
        raise IOError('The ZIP archive containing the dictionary is corrupt.')
    dic_filename = ''.join((hyphen.dict_info[language]['name'], '.dic'))
    dic_str = z.read(dic_filename)
    dest = open('/'.join((directory, dic_filename)), 'w')
    dest.write(dic_str)
    dest.close()

def uninstall(language, directory = config.default_dict_path):
    '''
    Uninstall the dictionary of the specified language.
    'language': is by convention a string of the form 'll_CC' whereby ll is the
        language code and CC the country code.
    'directory' (default: config.default_dict_path'. After installation of PyHyphen
    this is the package root of 'hyphen'.'''
    file_path = ''.join((directory, hyphen.dict_info[language]['name'], '.dic'))
    os.remove(file_path)


def install_dict_info(save = True, directory = config.default_dict_path):
    '''Loads the list of available dictionaries and stores it locally.'''
    
    l = urllib2.urlopen('http://ftp.osuosl.org/pub/openoffice/contrib/dictionaries/hyphavail.lst').readlines()
    
    stream = StringIO('\n'.join(l))
    d = csv.DictReader(stream, fieldnames = ['language_code', 'country_code',
        'name', 'long_descr', 'file_name'])
    avail_dict = {}
    for i in d:
        key = '_'.join((i['language_code'], i['country_code']))
        avail_dict[key] = i
    
    if save:
        file_path = directory + '/dict_info.pickle'
        f = open(file_path, 'w')
        pickle.dump(avail_dict, f)
        f.close()
    return avail_dict

    