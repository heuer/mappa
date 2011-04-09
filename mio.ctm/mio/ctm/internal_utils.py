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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
CTM related utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, XSD
from . import consts

_CONST2IRI = {
    consts.STRING: XSD.string,
    consts.IRI: XSD.anyURI,
    consts.DECIMAL: XSD.decimal,
    consts.INTEGER: XSD.integer,
    consts.DATE: XSD.date,
    consts.DATE_TIME: XSD.dateTime,
    consts.CTM_INTEGER: 'http://psi.topicmaps.org/iso13250/ctm-integer'
    }

def as_literal(lit):
    kind, val = lit
    iri = _CONST2IRI.get(kind)
    if iri is None and kind == consts.LITERAL:
        return val[0], val[1][1]
    elif not iri:
        raise mio.MIOException('Illegal literal "%r"' % val)
    return val, iri

def as_string_literal(lit):
    """\
    Checks if the provided literal is a string literal and returns 
    it with the correct xsd:string URI.
    """
    kind, val = lit
    if not kind == consts.STRING:
        raise mio.MIOException('Expected a string literal, got: "(%s, %s)"' % (kind, val))
    return val, XSD.string

def handle_identity(handler, ctx, identity):
    """\
    Issues a ``subjectIdentifier``, ``subjectLocator`` or ``itemIdentifier``
    event. Which event is issued depends on the value to which the variable 
    ``identity`` is bound to.
    
    `handler`
        An IMapHandler instance.
    `ctx`
        A TemplateContext instance
    `identity`
        A tuple (VARIABLE, name)
    """
    kind, iri = ctx.get_topic_reference(identity)
    if kind == consts.IID:
        handler.itemIdentifier(iri)
    elif kind == consts.SID:
        handler.subjectIdentifier(iri)
    elif kind == consts.SLO:
        handler.subjectLocator(iri)
    else:
        raise mio.MIOException('Unknown identity: (%s, %s)' % (kind, iri))
