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
        from mio.ltm import lexer, parser
        plyutils.make_lexer(lexer)
        plyutils._make_parser_for_sdist(parser)
        files.extend(['mio/ltm/lexer_lextab.py', 'mio/ltm/parser_parsetab.py'])
        _sdist.make_release_tree(self, basedir, files)


setup(
    name='mio.ltm',
    version='0.1.5',
    description='Linear Topic Maps (LTM) syntax reader',
    long_description='\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
    author='Lars Heuer',
    author_email='mappa@googlegroups.com',
    url='http://mappa.semagia.com/',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['mio'],
    entry_points="""
    [mio.reader]
    ltm = mio.ltm
    """,
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['*.txt']},
    cmdclass={'sdist': sdist},
    install_requires=['tm>=0.1.7'],
    keywords=['Topic Maps', 'Semantic Web', 'LTM'],
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
