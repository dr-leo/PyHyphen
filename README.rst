=================================
PyHyphen - hyphenation for Python
=================================

(c) 2008-2021 PyHyphen developers

Contact: fhaxbox66@gmail.com

Project home: https://github.com/dr-leo/PyHyphen

Mailing list: https://groups.google.com/group/pyhyphen


.. contents::

0. Quickstart
=============

With Python 3.7 or higher and a current version of pip, issue::

    $ pip install pyhyphen
    $ python
    >>> from hyphen import Hyphenator
    >>> # Download and install the hyphenation dict for German, if needed
    >>> h = Hyphenator('de_DE') # `language`defaults to 'en_US'
    >>> s = 'Politikverdrossenheit'
    >>> h.pairs(s)
    [['Po', 'litikverdrossenheit'],
    ['Poli', 'tikverdrossenheit'],
    ['Politik', 'verdrossenheit'],
    ['Politikver', 'drossenheit'],
    ['Politikverdros', 'senheit'],
    ['Politikverdrossen', 'heit']]
    >>> h.syllables(s)
    ['Po', 'li', 'tik', 'ver', 'dros', 'sen', 'heit']
    >>> h.wrap(s, 5)
    ['Poli-', 'tikverdrossenheit']

1. Overview
================

Pyhyphen is a pythonic interface to the hyphenation library used in projects such as LibreOffice and the Mozilla suite.
It comes with tools to download, install and uninstall hyphenation dictionaries from LibreOffice's Git repository.
PyHyphen provides the **hyphen**  package.

``hyphen.textwrap2`` is a  modified version of the familiar ``textwrap`` module
which wraps a text with hyphenation given a specified width. See the code example below.

PyHyphen supports Python 3.7  or higher.

1.1 Content of the hyphen package
---------------------------------

The 'hyphen' package contains the following:

- the ``hyphen.Hyphenator`` class: each instance of it can hyphenate and wrap words using a dictionary compatible with the hyphenation feature of
  LibreOffice and Mozilla. Required dictionaries are automatically downloaded at runtime, if not already installed.
- the ``dictools`` module contains useful functions such as for downloading and installing dictionaries from a configurable repository. After
  installation of PyHyphen, the LibreOffice repository is used by default. Dictionaries are storedin the platform-specific user's app directory.
- 'hyphen.hnj' is the C extension module that does all the ground work. It
  contains the high quality `C library libhyphen <http://sourceforge.net/projects/hunspell/files/Hyphen/>`_.
  It supports hyphenation with replacements as well as compound words.


1.2 The 'textwrap2' module
--------------------------

This module is an enhanced, though backwards-compatible version of the module 'textwrap' from the Python standard library. Unsurprisingly, it adds
hyphenation functionality to 'textwrap'. To this end, a new key word parameter ``use_hyphenator`` has been added to the ``__init__`` constructor
of the TextWrapper class which defaults to ``None``. It can be initialized with any hyphenator object.

2. Code examples
================

::

    >>> from hyphen import Hyphenator
    # Create some hyphenators
    h_de = Hyphenator('de_DE')
    h_en = Hyphenator('en_US')

    # Now hyphenate some words
    h_en.pairs('beautiful'
    [['beau', 'tiful'], ['beauti', 'ful']]

    h_en.wrap('beautiful', 6)
    ['beau-', 'tiful']

    h_en.wrap('beautiful', 7)
    ['beauti-', 'ful']

    h_en.syllables('beautiful')
    ['beau', 'ti', 'ful']

    >>> from hyphen.textwrap2 import fill
    >>> long_text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vehicula rhoncus nulla et vulputate. In et risus dignissim erat dapibus iaculis ac ut nunc. Etiam vestibulum elit eget purus fermentum, eu finibus velit eleifend.'
    >>> print(fill(long_text, width=40, use_hyphenator=h_en))
    Lorem ipsum dolor sit amet, consectetur
    adipiscing elit. Fusce vehicula rhoncus
    nulla et vulputate. In et risus dignis-
    sim erat dapibus iaculis ac ut nunc.
    Etiam vestibulum elit eget purus fermen-
    tum, eu finibus velit eleifend.

Just by creating ``Hyphenator`` objects for a language, the corresponding
dictionaries will be automatically downloaded.
For the HTTP connection to the LibreOffice server, PyHyphen uses the
familiar`requests <https://www.python-requests.org>`_
library. Requests are fully configurable to handle  proxies etc.
Alternatively, dictionaries may be manually
installed and listed with the ``dictools`` module::

    >>> from hyphen.dictools import *

    # Download and install some dictionaries in the default directory using the default
    # repository, usually the LibreOffice website
    >>> for lang in ['de_DE', 'en_US']:
        install(lang) # provide kwargs to configure the HTTP request

    # Show locales of installed dictionaries
    >>> list_installed()
    ['de', 'de_DE', 'en_PH', 'en_US']


3. Installation
===============

PyHyphen is pip-installable from PyPI. In most scenarios the easiest way to install PyHyphen is to type from the shell prompt::

    $ pip install pyhyphen

Besides the source distribution, there is a  wheel on PyPI for Windows. As the
C extension uses the limited C API, the wheel should work on all Python versions >= 3.7.

Building PyHyphen from source under Linux or MacOS should be straightforward. On Windows, the wheel isinstalled by default, so no C compiler is needed.

4. Managing dictionaries
========================

The ``dictools`` module contains a non-exhaustive list of available language strings that can be used to instantiate ``Hyphenator`` objects as shown above::

    >>> from hyphen import dictools
    >>> dictools.LANGUAGES
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


5. Contributing and reporting bugs
=====================================

Questions can be asked in the Google group (https://groups.google.com/group/pyhyphen). Or just send an e-mail to the authors.

Browse  or fork the  repository and report bugs at PyHyphen's `project site on Github <https://github.com/dr-leo/PyHyphen>`_.

Before submitting a PR, run the unit tests::

    $ make test

6. License
============

Without prejudice to third party licenses, PyHyphen is distributed under the Apache 2.0 license. PyHyphen ships with third party code including the hyphenation library hyphen.c and a patched version of the Python standard module textwrap.


7. Changelog
======================
