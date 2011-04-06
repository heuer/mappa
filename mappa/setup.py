# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name 'Semagia' nor the name 'Mappa' nor the names of the
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

if sys.version_info < (2, 4):
    raise Exception('Requires Python 2.4 or higher')

setup(
      name = 'Mappa',
      version = '0.1.7',
      description = 'Mappa Topic Maps engine',
      long_description = '\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
      author = 'Lars Heuer',
      author_email = 'mappa@googlegroups.com',
      url = 'http://mappa.semagia.com/',
      license = 'BSD',
      packages = find_packages(),
      platforms = 'any',
      zip_safe = False,
      include_package_data = True,
      package_data = {'': ['*.txt']},
      install_requires=['tm',
                        'mio.xtm>=0.1.0',
                        'mio.ctm>=0.1.0',
                        'mappa.xtm>=0.1.0',
                        'mappa.cxtm>=0.1.0',
                        'mappa.store.mem>=0.1.0'],
      keywords = ['Topic Maps', 'Semantic Web', 'TMDM'],
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
