# setup.py for the PyHyphen hyphenation package
# (c) 2007-2021 Dr. Leo (fhaxbox66@gmail.com) and other developers

from setuptools import setup, Extension, find_packages


arg_dict = dict(
    name="PyHyphen",
    author="Dr. Leo & Regis Behmo",
    author_email="fhaxbox66@googlemail.com",
    url="https://github.com/dr-leo/PyHyphen",
    description="The hyphenation library of LibreOffice and FireFox wrapped for Python",
    long_description=open('README.rst', 'rt').read(),
    long_description_content_type='text/rst',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 4 - Beta',
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
    ext_modules=[
        Extension('hyphen.hnj', ['lib/hnjmodule.c',
                                 'lib/hyphen.c',
                                 'lib/hnjalloc.c'],
                  include_dirs=['lib'],
                  py_limited_api=True)
                  ],
    install_requires=['appdirs', "requests"],
    include_package_data=True,
)


setup(**arg_dict)
