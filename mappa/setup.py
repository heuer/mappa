# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Setup script for Mappa.
"""
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(name='Mappa',
      version='0.1.7',
      description='Mappa Topic Maps engine',
      long_description='\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
      author='Lars Heuer',
      author_email='mappa@googlegroups.com',
      url='http://mappa.semagia.com/',
      license='BSD',
      packages=find_packages(),
      platforms='any',
      zip_safe=False,
      include_package_data=True,
      package_data={'': ['*.txt']},
      install_requires=[
          'tm>=0.1.7',
          'mio.xtm>=0.1.7',
          'mio.ctm>=0.1.3',
          'mappa.xtm>=0.1.0',
          'mappa.cxtm>=0.1.0',
          'mappa.store.mem>=0.1.0'
      ],
      keywords=['Topic Maps', 'Semantic Web', 'TMDM'],
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
