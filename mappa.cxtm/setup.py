# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Setup script
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='mappa.cxtm',
    version='0.1.0',
    description='Canonical Topic Maps (CXTM) writer',
    long_description='\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
    author='Lars Heuer',
    author_email='mappa@googlegroups.com',
    url='http://mappa.semagia.com/',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['mappaext'],
    entry_points="""
      [mappaext.writer]
      cxtm = mappaext.cxtm
      """,
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.txt']},
    install_requires=[],
    keywords=['Topic Maps', 'Semantic Web', 'CXTM'],
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
