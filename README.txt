=================================
PyHyphen - hyphenation for Python
=================================

(c) 2008-2013 Dr. Leo

Contact: fhaxbox66@googlemail.com

Project home: http://pyhyphen.googlecode.com

Mailing list: http://groups.google.com/group/pyhyphen


.. contents::

Change log
======================

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


1. Overview
================

PyHyphen is a pythonic interface to the hyphenation C library used in software such as LibreOffice and the Mozilla suite.
It comes with tools to download, install and uninstall hyphenation dictionaries from LibreOffice's Git repository.
PyHyphen consists of the package 'hyphen' and the module 'textwrap2'. 
The source distribution supports Python 2.6 or higher, including Python 3.3. If you depend on python 2.4 or 2.5, use PyHyphen-1.0b1
instead. In this case you may have to download hyphenation dictionaries manually.

1.1 Content of the hyphen package
------------------------------------------

The 'hyphen' package contains the following:

    - the class hyphen.Hyphenator: each instance of it
      can hyphenate and wrap words using a dictionary compatible with the hyphenation feature of
      LibreOffice and Mozilla.
    - the module dictools contains useful functions such as for downloading and
      installing dictionaries from a configurable repository. After installation of PyHyphen, the
      LibreOffice repository is used by default.
    - hyphen.dict_info: a dict object with metadata on all hyphenation dictionaries installed locally. In previous
      versions, dict_info contained meta data on all downloadable dictionaries. This feature
      is no longer supported as LibreOffice's GIT repository
      does not provide such a list anymore. Instead, Use
      hyphen.config.languages which is an incomplete set of
      language codes of hyphenation dictionaries available from LibreOffice's GIT repository. These codes
      can be passed to hyphen.dictools.install() to download and install
      the respective dictionary and update the local registry.
    - hyphen.config is a configuration file initialized at install time with default values
      for paths of dictionaries and the registry file, as well as the default URL of
      the repository for
      downloadable dictionaries. Initial values for the local paths are set to
      the package root, the URL is set to the LibreOffice
      repository for dictionaries.
    - hyphen.DictInfo: dict-like container type for meta data on dictionaries. It has the following attributes:
      'locales': a list of locales for which the dictionary is suitable;
      'url': the URL from which the dictionary was downloaded, or None; 'filepath': the
      local path including the file name of the dictionary.
    - hyphen.hnj' is the C extension module that does all the ground work. It
      contains the high quality
      `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_.
      It supports hyphenation with replacements as well as compound words.
      Note that hyphenation dictionaries are invisible to the
      Python programmer. But each hyphenator object has an attribute 'info' which is a
      DictInfo object containing meta data on the hyphenation dictionary of this Hyphenator instance.
      The 'language' attribute containing a locale for which the dictionary is suitable,
      is deprecated as from v1.0. Use my_hyphenator.info.locales instead to access
      a list of locales for which the dictionary is suitable.


1.2 The module 'textwrap2'
------------------------------

This module is an enhanced though backwards compatible version of the module
'textwrap' from the Python standard library. Unsurprisingly, it adds
hyphenation functionality to 'textwrap'. To this end, a new key word parameter
'use_hyphenator' has been added to the __init__ method of the TextWrapper class which
defaults to None. It can be initialized with any hyphenator object. Note that until version 0.7
this keyword parameter was named 'use_hyphens'. So older code may need to be changed.'


2. Code examples
======================


::

        >>>from hyphen import Hyphenator, dict_info
        from hyphen.dictools import *

        # Download and install some dictionaries in the default directory using the default
        # repository, usually the LibreOffice website
        >>>for lang in ['de_DE', 'en_US']:
            if not is_installed(lang): install(lang)
            
        # Show locales of installed dictionaries
        >>>dict_info.keys()
        ['de_CH', 'en_CA', 'en_PH', 'de', 'de_DE', 'en_TT', 'en_NA', 'en_MW',
        'en_ZA', 'en_AU', 'en_NZ', 'en_JM', 'en_BS', 'en_US', 'de_AT',
        'en_IE', 'en_ZW', 'en_GH', 'en_IN', 'en_BZ', 'en_GB']

        >>>print(dict_info['en_GB'])
        Hyphenation dictionary:
        Locales: ['en_GB', 'en_ZA', 'en_NA', 'en_ZW', 'en_AU', 'en_CA', 'en_IE', 'en_IN'
        , 'en_BZ', 'en_BS', 'en_GH', 'en_JM', 'en_MW', 'en_NZ', 'en_TT']
        filepath: c:\python27\lib\site-packages\hyphen/hyph_en_GB.dic
        URL: http://cgit.freedesktop.org/libreoffice/dictionaries/plain/dictionaries/en/
        hyph_en_GB.dic


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
        
        h_en.info
        {'file_name': 'hyph_en_US.zip', 'country_code': 'US', 'name': 'hyph_en_US',
        'long_descr': 'English (United States)', 'language_code': 'en'}
        

        from textwrap2 import fill
        print fill('very long text...', width = 40, use_hyphenator = h_en)



3. Installation
================================

PyHyphen works with Python 2.6 or higher, including Python 3.x.
The package includes pre-compiled binaries of the hnj module for win32 and Python 2.6, 2.7, 3.2 and 3.3.
On other platforms you will need a build environment such as gcc, make

PyHyphen is pip-installable. In most scenarios the easiest way to install PyHyphen is to type from the shell prompt: 

$ pip install pyhyphen

Manual download and installation will be your preferred option if you want to compile the C library
from source on Windows rather than using the pre-compiled binary, or if you do not want to download dictionaries upon install.

The setup script first checks the Python version, creates a 'hyphen' subdir, and copies
the required files from the 2.x and src subdirs. If needed, lib2to3 will
be used.

Second, setup.py searches in ./bin for a pre-compiled binary
of hnj for your platform. If there is a binary that looks ok, this version is installed. Otherwise,
hnj is compiled from source. On Windows you will need MSVC, mingw
or whatever fits to your Python distribution.
If the distribution comes with a binary of 'hnj'
that fits to your platform and python version, you can still force a compilation from
source by entering

    $python setup.py install --force_build_ext

Under Linux you may need root privileges.

 After compiling and installing the hyphen package, config.py is adjusted as follows:
 
- the local default path for hyphenation dictionaries is set to  the package directory
- the base URL from which
  dictionaries are downloaded is set to LibreOffice's GIT repository

Thereafter the setup script imports the hyphen package to install a default
set of dictionaries, unless the command line contains 'no_dictionaries' after the 'install' command.
The dictionaries installed by default are those for English and the locale, if different.


4. Contributing and reporting bugs
=====================================

Contributions, comments, bug reports, criticism and praise can be sent to the author.

Browse  the Mercurial repository and submit
bug reports at http://pyhyphen.googlecode.com.


