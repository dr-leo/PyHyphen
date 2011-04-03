# Without prejudice to the license governing the use of
# the Python standard module textwrap on which textwrap2 is based,
# PyHyphen is licensed under the same terms as the underlying C library hyphen-2.3.1.
# The essential parts of the license terms of libhyphen are quoted hereunder.
#
#
#
#
# Extract from the license information of hyphen-2.3.1 library
# ============================================================
#
#
#
# GPL 2.0/LGPL 2.1/MPL 1.1 tri-license
#
# Software distributed under these licenses is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the licences
# for the specific language governing rights and limitations under the licenses.
#
# The contents of this software may be used under the terms of
# the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL",



'''
hyphen - hyphenation for Python

This package adds hyphenation functionality to the Python programming language.
You may also wish to have a look at the module 'textwrap2' distributed jointly
with this package.

Contents

1. Overview
2. Code examples




1. Overview

The gole of the PyHyphen project is to add hyphenation functionality to the Python programming
language. PyHyphen consists of the package 'hyphen' and the module 'textwrap2'

1.1 The hyphen package contains:
    - at top level the definition of the class 'Hyphenator' each instance of which
      can hyphenate words using a dictionary compatible with the hyphenation feature of
      OpenOffice and Mozilla.
      The former class 'hyphenator' is deprecated
      as of version 0.10 as class names conventially begin with a capital letter.
    - the module dictools contains useful functions such as automatic downloading and
    - the module dictools contains useful functions automatically downloading and
      installing dictionaries from a configurable repository. By default, the
      OpenOffice repository is used.
     - config is a configuration file initialized at install time with default values
       for the directory where dictionaries are searched, and the repository for future
       downloads of dictionaries.
     - hyph_en_US.dic is the hyphenation dictionary for US English as found on
       the OpenOffice.org repository.
    - 'hnjmodule' is the C extension module that does all the ground work. It
      contains the C library hyphen-2.4. I cannot think of a reason
      to access the wrapper class exported by 'hnjmodule' directly rather than through
      the top level wrapper class hyphen.hyphenator. So 'hnjmodule' is disregarded by
      'from hyphen import *'. Note that hyphenation dictionaries are invisible to the
      Python programmer. But each hyphenator object has a member 'language' which is a
      string showing the language of the dictionary in use.



1.2 The module 'textwrap2'

This module is an enhanced though backwards compatible version of the module
'textwrap' known from the Python standard library. Not very surprisingly, it adds
hyphenation functionality to 'textwrap'.

2. Code examples (see README.txt)

'''


from . import hnj, config
import pickle, os


__all__ = ['dictools', 'Hyphenator']

# Try to load meta information on downloadable dictionaries:
if os.path.exists(config.default_dict_path + '/dict_info.pickle'):
    dict_info = pickle.load(open(config.default_dict_path + '/dict_info.pickle', 'rb'))
else: dict_info = None




class Hyphenator:
    '''
    Wrapper class around the class 'hnjmodule.hyphenator_'. It provides convenient access to the C library
    'libhyphen'.
    '''
    def __init__(self, language = 'en_US', lmin = 2, rmin = 2, compound_lmin = 2, compound_rmin = 2,
            directory = config.default_dict_path):
        '''
        Return a hyphenator object initialized with a dictionary for the specified language.

            'language' should by convention be a string of length 5 of the form "ll_CC" where ll
            is the language code          and CC the country code.
            This is inspired by the file names of
            OpenOffice's hyphenation dictionaries.
            Example: 'en_NZ' for English / New Zealand

        Each class instance has an attribute 'info' of type dict containing metadata on its dictionary.
        If the module-level attribute dict_info is None
        or does not contain an entry for this dictionary, the info attribute of the Hyphenator instance will be None.
        There is also a 'language' attribute of type str which is deprecated since v1.0.
        
        lmin, rmin, compound_lmin and compound_rmin: set minimum number of chars to be cut off by hyphenation in
        single or compound words
        
        '''
        
        
        if dict_info and language in dict_info:
            file_name = dict_info[language]['name'] + '.dic'
        else: file_name = language
        file_path = ''.join((directory, '/hyph_', language, '.dic'))
        self.__hyphenate__ = hnj.hyphenator_(file_path, lmin, rmin, compound_lmin, compound_rmin)
        self.language = language
        if dict_info:
            self.info = dict_info[language]
        else: self.info = None




    def pairs(self, word):
        '''
        Hyphenate 'word' and return a list of lists of the form [['hy', 'phenation'], ['hyphen', 'ation']].

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding
        * * the hyphenator could not find a hyphenation point        .'''
        mode = 1
        if (len(word) < 4) or ('=' in word): return []
        if not word.islower():
            if (word.isupper()):
                mode += 4
                word = word.lower()
            else:
                if (word[1:].islower()):
                    mode += 2
                    word = word.lower()
                else: return []
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.''
        try:
            return self.__hyphenate__.apply(word, mode)
        except UnicodeError:
            return []



    def syllables(self, word):
        '''
        Hyphenate 'word' and return a list of syllables.

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding
        * the hyphenator could not find a hyphenation point        .

        Results are inconsistent in case of non-standard hyphenation as
        a join of syllables would not yield the original word.
        '''

        mode = 0
        if (len(word) < 4) or ('=' in word): return []
        if not word.islower():
            if (word.isupper()):
                mode += 4
                word = word.lower()
            else:
                if (word[1:].islower()):
                    mode += 2
                    word = word.lower()
                else: return []
        # Now call the hyphenator catching the case that 'word' is not encodable
        # to the dictionary's encoding.''
        try:
            return self.__hyphenate__.apply(word, mode).split('=')
        except UnicodeError:
            return []



    def wrap(self, word, width, hyphen = '-'):
        '''
        Hyphenate 'word' and determine the best hyphenation fitting
        into 'width' characters.
        Return a list of the form ['hypen-', 'ation']
        The '-' in the above example is the default value of 'hyphen'.
        It is added automatically and must fit
        into 'width' as well. If no hyphenation was found such that the
        shortest prefix (plus 'hyphen') fits into 'width', [] is returned.
        If the left part ends with a hyphen such as in 'Python-powered', no hyphen is appended.
        '''
        
        p = self.pairs(word)
        max_chars = width - len(hyphen)
        while p:
            if p[-1][0].endswith(hyphen): cur_max_chars = max_chars + 1
            else: cur_max_chars = max_chars
            if len(p[-1][0]) > cur_max_chars:
                p.pop()
            else: break
        if p:
            # Need to append a hyphen?
            if cur_max_chars == max_chars:
                p[-1][0] += hyphen
            return p[-1]
        else: return []



# The following ensures backwards compatibility with version 0.9.3
class hyphenator(Hyphenator):
    '''This class is deprecated. Use 'Hyphenator' instead.'''
