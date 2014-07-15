# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module translates CTM templates into Python code.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev:$ - $Date:$
:license:      BSD license
"""
from . import consts

_UNDEFINED = object()


def make_statement(evt, arg=_UNDEFINED):
    """\
    Returns Python code for the provided event (i.e. 'startTopic').

    To execute the Python code, the ``internal_utils`` module must be available 
    (from mio.reader.ctm) and a variable ``handler`` which must be bound to
    a ``SimpleMapHandler`` instance and ``ctx`` which must be bound to 
    a ``TemplateContext`` instance.
    """
    if evt == u'startTopic':
        kind, identity = arg
        res = []
        if kind not in (consts.SID, consts.SLO, consts.IID):
            # Lookup the identity
            res.append(u'focus = ctx.get_topic_reference((%d, u"%s"))' % (kind, identity))
        else:
            # Constant identity
            res.append(u'focus = (%d, u"%s")' % (kind, identity))
        res.append(u'handler.startTopic(focus)')
        res.append(u'ctx.push_focus(focus)')
        res = u'\n'.join(res)
    elif evt == 'endTopic':
        res = u'handler.endTopic()\nctx.pop_focus()' 
    elif evt in (u'startVariant', u'startScope'): # Special treatment since these methods take no argument
        res = u'handler.%s()' % evt
    elif u'start' in evt or evt in (u'isa', u'ako', u'player', u'reifier', u'theme'):
        kind, identity = arg[0]
        if kind not in (consts.SID, consts.SLO, consts.IID):
            # Lookup the topic's identity
            res = u'handler.%s(ctx.get_topic_reference((%d, u"%s")))' % (evt, kind, identity)
        else:
            # Constant identity
            res = u'handler.%s((%d, u"%s"))' % (evt, kind, identity)
    elif u'end' in evt: # All 'end'-events but not 'endTopic'
        res = u'handler.%s()' % evt
    elif evt == u'value':
        kind, val = arg[0]
        if kind not in (consts.VARIABLE, consts.LITERAL):
            res = u'handler.value(*utils.as_literal((%d, u"%s")))' % (kind, val)
        else:
            if kind is consts.VARIABLE:
                res = u'handler.value(*utils.as_literal(ctx.get_literal((%d, u"%s"))))' % (kind, val)
            else:
                value, datatype = val
                #TODO: What are we doing here and why is this code not covered by the test cases? 
                # Should raise an error, shouldn't it?
                res = u'handler.value(utils.as_string(ctx.get_literal((%d, u"%s")))[0], ctx.get_literal((%d, u"%s"))[1])' % (value, datatype)
    elif evt == u'name_value':
        val = arg[0]
        if isinstance(val, tuple):
            if val[0] is consts.STRING:
                res = u'handler.value(u"%s")' % val[1]
            else:
                res = u'handler.value(utils.as_string_literal(ctx.get_literal((%d, u"%s")))[0])' % val
        else:
            res = u'handler.value(u"%s")' % val
    elif evt == u'call_template':
        name, args = arg
        res = [u'ctx.call_template(u"%s", [' % name]
        arguments = []
        if len(args) == 1 and args[0] is None:
            pass
        else:
            for kind, val in args:
                if kind in (consts.NAMED_WILDCARD, consts.WILDCARD):
                    arguments.append(u'ctx.get_topic_reference((%d, u"%s"))' % (kind, val))
                else:
                    arguments.append(u'(%r, %r)' % (kind, val))
        res.append(u', '.join(arguments))
        res.append(u'])')
        res = u''.join(res)
    elif evt in (u'itemIdentifier', u'subjectLocator', u'subjectIdentifier'):
        res = u'handler.%s(u"%s")' % (evt, arg[0])
    elif u'_variable' in evt:
        res = u'handler.%s(ctx.get_literal((%d, u"%s"))[1])' % (evt.split(u'_')[0], consts.VARIABLE, arg[0])
    elif evt == u'identity':
        var = arg[0]
        res = u'utils.handle_identity(handler, ctx, (%d, u"%s"))' % (var[0], var[1])
    else:
        raise Exception('Internal error: Unhandled event "%s"' % evt)
    return res
