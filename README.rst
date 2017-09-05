=================================
PyHyphen - hyphenation for Python
=================================

(c) 2008-2017 Dr. Leo

Contact: fhaxbox66@googlemail.com

Project home: https://bitbucket.org/fhaxbox66/pyhyphen

Mailing list: http://groups.google.com/group/pyhyphen


.. contents::

0. Quickstart
=============

::

    $ pip install pyhyphen
    $ echo "long sentences and complicated words are flabbergasting" | wraptext -w 10 -
    long sen-
    tences and
    compli-
    cated
    words are 
    flabber-
    gasting


1. Overview
================

PyHyphen is a pythonic interface to the hyphenation C library used in software such as LibreOffice and the Mozilla suite.
It comes with tools to download, install and uninstall hyphenation dictionaries from LibreOffice's Git repository.
PyHyphen consists of the 'hyphen' and 'textwrap2' packages.
The source distribution also contains ``wraptext.py``, a script which wraps 
a text-file with hyphenation given a specified width. See the code example under "Quick start" above. 
 
The source distribution supports Python 2.7 and 3.4 or higher, perhaps Python 3.3 works as well. 
If you depend on earlier 2.x versions, use PyHyphen-1.0b1
instead. In this case you may have to download hyphenation dictionaries manually.

1.1 Content of the hyphen package
------------------------------------------

The 'hyphen' package contains the following:

- the class hyphen.Hyphenator: each instance of it can hyphenate and wrap
  words using a dictionary compatible with the hyphenation feature of
  LibreOffice and Mozilla. Required dictionaries are automatically
  downloaded at runtime.
- the module dictools contains useful functions such as for downloading and
  installing dictionaries from a configurable repository. After
  installation of PyHyphen, the LibreOffice repository is used by default.
- 'hyphen.hnj' is the C extension module that does all the ground work. It
  contains the high quality
  `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_.
  It supports hyphenation with replacements as well as compound words.


1.2 The module 'textwrap2'
------------------------------

This module is an enhanced, though backwards-compatible version of the module
'textwrap' from the Python standard library. Unsurprisingly, it adds
hyphenation functionality to 'textwrap'. To this end, a new key word parameter
'use_hyphenator' has been added to the __init__ method of the TextWrapper class which
defaults to None. It can be initialized with any hyphenator object. Note that until version 0.7
this keyword parameter was named 'use_hyphens'. So older code may need to be changed.'


2. Code examples
======================


::

        >>> from hyphen import Hyphenator
        # Create some hyphenators
        h_de = Hyphenator('de_DE')
        h_en = Hyphenator('en_US')

        # Now hyphenate some words
        # Note: the following examples are written in Python 3.x syntax.
        # If you use Python 2.x, you must add the 'u' prefixes as Hyphenator methods expect unicode strings.

        h_en.pairs('beautiful'
        [['beau', 'tiful'], [u'beauti', 'ful']]

        h_en.wrap('beautiful', 6)
        ['beau-', 'tiful']

        h_en.wrap('beautiful', 7)
        ['beauti-', 'ful']
        
        h_en.syllables('beautiful')
        ['beau', 'ti', 'ful']
        
        >>> from textwrap2 import fill
        print fill('very long text...', width=40, use_hyphenator=h_en)

Just by creating ``Hyphenator`` objects for a language, the corresponding
dictionaries will be automatically downloaded. Dictionaries may be manually
installed and listed with the ``dictools`` module::

        >>> from hyphen.dictools import *

        # Download and install some dictionaries in the default directory using the default
        # repository, usually the LibreOffice website
        >>> for lang in ['de_DE', 'en_US']:
            install(lang)
            
        # Show locales of installed dictionaries
        >>> list_installed()
        ['de', 'de_DE', 'en_PH', 'en_US']


3. Installation
===============

PyHyphen is pip-installable. In most scenarios the easiest way to install PyHyphen is to type from the shell prompt::

    $ pip install pyhyphen

Besides the source distribution, there are wheels on PyPI for common Windows-based environments. So most Windows users
can install PyHyphen without a C compiler. 

Building PyHyphen from source under Linux may require root privileges.

4. Managing dictionaries
========================

The ``dictools`` module contains a non-exhaustive list of available language strings that can be used to instautiate ``Hyphenator`` objects as shown above::

    >>>from hyphen import dictools
    >>>dictools.LANGUAGES
    ['af_ZA', 'an_ES', 'ar', 'be_BY', 'bg_BG', 'bn_BD', 'br_FR', 'ca', 'cs_C
    Z', 'da_DK', 'de', 'el_GR', 'en', 'es_ES', 'et_EE', 'fr_FR', 'gd_GB', 'gl', 'gu_
    IN', 'he_IL', 'hi_IN', 'hr_HR', 'hu_HU', 'it_IT', 'ku_TR', 'lt_LT', 'lv_LV', 'ne
    _NP', 'nl_NL', 'no', 'oc_FR', 'pl_PL', 'prj', 'pt_BR', 'pt_PT', 'ro', 'ru_RU', '
    si_LK', 'sk_SK', 'sl_SI', 'sr', 'sv_SE', 'sw_TZ', 'te_IN', 'th_TH', 'uk_UA', 'zu
    _ZA']
    
The downloaded dictionary files are stored in a local data folder, along with a
``dictionaries.json`` file that lists the downloaded files and the associated
locales::


    $ ls ~/.local/share/pyhyphen
    dictionaries.json  hyph_de_DE.dic  hyph_en_US.dic

    $ cat ~/.local/share/pyhyphen/dictionaries.json
    {
      "de": {
        "file": "hyph_de_DE.dic", 
        "url": "http://cgit.freedesktop.org/libreoffice/dictionaries/plain/de/hyph_de_DE.dic"
      }, 
      "de_DE": {
        "file": "hyph_de_DE.dic", 
        "url": "http://cgit.freedesktop.org/libreoffice/dictionaries/plain/de/hyph_de_DE.dic"
      }, 
      "en_PH": {
        "file": "hyph_en_US.dic", 
        "url": "http://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/hyph_en_US.dic"
      }, 
      "en_US": {
        "file": "hyph_en_US.dic", 
        "url": "http://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/hyph_en_US.dic"
      }
    }

Each entry of the ``dictionaries.json`` file contains both the path to the
dictionary file and the url from which it was downloaded.

5. Development
===============

Feel free to submit issues or PRs on bitbucket or join the mailing-list (see above).
When making changes, run the unit tests with pytest.



6. Contributing and reporting bugs
=====================================

PRs and bug reports can be submitted on bitbucket, questions are welcome in the Google group 
(http://groups.google.com/group/pyhyphen). Or just send
an e-mail to the authors.

Browse  or fork the Mercurial repository and report 
bugs at `bitbucket <https://bitbucket.org/fhaxbox66/pyhyphen/issues?status=new&status=open>`_.

7. License
============

Without prejudice to third party licenses, PyHyphen is distributed under the Apache 2.0 license. PyHyphen ships with third party code including the hyphenation library
hyphen.c and a patched version of the Python standard module textwrap.    
   

8. Changelog
======================

New in Version 3.0.0:

* lazy dictionary install at runtime
* switch to user-specific data directory for storing dictionaries
* unit tests
* migration from distutils to setuptools and simplified setup
* get rid of config module and config scripts
* upgrade textwrap2 to latest python2 and python3 versions; 
  add CLI script to wrap text files with hyphenation
* improve detection of dictionary location
* Remove Windows binaries from the source distribution. Provide wheels instead 
  thanks to the awesome `cibuildwheel tool <https://github.com/joerick/cibuildwheel>`_.

New in Version 2.0.9:

* add support for Python 3.6


New in Version 2.0.8:

* fix python 3 install
* fix install from source


New in Version 2.0.7:

* add win binary for AMD64, win27
* make it pip-installable (PR1)
* minor fixes
 

New in Version 2.0.5:

* remove pre-compiled win32 C extension for Python 2.6, add one for Python 3.4
* avoid unicode error in config.py while installing on some Windows systems


New in Version 2.0.4:

* Update C library to v2.8.6

 
New in Version 2.0.2:

* minor bugfixes and refactorings


New in Version 2.0.1:

* updated URL for LibreOffice's dictionaries
* no longer attempt to hyphenate uppercased words such as 'LONDON'. This
  feature had to be dropped to work around a likely bug in the C extension which,
  under Python 3.3, caused
  the hyphenator to return words starting with a capital letter as lowercase.




New in Version 2.0

The hyphen.dictools module has been completely rewritten. This was required
by the switch from OpenOffice to LibreOffice which does no longer support the
old formats for dictionaries and meta data. these changes made it impossible to release a stable v1.0.
The new dictionary management is more
flexible and powerful. There is now a registry for locally installed hyphenation dictionaries. Each dictionary
can have its own file path. It is thus possible to add persistent metadata on pre-existing hyphenation
dictionaries, e.g. from a LibreOffice installation.
Each dictionary and hence Hyphenator can now be
associated with multiple locales such as for 'en_US' and 'en_NZ'. These changes cause some backwards-incompatible API changes.
Further changes are:

* Hyphenator.info is of a container type for 'url', 'locales' and 'filepath' of the dictionary.
* the Hyphenator.language attribute deprecated in v1.0 has been removed
* download and install dictionaries from LibreOffice's git repository by default
* dictools.install('xx_YY') will install all dictionaries found for the 'xx' language and associate them with all relevant locales
  as described in the dictionaries.xcu file in LibreOffice's git repository.
* upgraded the `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_
  to v2.8.3
* use lib2to3 instead of separate code bases
* dropped support for Python 2.4 and 2.5
* support Python 3.3


New in version 1.0

* Upgraded the `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_
  to v2.7 which brings significant improvements, most notably correct treatment of
  already hyphenated words such as 'Python-powered'
* use a CSV file from the oo website with meta information
  on dictionaries for installation of dictionaries and
  instantiation of hyphenators. Apps can access the metadata
  on all downloadable dicts through the new module-level attribute hyphen.dict_info or for each hyphenator
  through the 'info' attribute,
* Hyphenator objects have a 'info' attribute which is
  a Python dictionary with meta information on
  the hyphenation dictionary. The 'language' attribute
  is deprecated. *Note:* These new features add
  complexity to the installation process as the metadata and dictionary files
  are downloaded at install time. These features have to be tested
  in various environments before declaring the package stable.
* Streamlined the installation process
* The en_US hyphenation dictionary
  has been removed from the package. Instead, the dictionaries for en_US and the local language are automatically
  downloaded at install time.
* restructured the package and merged 2.x and 3.x setup files
* switch from svn to hg
* added win32 binary of the C extension module for Python32, currently no binaries for Python 2.4 and 2.5


New in version 0.10

* added win32 binary for Python 2.7
* renamed 'hyphenator' class to to more conventional 'Hyphenator'. 'hyphenator' is deprecated.


