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
The Mappa Topic Maps engine. :)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import pkg_resources
from tm.namespace import Namespace
from tm import voc, ANY, UCS, XSD, TMDM, irilib
from mappa._internal.lit import Literal
from mappa._internal.exceptions import ModelConstraintViolation, IdentityViolation, InternalError
try:
    __version__ = pkg_resources.get_distribution('mappa').version
except Exception:
    __version__ = 'unknown'
__all__ = ['Literal', '__version__',
           'Namespace', 'voc', 'ANY', 'UCS', 'XSD', 'TMDM', 'irilib',    # from PyTM
           'connect',
           'ModelConstraintViolation', 'IdentityViolation']

def connect(backend='mem', **kw):
    """\
    Creates / returns a connection with the specified configuration.
    If no configuration is provided, an in-memory connection will be created.
    
    This function uses the ``backend`` keyword from the `config` only. The
    configuration is handled over to the concrete implementation of the 
    backend which may or may not require further configuration key/value 
    pairs.
    
    Whether this function returns a new connection instance or if an existing
    instance is returned, depends on the implementation and the configuration.
    
    Usage::
    
        >>> conn = connect()
        >>> tm = conn.create('http://www.semagia.com/somemap/')
        >>> tm.iri
        'http://www.semagia.com/somemap/'
        >>> # Creating a connection with a Durus backend
        >>> conn2 = connect(backend='durus')
        >>> tm2 = conn2.create('http://www.semagia.com/another-map')
        >>> tm2.iri == 'http://www.semagia.com/another-map'
        True
    """
    store_name = backend
    store = None
    for ep in pkg_resources.iter_entry_points('mappa.store'):
        if ep.name == store_name:
            store = ep.load()
            break
    if not store:
        raise Exception('Cannot find the store "%s"' % store_name)
    return store.create_connection(**kw)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
