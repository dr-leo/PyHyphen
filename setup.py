# setup.py for the PyHyphen hyphenation package
# (c) Dr. Leo (fhaxbox66 <at> gmail >dot< com)

from setuptools import setup, Extension, find_packages


arg_dict = dict(
    name="PyHyphen",
    version="4.0.0",
    author="Dr. Leo & Regis Behmo",
    author_email="fhaxbox66@googlemail.com",
    url="https://github.com/dr-leo/PyHyphen",
    description="The hyphenation library of LibreOffice and FireFox wrapped for Python",
    long_description=open('README.rst', 'r').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Development Status : 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: C',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic'
    ],
    packages=find_packages(where='src', include=['hyphen']),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ["wraptext = textwrap2.cli:main"]
    },
    ext_modules=[
        Extension('hyphen.hnj', ['lib/hnjmodule.c',
                                 'lib/hyphen.c',
                                 'lib/hnjalloc.c'],
                  include_dirs=['lib'])],
    install_requires=['appdirs', "requests"],
)


setup(**arg_dict)
