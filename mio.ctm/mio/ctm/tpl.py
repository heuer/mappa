# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
        eval(self._code, {u'ctx': ctx, u'handler': ctx.handler})


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
