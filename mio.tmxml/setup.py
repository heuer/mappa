# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Setup script for deserializer.
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='mio.tmxml',
    version='0.3.0',
    description='TM/XML syntax reader',
    long_description='\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
    author='Lars Heuer',
    author_email='mappa@googlegroups.com',
    url='http://mappa.semagia.com/',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['mio'],
    entry_points="""
    [mio.reader]
    tm/xml = mio.tmxml
    """,
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.txt']},
    install_requires=['tm'],
    keywords=['Topic Maps', 'Semantic Web', 'TMXML'],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ]
)
