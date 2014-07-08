# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
    consts.CTM_INTEGER: u'http://psi.topicmaps.org/iso13250/ctm-integer'
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
    Issues a ``subjectIdentifier`` event.
    
    `handler`
        An IMapHandler instance.
    `ctx`
        A TemplateContext instance
    `identity`
        A tuple (VARIABLE, name)
    """
    kind, iri = ctx.get_topic_reference(identity)
    if not kind == consts.IRI:
        raise mio.MIOException('Expected an IRI, got: (%s, %s)' % (kind, iri))
    handler.subjectIdentifier(iri)
