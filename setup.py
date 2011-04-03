
import sys, os, shutil, codecs, locale
from string import Template
from distutils.core import setup, Extension



# URL of the default repository. It goes into config.py.
# Change this if you want to download dictionaries from somewhere else by default.
# Note that you can also specify the repository individualy
# when calling hyphen.dictools.install.
default_repo = 'http://ftp.services.openoffice.org/pub/OpenOffice.org/contrib/dictionaries/'


# Copy version-specific files
files = {'__init__.py' : 'hyphen/',
        'dictools.py' : 'hyphen/',
        'config.py' : 'hyphen/',
        'hnjmodule.c' : 'src/',
        'textwrap2.py' : './'}
        
        # create package directory:
if not os.path.exists('hyphen'): os.mkdir('hyphen')

#copy version-specific files
ver = sys.version[0]
py3k = (ver == '3')
for file_name, dest in files.items():
    shutil.copy(ver + '.x/' + file_name, dest + file_name)



longdescr = open('README.txt').read()



arg_dict = dict(
    name = "PyHyphen", version = "1.0beta1",
    author = "Dr. Leo",
    author_email = "fhaxbox66@googlemail.com",
    url = "http://pyhyphen.googlecode.com",
    description = "The hyphenation library of OpenOffice and FireFox wrapped for Python",
    long_description = longdescr,
    classifiers = [
        'Intended Audience :: Developers',
         'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: C',
                'Topic :: Text Processing',
                'Topic :: Text Processing :: Linguistic'
    ],
    packages = ['hyphen'],
    ext_modules = [
      Extension('hyphen.hnj', ['src/hnjmodule.c',
                                  'src/hyphen.c',
                                   'src/hnjalloc.c' ],
                                   include_dirs = ['include'])],
    py_modules = ['textwrap2'],
    provides = ['hyphen', 'textwrap2']
)


# Check for a binary shipping with this distribution and use it instead of compiling
# the C sources, unless --force_build_ext is given.
if len(set(('install', 'bdist_wininst', 'bdist')) - set(sys.argv)) < 3:
    if  '--force_build_ext' in sys.argv:
        sys.argv.remove('--force_build_ext')
    else:
        bin_file = ''.join(('bin/hnj', '.', sys.platform, '-', sys.version[:3], '.pyd'))
        if os.path.exists(bin_file):
            shutil.copy(bin_file, './hyphen/hnj.pyd')
            arg_dict['package_data'] = {'hyphen' : ['hnj.pyd']}
            arg_dict.pop('ext_modules')
            sys.stdout.write("Found a suitable binary version of the C extension module. This binary will be installed rather than building it from source.\n\
            However, if you prefer compiling, reenter 'python setup.py <command> --force_build_ext'.")


setup(**arg_dict)

# clean up
shutil.rmtree('hyphen') # it would disturb the following import of hyphen
os.remove('textwrap2.py')
os.remove('src/hnjmodule.c')


# Configure the path for dictionaries in config.py
if 'install' in sys.argv:
    sys.stdout.write("Adjusting /.../hyphen/config.py... ")
    # We catch ImportErrors to handle situations where the
    # hyphen package has been
    # installed in a directory that is not listed in
    # sys.path. This occurs, e.g.,
    # when creating a Debian package.
    try:
        import hyphen
        mod_path = hyphen.__path__[0] + '/config.py'
        content = codecs.open(mod_path, 'r', 'utf8').read()
        new_content = Template(content).substitute(path = hyphen.__path__[0],
    repo = default_repo)
    
        # Remove config.pyc to make sure the modified .py file is byte-compiled
        # when re-importing. Otherwise the new config.py might have
        # the same time stamp as the old one
        os.remove(mod_path + 'c')
    
        # Write the new config.py
        codecs.open(mod_path, 'w', 'utf8').write(new_content)
        sys.stdout.write("Done.\n")
        
        # Install dictionaries
        if '--no_dictionaries' not in sys.argv:
            # install dict_info and dictionaries
            if py3k: from imp import reload
            reload(hyphen.config)
            reload(hyphen)
            from hyphen.dictools import install, install_dict_info
            sys.stdout.write('Installing dictionary info...')
            hyphen.dict_info = install_dict_info()
            sys.stdout.write(' Done.\n')
            sys.stdout.write('Installing dictionaries... en_US ')
            install('en_US')
            
            # Install dict for local language if needed
            locale.setlocale(locale.LC_ALL, '')
            local_lang = locale.getlocale()[0]
            if local_lang != 'en_US':
                if local_lang in hyphen.dict_info:
                    sys.stdout.write(local_lang + ' ')
                    install(local_lang)
                    sys.stdout.write('Done.\n')
            else:
                sys.stdout.write('(No dictionary for local language found)\n')
            
    except ImportError:
        sys.stderr.write("""Warning:
        Could not import hyphen package.
        You may wish to adjust config.py
            manually or run setup.py with different options.
            No dictionary has been installed.\n""")

    