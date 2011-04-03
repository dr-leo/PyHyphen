=================================
PyHyphen - hyphenation for Python
=================================

(c) 2008-2011 Dr. Leo

Contact: fhaxbox66@googlemail.com

Project home: http://pyhyphen.googlecode.com

Mailing list: http://groups.google.com/group/pyhyphen


.. contents::

Change log
======================

New in version 1.0

* Upgraded the C library libhyphen to v2.7 which brings significant improvements, most notably correct treatment of
*  already hyphenated words such as 'Python-powered'
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

New in version 0.9.3:

* added win32 binary of the C extension for Python 3.1
* added 'syllables' method to the hyphenator (can yield inconsistent results
  in languages with non-standard hyphenation)


New in version 0.9.2

* make it compile with Python 3.0.1
* add win32 binary of the C extension for Python 3.0

New in version 0.9.1

* full support for Python 3.0
* merged 3.0 sources with the 2.x distribution.




New in Version 0.9:

* removed the 'inserted' method from the hyphenator class as it is not used in practice
  the word to be hyphenated must now be unicode (utf-8 encoded strings raise
  TypeError). The restriction to unicode is safer and more 3.0-compliant.
* fixed important bug in 'pairs' method that could cause a unicode error if 'word'
  was not encodable to the dictionary's encoding. In the latter case, the new
  version returns an empty list (consistent with other cases where the word
  is not hyphenable).
* the configuration script has been simplified and improved: it does not
  raise ImportError even if the package cannot be imported. This tolerance is
  needed to create a Debian package.



New in Version 0.8

- supports Python 2.x and 3.0 (in 2 separate distributions))
- contains the new C library hyphen-2.4 which implements an extended algorithm
  supporting:
  
  - compound words (dictionaries are under development in the OpenOffice community))
  - parameters to fix the minimal number of characters to be cut off
      by hyphenation (lmin, rmin, compound_lmin and compound_rmin). )
      This may require code changes in existing apps.
      
- new en_US dictionary.
- many minor improvements under the hood
        

1. Overview
================

The gole of the PyHyphen project is to provide Python with a high quality hyphenation facility.
PyHyphen consists of the package 'hyphen' and the module 'textwrap2'. 
The source distribution supports Python 2.4 or higher, including Python 3.2.

1.1 Content of the hyphen package
------------------------------------------

The 'hyphen' module defines the following:

    - at top level the definition of the class 'Hyphenator' each instance of which
      can hyphenate and wrap words using a dictionary compatible with the hyphenation feature of
      OpenOffice and Mozilla.
    - the module dictools contains useful functions such as downloading and
      installing dictionaries from a configurable repository. After installation of PyHyphen, the
      OpenOffice repository is used by default. 'dictools.install_dict-info'
      downloads metadata on all available hyphenation dictionaries from the OpenOffice website and
      stores it in a pickled file.
    - hyphen.dict_info: a dict object with metadata on all hyphenation dictionaries downloadable from the
      OpenOffice website.
    - config is a configuration file initialized at install time with default values
      for the directory where dictionaries are searched, and the repository for
      downloads of dictionaries. Initial values are the package root and the OpenOffice
      repository for dictionaries.
    - hnj' is the C extension module that does all the ground work. It
      contains the C library libhyphen. It supports non-standard hyphenation
      with replacements as well as compound word hyphenation.
      Note that hyphenation dictionaries are invisible to the
      Python programmer. But each hyphenator object has an attribute 'info' which is a
      dict object containing metadata on the hyphenation dictionary of this Hyphenator instance.
      The former 'language' attribute, a string of the form 'll_CC'
      is deprecated as from v1.0.


1.2 The module 'textwrap2'
------------------------------

This module is an enhanced though backwards compatible version of the module
'textwrap' from the Python standard library. Not very surprisingly, it adds
hyphenation functionality to 'textwrap'. To this end, a new key word parameter
'use_hyphenator' has been added to the __init__ method of the TextWrapper class which
defaults to None. It can be initialized with any hyphenator object. Note that until version 0.7
this keyword parameter was named 'use_hyphens'. So older code may need to be changed.'

1.3 hyphen_test
-------------------------------

(no longer part of the distribution as of version 0.9.1; please
    clone the hg repository to get it)

This Python script is a framework for running large tests of the hyphen package.
A test is a list of 3 elements: a text file (typically a word list), its encoding and a
list of strings specifying a dictionary to be applied to the word list. Adding a test
is as easy as writing a function call. All results are logged.


2. Code example
======================


::

        >>>from hyphen import Hyphenator
        from hyphen.dictools import *

        # Download and install some dictionaries in the default directory using the default
        # repository, usually the OpenOffice website
        for lang in ['de_DE', 'fr_FR', 'en_UK', 'ru_RU']:
            if not is_installed(lang): install(lang)

        # Create some hyphenators
        h_de = Hyphenator('de_DE')
        h_en = Hyphenator('en_US')

        # Now hyphenate some words
        # Note: the following examples are written in Python 3.x syntax.
        # If you use Python 2.x, you must add the 'u' prefixes as Hyphenator methods expect unicode objects.

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
        print fill('very long text...', width = 40, use_hyphens = h_en)



3. Compiling and installing
================================

3.1 General requirements
---------------------------

PyHyphen works with Python 2.4 or higher, including 3.2.
There are pre-compiled binaries of the hnj module for win32 and Python 2.6 to 3.2.
On other platforms you will need a build environment such as gcc, make


3.2 Compiling and installing from source
----------------------------------------------

Choose and download the source distribution from

    http://cheeseshop.python.org/pypi/PyHyphen

and unpack it in a temporary directory. Then cd to this directory.

You can compile and install the hyphen package
as well as the module textwrap2 by entering at the command line somethin like:

$python setup.py install

The setup script will first check the Python version and copy the required
version-specific files. 

Second, setup.py searches in ./bin for a pre-compiled binary
of hnj for your platform. If there is a binary that looks ok, this version is installed. Otherwise,
hnj is compiled from source. On Windows you will need MSVC 2003 (Python 2.4 and 2.5) or MSVC 2008 (for Python2.6 or higher), mingw
or whatever fits to your Python distribution.
If the distribution comes with a binary of 'hnj'
that fits to your platform and python version, you can still force a compilation from
source by entering

    $python setup.py install --force_build_ext

Under Linux you may need root privileges, so you may want to enter something like

    $sudo python setup.py install

 After compiling and installing the hyphen package, config.py is adjusted as follows:
 
- the package directory becomes the local default path for hyphenation dictionaries
 - the OpenOffice website becomes the default repository from which
   dictionaries are downloaded.

Thereafter, the setup script tries to re-import the hyphen package to install a default
set of dictionaries, unless the command line contains the 'no_dictionaries' command after 'install'. The script
then tries to install the metadata file by calling hyphen.dictools.install_dict_info. Then, the hyphenation dictionaries
for en_US (commonly used) and the local language, if different, are installed.

 
4. How to get dictionaries?
=================================
 
 Information on all hyphenation dictionaries available on the OpenOffice website is stored in hyphen.dict_info.
 You can also visit http://wiki.services.openoffice.org/wiki/Dictionaries for a
 complete list. Then use the dictools.install function to download and install the dictionary locally.


5. What's under the hood?
==============================

the C extension module 'hnj' used by the hyphenator class defined in
__init__.py contains the C library libhyphen which is used by OpenOffice.org, Mozilla
and alike. The C sources have not been changed, let alone hnjmalloc.c which has
been slightly modify to use pythonic memory management and error handling.

For further information on the hyphenation library and available dictionaries visit
http://wiki.services.openoffice.org/wiki/Dictionaries.


6. Testing
==============

This requires cloning the hg repository, as the test.py module is no longer part
of the source distribution. Please see the instructions in Demo/hyphen_test.py. All you need is a text file,
and its encoding. Copy the text file into the Demo/input directory, add a new function
call to hyphen_test.py, run it and read the .log file and the files created in the
output directory. There you will see the results for each word. You can specify a list
of dictionaries to be used. Then, hyphen_test will create an output file for each
dictionary used with a given word list.


7. Contributing and reporting bugs
=====================================

Contributions, comments, bug reports, criticism and praise can be sent to the author.

The sources of PyHyphen are found in a Mercurial repository at

    http://pyhyphen.googlecode.com
    
This is also where you can submit bug reports.


 
