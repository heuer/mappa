# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
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
Setup script for tm.
"""
import os
import sys
import re
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

if sys.version_info < (2, 3):
    raise Exception('Topic Maps requires Python 2.3 or higher')

v = file(os.path.join(os.path.dirname(__file__), 'tm', '__init__.py'))
m = re.compile(r'.*__version_info__\s*\=\s*\(([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*(?:\'|")([A-Za-z0-9]*)(?:\'|")\s*\)', re.S).match(v.read())
if not m:
    raise Exception("TM's author has done something wrong")
major, minor, micro, level = m.groups()
VERSION = '%s.%s.%s%s' % (major, minor, micro, level and '.%s' % level or '')
v.close()

setup(
      name = 'tm',
      version = VERSION,
      description = 'Topic Maps utilities',
      long_description = '\n\n'.join([open('README.txt').read(), open('CHANGES.txt').read()]),
      author = 'Lars Heuer',
      author_email = 'mappa@googlegroups.com',
      url = 'http://mappa.semagia.com/',
      license = 'BSD',
      packages = find_packages(),
      entry_points = {'tm.reader':''},
      platforms = 'any',
      zip_safe = False,
      include_package_data = True,
      package_data = {'': ['*.txt']},
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
