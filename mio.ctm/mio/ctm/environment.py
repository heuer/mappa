# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Environment.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, irilib, TM, Source
from tm.mio.deserializer import Context
from . import consts, tpl

_IRI2SYNTAX = {
    TM.ctm: 'ctm',
    TM.xtm: 'xtm'
    }

class Environment(object):
    """\
    Parser environment to keep track of registered templates, prefixes etc.
    """
    def __init__(self, handler, iri, subordinate, 
                 included_by=None, context=None, wildcard_counter=0):
        """\
        
        `handler`
            A IMapHandler instance.
        `iri`
            The document / base IRI used to resolve identifiers / IRIs against
        `subordinate`
            Indicates if the topic map was included / merged by another topic map.
        `included_by`
            Either ``None`` or a list of document IRIs from which the topic map
            was included by.
        `context` 
            The deserializer context (used to keep track of already loaded topic
            maps)
        `wildcard_counter`
            The wildcard counter. 
        """
        self._prefixes = {}
        self._wc2identity = {}
        self._maphandler = handler
        self.base = iri
        self.wildcard_counter = wildcard_counter
        self._subordinate = subordinate
        self._context = context or Context()
        self.templates = {}
        self._tpl_context = TemplateContext(self)
        self.included_by = included_by or []

    def add_prefix(self, prefix, iri):
        """\
        Registeres the `iri` under the provided `prefix`.

        `iri`
            An absolute IRI (already resolved against self.base)
        """
        existing = self._prefixes.get(prefix)
        if existing:
            if existing != iri:
                raise mio.MIOException('The prefix "%s" is already asigned to "%s"' % (prefix, existing))
            return
        self._prefixes[prefix] = iri

    def topic_identity(self, name=None):
        """\
        Returns an item identifier for a wildcard. 
        
        If the `name` is ``None``, a new item identifier will be created. If
        the `name` is not ``None`` an existing item identifier is returned iff
        the `name` is already known by the system. 
        """
        identity = self._wc2identity.get(name)
        if not identity:
            identity = self.next_topic_identity(name)
            if name:
                self._wc2identity[name] = identity
        return identity

    def next_topic_identity(self, name=None):
        """\
        Returns an item identifier for a wildcard without checking if the 
        wildcard is already known.
        """
        self.wildcard_counter+=1
        ident = '$__%d' % self.wildcard_counter
        if name:
            ident = '.'.join([ident, name])
        iri = None
        if self.included_by:
            iri = irilib.resolve_iri(self.included_by[0], '#' + ident)
        else:
            iri = self.resolve_ident(ident)
        return consts.IID, iri
    
    def register_template(self, name, template):
        """\
        Registeres the provided `template` under the specified `name`.
        
        Raises an exception if a template with the same name and number of 
        arguments is already registered.
        """
        key = name, len(template.args)
        existing = self.templates.get(key)
        if existing:
            raise mio.MIOException('The template "%s/%d" is already registered' % (name, len(template.args)))
        self.templates[key] = template
    
    def get_template(self, name, args):
        """\
        Returns a registered template with the provided `name` and parameters.
        
        Raises an exception if the template is not registered.
        """
        key = name, len(args)
        template = self.templates.get(key)
        if not template:
            raise mio.MIOException('Undefined template "%s/%d"' % (name, len(args)))
        return template
    
    def resolve_iri(self, iri):
        """\
        Resolves the `iri` against the document IRI.
        """
        return irilib.resolve_iri(self.base, iri)

    def resolve_ident(self, ident):
        """\
        Converts the `ident` into a fragment identifier and resolves it against
        the document IRI.
        """
        return self.resolve_iri('#' + ident)

    def resolve_qname(self, qname):
        """\
        Returns an absolute IRI from the QName.
        
        `qname`
            A ``(prefix, local)`` tuple.
        """
        prefix, name = qname
        iri = self._prefixes.get(prefix)
        if not iri:
            raise mio.MIOException('Unknown prefix "%s"' % prefix)
        return self.resolve_iri(iri + name)

    def include(self, iri):
        """\
        Includes another CTM source into this CTM instance.
        
        `iri`
            An absolute IRI.
        """
        if iri in self.included_by:
            return
        included_by = self.included_by[:]
        included_by.append(self.base)
        self._merge_ctm(iri, included_by)

    def merge(self, iri, syntax_iri):
        """\
        Merges another topic map source into this instance.
        
        `iri`
            An absolute IRI.
        `syntax_iri`
            The PSI of the Topic Maps syntax. 
        """
        if iri in self._context.loaded:
            return
        self._context.add_loaded(iri)
        syntax = _IRI2SYNTAX.get(syntax_iri)
        if syntax == 'ctm':
            self._merge_ctm(iri)
        else:
            deser = mio.create_deserializer(syntax)
            if not deser:
                raise mio.MIOException('Unsupported syntax: "%s"' % syntax_iri)
            deser.subordinate = True
            deser.context = self._context
            deser.handler = self._maphandler
            deser.parse(mio.Source(iri))

    def _merge_ctm(self, iri, included=None):
        """\
        Merges / includes another CTM source into this instance.
        
        `iri`
            The absolute IRI of the CTM source.
        `included`
            Either ``None`` or a list of document IRIs from which the CTM 
            source is included by.
        """
        from mio.ctm import CTMDeserializer
        deser = CTMDeserializer(context=self._context, included_by=included)
        deser.handler = self._maphandler
        deser.subordinate = True
        if included:
            deser.wildcard_counter = self.wildcard_counter
        deser.parse(Source(iri))
        if included:
            self.wildcard_counter = deser.wildcard_counter
            for template in deser.environment.templates.itervalues():
                self.register_template(template.name, template)

    def new_context(self, bindings):
        """\
        Returns a new template context with the provided variable bindings.
        
        The template context *is not* pushed onto the stack of template 
        contexts.
        """
        return TemplateContext(self, self._tpl_context, bindings)

    def push_context(self, ctx):
        """\
        Pushes the provided template context onto the stack.
        """
        self._tpl_context = ctx

    def pop_context(self):
        """\
        Removes the provided template context from the stack.
        """
        ctx, self._tpl_context = self._tpl_context, self._tpl_context.parent
        ctx.parent = None
    
    #pylint: disable-msg=W0212
    maphandler = property(lambda self: self._maphandler)
    subordinate = property(lambda self: self._subordinate)


class TemplateContext(object):
    """\
    Template context which keeps track of variable bindings.
    """
    __slots__ = ['_env', 'parent', '_focus', '_bindings']
    
    def __init__(self, env, parent=None, bindings=None):
        """\
        
        `env`
            An ``Environment`` instance.
        `parent`
            A template context or ``None``.
        `bindings`
            Variable bindings.
        """
        self._env = env
        self.parent = parent
        self._focus = []
        self._bindings = bindings or {}
        if parent:
            self._focus = parent._focus[:]

    def push_focus(self, identity):
        """\
        Sets the provided `identity` into the focus.
        """
        self._focus.append(identity)

    def pop_focus(self):
        """\
        Removes the current focus from the stack.
        """
        self._focus.pop()

    def _get_focus(self):
        if not self._focus:
            raise Exception('Internal error: No topic in focus')
        return self._focus[-1]

    def call_template(self, name, args):
        """\
        Invokes the template with the provided `name` and arguments.
        """
        tpl_invocation = tpl.TemplateInvocation(name, args)
        tpl_invocation(self._env)

    def _make_topic_identity(self, ref):
        """\
        Returns either an existing item identifier for a wildcard or creates
        a new item identifier for a wildcard.
        """
        key = ref
        identity = self._bindings.get(key)
        if not identity:
            identity = self._env.next_topic_identity(ref[0] == consts.NAMED_WILDCARD and ref[1] or None)
            self._bindings[key] = identity 
        return identity

    def get_topic_reference(self, ref):
        """\
        Returns the topic identity for the provided reference `ref`.
        
        `ref`
            A tuple (kind, identity)
        """
        kind, identity = ref
        if kind == consts.IN_FOCUS:
            return self.focus
        if kind == consts.VSLO:
            kind, identity = self._get_reference_by_variable((consts.VARIABLE, ref[1]))
            kind = consts.SLO
        elif kind == consts.VIID:
            kind, identity = self._get_reference_by_variable((consts.VARIABLE, ref[1]))
            kind = consts.IID
        if kind == consts.VARIABLE:
            kind, identity = self._get_reference_by_variable(ref)
        if kind in (consts.WILDCARD, consts.NAMED_WILDCARD):
            try:
                kind, identity = self._bindings.get((kind, identity))
            except TypeError:
                kind, identity = self._make_topic_identity((kind, identity))
        if kind in (consts.IID, consts.IRI, consts.SLO):
            return kind, identity
        raise mio.MIOException('Error: Unknown topic reference "(%s, %s)"' % (kind, identity))

    def _get_reference_by_variable(self, var):
        """\
        Returns a reference for the provided variable ``var``.
        """
        if not var[0] == consts.VARIABLE:
            raise Exception('Internal error: Expected a variable, got: "%r"' % var)
        res = self._bindings.get(var, var)
        if res == consts.TOPIC_IN_FOCUS:
            res = self.focus
        while res[0] == consts.VARIABLE and self.parent:
            res = self.parent._get_reference_by_variable(res) #pylint: disable-msg=W0212
            if res == consts.TOPIC_IN_FOCUS:
                res = self.focus
        return res

    def get_literal(self, ref):
        kind, val = ref
        if kind == consts.VARIABLE:
            kind, val = self._get_reference_by_variable(ref)
        return kind, val

    def _get_ref(self, var):
        res = self._bindings.get(var)
        if not res and self.parent:
            res = self.parent._get_ref(var)
        if not res:
            raise Exception('Unknown variable "$%s"' % var[1])
        return res

    handler = property(lambda self: self._env.maphandler)
    focus = property(_get_focus)
