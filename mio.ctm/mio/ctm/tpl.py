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
Template-related classes.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
class Template(object):
    """\
    Represents a CTM template.
    """
    __slots__ = ['name', 'args', '_body', '_code']

    def __init__(self, name, args, body):
        """\

        `name`
            Name of the template
        `args`
            A (maybe empty) tuple of variables
        `body`
            The template body, a ``list``
        """
        self.name = name
        self.args = args
        self._body = body
        self._code = None

    def __call__(self, ctx):
        if not self._code:
            # 1st invocation: Compile the body into Python code.
            self._code = compile(u'\n'.join(self._body), u'%s-%d' % (self.name, len(self.args)), 'exec')
            del self._body # Not needed anymore.
        eval(self._code, {'ctx': ctx, 'handler': ctx.handler})


class TemplateInvocation(object):
    """\
    Represents a CTM template invocation.
    """
    __slots__ = ['_name', '_tpl', '_args', '_bindings']

    def __init__(self, name, args):
        """\
        
        `name`
            Name of the template
        `args`
            Values which should be submitted to the template.
        """
        self._name = name
        self._tpl = None
        self._args = args
        self._bindings = None
    
    def __call__(self, env):
        if not self._tpl:
            # 1st invocation: Fetch the template from the environment
            self._init(env.get_template(self._name, self._args))
        ctx = env.new_context(self._bindings)
        env.push_context(ctx)
        self._tpl(ctx)
        env.pop_context()

    def _init(self, tpl):
        self._tpl = tpl
        self._bindings = dict(zip(tpl.args, self._args))
        del self._args # Not needed anymore
