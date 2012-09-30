
import sys, os, shutil, imp, py_compile, codecs, locale
from string import Template
from distutils.core import setup, Extension



# URL of the default repository. It goes into config.py.
# Change this if you want to download dictionaries from somewhere else by default.
# Note that you can also specify the repository individualy
# when calling hyphen.dictools.install.
default_repo = 'http://cgit.freedesktop.org/libreoffice/dictionaries/plain/dictionaries/'


# Copy version-specific files
# to be copied from 2.x/
files_from_2x = {
    '__init__.py' : './hyphen/',
    'config.py' : './hyphen/',
    'dictools.py' : './hyphen/'}

# from either 2.x/ or 3.x/
files_from_any = {
    'hnjmodule.c' : 'src/',
    'textwrap2.py' : './'}
        

#copy version-specific files
ver = sys.version[0]
py3k = (ver == '3')
if not os.path.exists('hyphen'):
    os.mkdir('hyphen')
for file_name, dest in files_from_2x.items():
    shutil.copy('2.x/' + file_name, dest + file_name)

for file_name, dest in files_from_any.items():
    shutil.copy(ver + '.x/' + file_name, dest + file_name)


# refactor 2to3
if py3k:
    import lib2to3.main
    lib2to3.main.main('lib2to3.fixes', args = '--no-diffs -wn -f unicode -f urllib \
        hyphen'.split())


longdescr = open('README.txt', 'r').read()



arg_dict = dict(
    name = "PyHyphen",
    version = "2.0",
    author = "Dr. Leo",
    author_email = "fhaxbox66@googlemail.com",
    url = "http://pyhyphen.googlecode.com",
    description = "The hyphenation library of LibreOffice and FireFox wrapped for Python",
    long_description = longdescr,
    classifiers = [
        'Intended Audience :: Developers',
         'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
'Programming Language :: Python :: 3.3',
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
        pkg_path = imp.find_module('hyphen')[1]
        mod_path = pkg_path + '/config.py'
        content = codecs.open(mod_path, 'r', 'utf8').read()
        new_content = Template(content).substitute(path = pkg_path,
            repo = default_repo)
        
        # Write the new config.py
        codecs.open(mod_path, 'w', 'utf8').write(new_content)
        py_compile.compile(mod_path)
        sys.stdout.write("Done.\n")
        
        # Delete any existing dict registry file
        reg_file = pkg_path + '/hyphen_dict_info.pickle'
        if os.path.exists(reg_file):
            os.remove(reg_file)

        # Install dictionaries
        if '--no_dictionaries' not in sys.argv:
            from hyphen.dictools import install
            sys.stdout.write('Installing dictionaries... en_US ')
            install('en_US')
            
            # Install dict for local language if needed
            locale.setlocale(locale.LC_ALL, '')
            local_lang = locale.getlocale()[0]
            if local_lang != 'en_US':
                sys.stdout.write(local_lang + ' ')
                try:
                    install(local_lang)
                    sys.stdout.write('Done.\n')
                except Error:
                    sys.stdout.write('Failed.\n')

            
    except ImportError:
        sys.stderr.write("""Warning:
        Could not import hyphen package.
        You may wish to adjust config.py
            manually or run setup.py with different options.
            No dictionary has been installed.\n""")

    