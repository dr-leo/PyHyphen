=================================
PyHyphen - hyphenation for Python
=================================

(c) 2008-2017 Dr. Leo

Contact: fhaxbox66@googlemail.com

Project home: https://bitbucket.org/fhaxbox66/pyhyphen

Mailing list: http://groups.google.com/group/pyhyphen


.. contents::

1. Overview
================

PyHyphen is a pythonic interface to the hyphenation C library used in software such as LibreOffice and the Mozilla suite.
It comes with tools to download, install and uninstall hyphenation dictionaries from LibreOffice's Git repository.
PyHyphen consists of the 'hyphen' and 'textwrap2' packages. 
The source distribution supports Python 2.6 or higher, including Python 3.6. If you depend on python 2.4 or 2.5, use PyHyphen-1.0b1
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

        >>> from hyphen.dictools import *

        # Download and install some dictionaries in the default directory using the default
        # repository, usually the LibreOffice website
        >>> for lang in ['de_DE', 'en_US']:
            install_if_necessary(lang)
            
        # Show locales of installed dictionaries
        >>> list_installed()
        ['de', 'de_DE', 'en_PH', 'en_US']

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



3. Installation
================================

PyHyphen is tested with Python 2.7 and Python 3.3 and 3.4, but  should
word on older versions as well.
The package includes pre-compiled binaries of the hnj module for win32 and Python 2.6, 2.7, 3.2 and 3.3.
On other platforms you will need a build environment such as gcc, make

PyHyphen is pip-installable. In most scenarios the easiest way to install PyHyphen is to type from the shell prompt: 

    $ pip install pyhyphen

Manual download and installation will be your preferred option if you want to compile the C library
from source on Windows rather than using the pre-compiled binary, or if you do not want to download dictionaries upon install.

Setup will search in ./bin for a pre-compiled binary of hnj for your
platform. If there is a binary that looks ok, this version is installed.
Otherwise, hnj is compiled from source. On Windows you will need MSVC, mingw or
whatever fits to your Python distribution. If the distribution comes with a
binary of 'hnj' that fits to your platform and python version, you can still
force a compilation from source by entering

    $ python setup.py install --force_build_ext

Under Linux you may need root privileges.

4. Development
===============

When making changes to PyHyphen, be sure to write and run the unit tests:

    ./runtests.py

Don't forget to run tests both with Python 3 and Python 2!

5. Contributing and reporting bugs
=====================================

Contributions, comments, bug reports, criticism and praise can be sent to the author.

Browse  or fork the Mercurial repository and report 
bugs at `bitbucket <https://bitbucket.org/fhaxbox66/pyhyphen/issues?status=new&status=open>`_.


Change log
======================

New in Version 3.0.0:

* lazy dictionary install at runtime
* switch to user-specific data directory for storing dictionaries
* unit tests
* migration from distutils to setuptools and simplified setup
* get rid of config module and config scripts
* upgrade textwrap2 to latest python2 and python3 versions
* improve detection of dictionary location


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


