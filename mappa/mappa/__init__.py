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
from tm import Namespace, voc, ANY, UCS, XSD, TMDM, irilib
from mappa._internal.lit import Literal
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


class ModelConstraintViolation(Exception):
    """\
    Generic exception that indicates that some Topic Maps constraint has
    been violated.
    
    The object which has raised this exception can be accessed by ``reporter``
    (can be ``None``).
    """
    def __init__(self, msg, reporter=None):
        super(ModelConstraintViolation, self).__init__(msg)
        self.reporter = reporter


class IdentityViolation(ModelConstraintViolation):
    """\
    Exception that is raised if a uniqueness constraint is violated.
    
    I.e. trying to add a subject identifier to a topic that is already
    assigned to another topic.
    
    The object which has raised this exception can be accessed with 
    ``reporter``, the existing Topic Maps construct (the one with the
    identity) can be accessed by ``existing``.
    
    >>> t1 = tm.create_topic(sid='http://de.wikipedia.org/wiki/John_Lennon')
    >>> t2 = tm.create_topic(sid='http://a.non.existing.psi.for/John_Lennon')
    >>> try:
    ...     t2.add_sid('http://de.wikipedia.org/wiki/John_Lennon')
    ... except IdentityViolation, ex:
            ex.reporter is t2 # True
            ex.existing is t1 # True
    """
    def __init__(self, msg, reporter, existing):
        super(IdentityViolation, self).__init__(msg, reporter)
        self.existing = existing


class InternalError(Exception):
    """\
    Exception thrown in case of an internal error.
    """
    def __init__(self, msg):
        super(InternalError, self).__init__('INTERNAL ERROR: %s' % msg)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
