# -*- coding: utf-8 -*-

# Without prejudice to the license governing the use of
# the Python standard module textwrap on which textwrap2 is based,
# PyHyphen is licensed under the same terms as the underlying C library hyphen-2.3.1.
# The essential parts of the license terms of hyphen-2.3.1 are quoted hereunder.
#
#
#
#
# Extract from the license information of hyphen-2.4 library
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
3. Compiling and installing (left out here; see the README file for details)
4. Obtaining dictionaries



1. Overview

PyHyphen consists of the package 'hyphen' and the module 'textwrap2'.

1.1 The hyphen package contains:
    - at top level the definition of the class 'Hyphenator' each instance of which
      can hyphenate words using a dictionary compatible with the hyphenation feature of
      OpenOffice and Mozilla. The former class 'hyphenator' is deprecated
      as of version 0.10 as class names conventially begin with a capital letter.
    - the module dictools contains useful functions such as automatic downloading and
      installing dictionaries from a configurable repository. By default, the
      OpenOffice repository is used.
     - config is a configuration file initialized at install time with default values
       for the directory where dictionaries are searched, and the repository for future
       downloads of dictionaries.
     - hyph_en_US.dic is the hyphenation dictionary for US English as found on
       the OpenOffice.org repository.
    - 'hnj' is the C extension module that does all the ground work. It
      contains the C library hyphen-2.4 used in OpenOffice and Mozilla products.
      It supports non-standard hyphenation and - as of version 2.4 - compound words.
      Moreover, the minimum number of characters cut off by the hyphen can be set
      both for the entire word and compound parts thereof.
         Note that hyphenation dictionaries are invisible to the
      Python programmer. But each hyphenator object has a member 'language' which is a
      string showing the language of the dictionary in use.


1.2 The module 'textwrap2'

This module is an enhanced though backwards compatible version of the module
'textwrap' known from the Python standard library. Not very surprisingly, it adds
hyphenation functionality to 'textwrap'.

2. Code examples

from hyphen import Hyphenator
from hyphen.dictools import *

# Download and install some dictionaries in the default directory using the default
# repository, usually the OpenOffice website
for lang in ['de_DE', 'fr_FR', 'en_UK', 'ru_RU']:
    if not is_installed(lang): install(lang)

# Create some hyphenators
h_de = Hyphenator('de_DE', rmin = 3; compound_rmin = 3) # the left values are 2 by default.
h_en = Hyphenator() # 'en_US' is the difault dictionary.'

# Now hyphenate some words

print h_en.pairs(u'beautiful')
[[u'beau', u'tiful'], [u'beauti', u'ful']]

print h_en.wrap(u'beautiful', 6)
[u'beau-', u'tiful']

print h_en.wrap(u'beautiful', 7)
[u'beauti-', u'ful']


4. Obtaining dictionaries

 Visit http://wiki.services.openoffice.org/wiki/Dictionaries for a
 complete list. If you know the language and country code of your favorite
 dictionary (e.g. 'it_IT' for Italian) and have internet access, you can take
 advantage of the install function in the hyphen.dictools module. See the code
 example above (2.) for more details, or read the module documentation.

'''


import hnj, config

__all__ = ['dictools', 'hyphenator']




class Hyphenator:
    """
    Wrapper class around the class 'hnj.hyphenator_'.
    It provides convenient access to the C library hyphen-2.4'.
    """
    def __init__(self, language = 'en_US', lmin = 2, rmin = 2, compound_lmin = 2,
    compound_rmin = 2,
        directory = config.default_dic_path):
        """
        Return a hyphenator object initialized with a dictionary for the
        specified language.

            'language' should by convention be a string of length 5 of the form
            "ll_CC" where ll is the language code          and CC the country code.
            This is inspired by the file names of
            OpenOffice's hyphenation dictionaries.
            Example: 'en_NZ' for English / New Zealand

        Each class instance has a member 'language' showing the language
        of its dictionary.
            lmin, compound_lmin and friends set the minimum number of characters
            cut off at the beginning or end of the entire word
               or compound parts thereof.
        """
        file_path = ''.join((directory, '/hyph_', language, '.dic'))
        self.__hyphenate__ = hnj.hyphenator_(file_path, lmin, rmin,
            compound_lmin, compound_rmin)
        self.language = language


    def pairs(self, word):
        '''
        Hyphenate a unicode string and return a list of lists of the form
        [[u'hy', u'phenation'], [u'hyphen', u'ation']].

        Return [], if len(word) < 4 or if word could not be hyphenated because
        
        * it is not encodable to the dictionary's encoding, or
        ** the hyphenator could not find any hyphenation point
        '''
        if not isinstance(word, unicode): raise TypeError('Unicode object expected.')
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
        # to the dictionary's encoding.'
        try:
            return self.__hyphenate__.apply(word, mode)
        except UnicodeError:
            return []


    def syllables(self, word):
        '''
        Hyphenate a unicode string and return list of syllables.

        Return [], if len(word) < 4 or if word could not be hyphenated because

        * it is not encodable to the dictionary's encoding, or
        ** the hyphenator could not find any hyphenation point

        Results are not consistent in case of non-standard hyphenation as a join of the syllables
        would not yield the original word.
        '''
        if not isinstance(word, unicode): raise TypeError('Unicode object expected.')
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
        # to the dictionary's encoding.'
        try:
            return self.__hyphenate__.apply(word, mode).split('=')
        except UnicodeError:
            return []


    def wrap(self, word, width, hyphen = '-'):
        '''
        Hyphenate 'word' and determine the best hyphenation fitting
        into 'width' characters.
        Return a list of the form [u'hypen-', u'ation']
        The '-' in the above example is the default value of 'hyphen'.
        It is added automatically and must fit
        into 'width' as well. If no hyphenation was found such that the
        shortest prefix (plus 'hyphen') fits into 'width', [] is returned.
        '''
        p = self.pairs(word)
        max_chars = width - len(hyphen)
        while p and (len(p[-1][0]) > max_chars): p.pop()
        if p:
            p[-1][0] = ''.join((p[-1][0], hyphen))
            return p[-1]
        else: return []


# The following ensures backwards compatibility with version 0.9.3
class hyphenator(Hyphenator):
    '''This class is deprecated. Use 'Hyphenator' instead.'''
