=========
Changelog
=========



Version 4.0.4 (2024-07-30)
==========================

* update default dict location
* update list of language strings
* update some requirements
 
Version 4.0.3 (2021-12-17)
==========================

* textwrap2: fix hyphenation of long words - Thanks to fruchti!



Version 4.0.2 (2021-11-19)
==========================

* Update requirements, enhance MakeFile

Version 4.0.1 (2021-03-16)
==========================

* Fix MacOS builds

Version 4.0.0 (2021-02-15)
==========================

This is a  big release.
The entire code-base has been overhauled.
A cross-Py-version wheel for Windows and the use of
the excellent `requests` package for HTTP connections
are but some of the highlights.

* `hyphen.Hyphenator`:

  - support of hyphenation of upper-cased words as in version 2.x
  - better error-handling
  - human-friendly str representation of Hyphenator objects

* Builds:

  - single-source package version (requires setuptools >= 47.0)
  - CI: move to Github actions. Build ABI3-compatible wheel for Windows

* C extension:

  - partial rewrite to support the limited API (PEP 384)
  - multi-phase initialization of the module
  - upgrade hyphen.c from hunspell
  - clean-ups

* hyphen.dictools:

  - use `requests` instead of urllib for HTTP connections
  - make HTTP connections configurable through kwargs passed to `requests.get`
  - improve error-handling
  - fix URL generation in some cases
  - clean-ups

* make textwrap2 a submodule of hyphen
* remove wraptext script

Version 3.0.1
=============

Fix source distribution which did not include C header files.

Version 3.0.0
=============

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

Version 2.0.9
=============

* add support for Python 3.6


Version 2.0.8
=============

* fix python 3 install
* fix install from source


Version 2.0.7
=============

* add win binary for AMD64, win27
* make it pip-installable (PR1)
* minor fixes


Version 2.0.5
=============

* remove pre-compiled win32 C extension for Python 2.6, add one for Python 3.4
* avoid unicode error in config.py while installing on some Windows systems


Version 2.0.4
=============

* Update C library to v2.8.6


Version 2.0.2
=============

* minor bugfixes and refactorings


Version 2.0.1
=============

* updated URL for LibreOffice's dictionaries
* no longer attempt to hyphenate uppercased words such as 'LONDON'. This
  feature had to be dropped to work around a likely bug in the C extension which,
  under Python 3.3, caused
  the hyphenator to return words starting with a capital letter as lowercase.


Version 2.0
===========

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


Version 1.0
===========

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


Version 0.10
============

* added win32 binary for Python 2.7
* renamed 'hyphenator' class to to more conventional 'Hyphenator'. 'hyphenator' is deprecated.
