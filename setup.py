# setup.py for the PyHyphen hyphenation package
# (c) Dr. Leo (fhaxbox66 <at> gmail >dot< com)

import os
import platform
import sys
from setuptools import setup, Extension


arg_dict = dict(
    name="PyHyphen",
    version="3.0.0",
    author="Dr. Leo",
    author_email="fhaxbox66@googlemail.com",
    url="https://bitbucket.org/fhaxbox66/pyhyphen",
    description="The hyphenation library of LibreOffice and FireFox wrapped for Python",
    long_description=open('README.rst', 'r').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic'
    ],
    packages=['hyphen', 'textwrap2'],
    ext_modules=[
        Extension('hyphen.hnj', ['src/hnjmodule.c',
                                 'src/hyphen.c',
                                 'src/hnjalloc.c'],
                  include_dirs=['include'])],
    install_requires=['appdirs', 'six'],
)


# Check for a binary shipping with this distribution and use it instead of compiling
# the C sources, unless --force_build_ext is given.
if '--force_build_ext' in sys.argv:
    sys.argv.remove('--force_build_ext')
else:
    # construct string describing platform
    if platform.system() == 'Windows':
        if sys.maxsize > 2**32:
            platform_descr = 'amd64'
        else:
            platform_descr = 'win32'
    else:
        # TODO this does not work on Linux: binary is recompiled from scratch
        platform_descr = platform.system()

    bin_file = os.path.join('bin', 'hnj' + '.' + platform_descr + '-' + sys.version[:3] + '.pyd')
    print(bin_file)
    if os.path.exists(bin_file):
        print("""Found a suitable binary version of the C extension module.
        This binary will be installed rather than building it from source.
        However, if you prefer compiling, reenter 'python setup.py <command> --force_build_ext'.""")
        arg_dict['package_data'] = {'hyphen': [bin_file]}
        arg_dict.pop('ext_modules') # don't try to build ext modules

setup(**arg_dict)
