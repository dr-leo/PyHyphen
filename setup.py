# setup.py for the PyHyphen hyphenation package
# (c) Dr. Leo (fhaxbox66 <at> gmail >dot< com)

import locale
import os
import platform
import shutil
import sys
from distutils.core import setup, Extension
from warnings import warn


current_dir = os.path.abspath(os.path.dirname(__file__))

# Copy version-specific files
# to be copied from 2.x/
files_from_2x = {
    '__init__.py': 'hyphen',
    'config.py': 'hyphen',
    'dictools.py': 'hyphen'
}

# from either 2.x/ or 3.x/
files_from_any = {
    'hnjmodule.c': 'src',
    'textwrap2.py': ''
}


# copy version-specific files
ver = sys.version[0]
py3k = (ver == '3')
if not os.path.exists(os.path.join(current_dir, 'hyphen')):
    os.mkdir(os.path.join(current_dir, 'hyphen'))
for file_name, dest in files_from_2x.items():
    shutil.copy(os.path.join(current_dir, '2.x', file_name),
                os.path.join(current_dir, dest, file_name))

for file_name, dest in files_from_any.items():
    shutil.copy(os.path.join(current_dir, ver + '.x/', file_name),
                os.path.join(current_dir, dest, file_name))


# refactor 2to3
if py3k:
    import lib2to3.main
    lib2to3.main.main('lib2to3.fixes', args='--no-diffs -wn -f unicode -f urllib \
        hyphen'.split())


longdescr = open('README.txt', 'r').read()


arg_dict = dict(
    name="PyHyphen",
    version="2.0.9",
    author="Dr. Leo",
    author_email="fhaxbox66@googlemail.com",
    url="https://bitbucket.org/fhaxbox66/pyhyphen",
    description="The hyphenation library of LibreOffice and FireFox wrapped for Python",
    long_description=longdescr,
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
    packages=['hyphen'],
    ext_modules=[
        Extension('hyphen.hnj', ['src/hnjmodule.c',
                                 'src/hyphen.c',
                                 'src/hnjalloc.c'],
                  include_dirs=['include'])],
    py_modules=['textwrap2'],
    provides=['hyphen', 'textwrap2']
)


# Check for a binary shipping with this distribution and use it instead of compiling
# the C sources, unless --force_build_ext is given.
if len(set(('install', 'bdist_wininst', 'bdist')) - set(sys.argv)) < 3:
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
            platform_descr = platform.system()

        bin_file = os.path.join(
            current_dir, 'bin', 'hnj' + '.' + platform_descr + '-' + sys.version[:3] + '.pyd')
        if os.path.exists(bin_file):
            shutil.copy(bin_file, './hyphen/hnj.pyd')
            arg_dict['package_data'] = {'hyphen': ['hnj.pyd']}
            arg_dict.pop('ext_modules')
            print("""Found a suitable binary version of the C extension module.
            This binary will be installed rather than building it from source.
            However, if you prefer compiling, reenter 'python setup.py <command> --force_build_ext'.""")


setup(**arg_dict)

# clean up
# it would disturb the following import of hyphen
shutil.rmtree(os.path.join(current_dir, 'hyphen'))
os.remove(os.path.join(current_dir, 'textwrap2.py'))
os.remove(os.path.join(current_dir, 'src', 'hnjmodule.c'))


# We catch ImportErrors to handle situations where the
# hyphen package has been
# installed in a directory that is not listed in
# sys.path. This occurs, e.g.,
# when creating a Debian package.
# Install dictionaries
if '--no_dictionaries' not in sys.argv:
    try:
        from hyphen.dictools import is_installed, install
    except ImportError:
        warn(
            """Could not import hyphen package. You may wish to adjust config.py manually
or run setup.py with different options. No dictionary has been installed."""
        )
    else:
        if not is_installed('en_US'):
            print('Installing dictionary en_US')
            install('en_US')

        # Install dict for local language if needed
        try:
            locale.setlocale(locale.LC_ALL, '')
            local_lang = locale.getlocale()[0]
            # Install local dict only if locale has been read (= is not None)
            # and local_lang is not en_US.
            if local_lang and local_lang != 'en_US' and not is_installed(local_lang):
                print('Installing dictionary', local_lang)
                install(local_lang)
        except Exception:
            warn('Could not install dictionary for local language.')
