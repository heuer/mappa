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
    from setuptools.command.sdist import sdist as _sdist
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


class sdist(_sdist):
    def make_release_tree(self, basedir, files):
        from tm import plyutils
        import sys
        sys.path[0:0] = ['.', '..']
        from mql.tolog import lexer, parser
        plyutils.make_lexer(lexer)
        plyutils._make_parser_for_sdist(parser)
        files.extend(['mql/tolog/lexer_lextab.py', 'mql/tolog/parser_parsetab.py'])
        _sdist.make_release_tree(self, basedir, files)


setup(
      name = 'mql.tolog',
      version = '0.1.0',
      description = 'Topic Maps Query Language - tolog',
      long_description = '\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
      author = 'Lars Heuer',
      author_email = 'mappa@googlegroups.com',
      url = 'http://mappa.semagia.com/',
      license = 'BSD',
      packages = find_packages(),
      namespace_packages = ['mql'],
      entry_points = """
      """,
      platforms = 'any',
      zip_safe = False,
      include_package_data = True,
      package_data = {'': ['*.txt', '*.xsl']},
      cmdclass={'sdist': sdist},
      install_requires=['lxml>=2.3.1', 'tm>=0.1.7', 'mio.ctm>=0.1.3'],
      keywords = ['Topic Maps', 'Semantic Web', 'tolog'],
      classifiers = [
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
