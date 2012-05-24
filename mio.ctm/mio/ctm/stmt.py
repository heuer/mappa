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
    if evt == 'startTopic':
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
    elif evt in ('startVariant', 'startScope'): # Special treatment since these methods take no argument
        res = u'handler.%s()' % evt
    elif 'start' in evt or evt in ('isa', 'ako', 'player', 'reifier', 'theme'):
        kind, identity = arg[0]
        if kind not in (consts.SID, consts.SLO, consts.IID):
            # Lookup the topic's identity
            res = u'handler.%s(ctx.get_topic_reference((%d, u"%s")))' % (evt, kind, identity)
        else:
            # Constant identity
            res = u'handler.%s((%d, u"%s"))' % (evt, kind, identity)
    elif 'end' in evt: # All 'end'-events but not 'endTopic'
        res = u'handler.%s()' % evt
    elif evt == 'value':
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
    elif evt == 'name_value':
        val = arg[0]
        if isinstance(val, tuple):
            if val[0] is consts.STRING:
                res = u'handler.value(u"%s")' % val[1]
            else:
                res = u'handler.value(utils.as_string_literal(ctx.get_literal((%d, u"%s")))[0])' % val
        else:
            res = u'handler.value(u"%s")' % val
    elif evt == 'call_template':
        name, args = arg
        res = [u'ctx.call_template(u"%s", [' % name]
        arguments = []
        if len(args) == 1 and args[0] is None:
            pass
        else:
            for kind, val in args:
                if kind in (consts.NAMED_WILDCARD, consts.WILDCARD):
                    arguments.append('ctx.get_topic_reference((%d, u"%s"))' % (kind, val))
                else:
                    arguments.append(u'(%r, %r)' % (kind, val))
        res.append(u', '.join(arguments))
        res.append(u'])')
        res = u''.join(res)
    elif evt in ('itemIdentifier', 'subjectLocator', 'subjectIdentifier'):
        res = u'handler.%s(u"%s")' % (evt, arg[0])
    elif '_variable' in evt:
        res = u'handler.%s(ctx.get_literal((%d, u"%s"))[1])' % (evt.split('_')[0], consts.VARIABLE, arg[0])
    elif evt == 'identity':
        var = arg[0]
        res = u'utils.handle_identity(handler, ctx, (%d, u"%s"))' % (var[0], var[1])
    else:
        raise Exception('Internal error: Unhandled event "%s"' % evt)
    return res
