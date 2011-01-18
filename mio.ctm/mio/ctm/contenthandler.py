# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2010 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Content handlers.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev:$ - $Date:$
:license:      BSD license
"""
from tm import mio
from tm.irilib import resolve_iri
from mio.ctm import consts, tpl, stmt, internal_utils as iutils

def _maphandler(content_handler):
    """\
    Returns the ``tm.mio.IMapHandler`` from the `content_handler` 
    """
    return content_handler.environment.maphandler

def _check_valid_global_identity(identity):
    """\
    Raises an exception if the provided `identity` is not valid in the 
    global context.
    """
    if identity[0] not in (consts.IID, consts.SID, consts.SLO):
        raise mio.MIOException('Unknown identity type: %s' % identity[0])

class ContentHandler(object):
    """\
    Base class for all content handlers.
    """
    #TODO: Remove me?!?
    pass

class GlobalScopeContentHandler(ContentHandler):
    """\
    ContentHandler which is usable outside of templates.
    """
    def __init__(self, env):
        super(GlobalScopeContentHandler, self).__init__()
        self._stack = []
        self.environment = env

    def startTopic(self, identity):
        _check_valid_global_identity(identity)
        _maphandler(self).startTopic(identity)
        self._stack.append(identity)

    def start_topic_wildcard(self, name=None):
        identity = self.environment.topic_identity(name)
        self.startTopic(identity)
        return identity

    def endTopic(self):
        _maphandler(self).endTopic()
        self._stack.pop()

    def __getattr__(self, name):
        def call_event(arg=None):
            op = getattr(_maphandler(self), name)
            if arg:
                if not isinstance(arg, basestring):
                    _check_valid_global_identity(arg)
                op(arg)
            else:
                op()
        return call_event

    def ako(self, identity):
        _check_valid_global_identity(identity)
        _maphandler(self).ako(self._stack[-1], identity)

    def call_template(self, name, args):
        if self._stack: # Within a topic?
            args.insert(0, self._stack[-1]) # Add topic as 1st arg
        tpl_invocation = tpl.TemplateInvocation(name, args)
        tpl_invocation(self.environment)

    def value(self, lit):
        _maphandler(self).value(*iutils.as_literal(lit)) #pylint: disable-msg=W0142
    
    def name_value(self, lit):
        _maphandler(self).value(iutils.as_string_literal(lit)[0])


class TemplateScopeContentHandler(ContentHandler):
    """\
    ContentHandler which is responsible for templates.
    """
    def __init__(self, env, name, args):
        super(TemplateScopeContentHandler, self).__init__()
        self.environment = env
        self._body = ['from mio.ctm import internal_utils as utils']
        self.template = tpl.Template(name, args, self._body)
        self._topic_count = 0

    def start_topic_wildcard(self, name=None):
        #TODO: Wouldn't it be more clever to create an internal variable here?
        # May shorten the stmt code for template calls as well. 
        identity = name and (consts.NAMED_WILDCARD, name) or (consts.WILDCARD, '%s_%s' % (self.template.name, self._topic_count))
        self.startTopic(identity)
        return identity

    def startTopic(self, identity):
        self._topic_count+=1
        self._body.append(stmt.make_statement('startTopic', identity))

    def endTopic(self):
        self._topic_count-=1
        self._body.append(stmt.make_statement('endTopic'))

    def call_template(self, name, args):
        if self._topic_count != 0: # Within a topic?
            args.insert(0, consts.TOPIC_IN_FOCUS) # Add topic as 1st arg
        self._body.append(stmt.make_statement('call_template', (name, args)))

    def __getattr__(self, name):
        def append_event(*arg):
            if arg:
                statement = stmt.make_statement(name, arg) 
            else:
                statement = stmt.make_statement(name)
            self._body.append(statement)
        return append_event


from tm import TMDM
_TOPICNAME = mio.SUBJECT_IDENTIFIER, TMDM.topic_name
del TMDM

class MainContentHandler(ContentHandler):
    """\
    This content handler delegates all parser events to an underlying content 
    handler.
    This content handler is responsible to switch the underlying content 
    context dependent.
    """
    def __init__(self, environment):
        super(MainContentHandler, self).__init__()
        self._handler = GlobalScopeContentHandler(environment)
        self._global_handler = self._handler

    def resolve_ident(self, ident):
        """\
        Creates an absolute IRI from the provided identifier ``ident``.
        
        If the topic map was included by another topic map, a ``startTopic``
        event is issued; followed by ``itemIdentifier`` events where ``ident``
        is resolved against all IRIs from which this topic map is included from;
        followed by an ``endTopic`` event.
        """
        res = self.environment.resolve_ident(ident)
        if self.environment.included_by:
            handler = self._handler
            handler.startTopic((consts.IID, res))
            frag = '#' + ident
            for iri in self.environment.included_by:
                handler.itemIdentifier(resolve_iri(iri, frag))
            handler.endTopic()
        return res

    def __getattr__(self, name):
        """\
        Delegates all unimplemented methods to the underlying content handler.
        """
        return getattr(self._handler, name)

    def startName(self, identity=None):
        self._handler.startName(identity or _TOPICNAME)

    def start_template(self, name, args):
        self._handler = TemplateScopeContentHandler(self._handler.environment, name, args)
    
    def end_template(self):
        tpl = self._handler.template
        self._global_handler.environment.register_template(tpl.name, tpl)
        self._handler = self._global_handler

    environment = property(lambda self: self._handler.environment)
