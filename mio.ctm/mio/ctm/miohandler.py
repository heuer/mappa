# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
An (experimental) ``tm.mio.handler.MapHandler`` implementation that
translates events into Compact Topic Maps (CTM) syntax.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import codecs
from collections import defaultdict
import logging
from tm import XSD
from tm.mio import SUBJECT_IDENTIFIER, SUBJECT_LOCATOR, ITEM_IDENTIFIER, MIOException
import tm.mio.handler as mio_handler
from .utils import is_valid_id, is_valid_local_part, is_valid_iri, is_native_datatype

__all__ = ['CTMHandler']

from tm import TMDM
_DEFAULT_NAME_TYPE = SUBJECT_IDENTIFIER, TMDM.topic_name
del TMDM

_NL = u'\n'
_END_OF_STATEMENT = u';\n'


class CTMHandler(mio_handler.HamsterMapHandler):
    """\
    
    """
    def __init__(self, fileobj, encoding='utf-8'):
        """\

        `fileobj`
            A file-like object which has a ``write`` method.
        """
        self._out = codecs.getwriter(encoding)(fileobj)
        self._prefixes = {}
        self._indent = u' ' * 4
        self._something_written = False
        self._header_written = False
        self._last_topic = None
        self._encoding = encoding.lower()
        self._association_templates = {}
        self.detect_prefixes = False
        self._pending_prefix_iris = []
        self._prefix_counter = 0
        self._prefix_iri_candidates = defaultdict(int)
        self._min_prefix = 10
        # Optional properties
        self.title = None
        self.author = None
        self.creation_date = None
        self.modification_date = None
        self.license = None
        self.comment = None

    def _get_indentation(self):
        return len(self._indent)

    def _set_indentation(self, val):
        self._indent = u' ' * val

    indentation = property(_get_indentation, _set_indentation, doc='Sets the indentation level')
    prefixes = property(lambda self: dict(self._prefixes), doc='Returns the registered prefixes (a dict)')

    def add_prefix(self, prefix, iri):
        """\
        Assigns the ``prefix`` to the IRI. If the handler has already serialized
        the prefixes, it's not possible to override an existing prefix.

        `prefix`
            The prefix (a valid CTM identifier)
        `iri`
            The IRI (a valid CTM IRI)
        """
        if not prefix or not iri:
            raise ValueError('Neither the prefix nor the IRI must be None, got: "%s" "%s"' % (prefix, iri))
        if not is_valid_id(prefix):
            raise ValueError('The prefix "%s" is not a valid CTM identifier' % prefix)
        if not is_valid_iri(iri):
            raise ValueError('The IRI "%s" is not a valid CTM IRI' % iri)
        if self._last_topic:
            raise MIOException('Cannot add prefix "%s" <%s>. Issue an "endTopic" event first' % (prefix, iri))
        existing = self._prefixes.get(prefix)
        if self._header_written and existing and existing != iri:
            raise MIOException('The prefix "%s" is already bound to <%s>' % (prefix, existing))
        if existing != iri:
            self._prefixes[prefix] = iri
            if self._header_written:
                self._write_prefix(prefix, iri)

    def remove_prefix(self, prefix):
        """\
        Removes the registered `prefix`. It's not possible to remove a
        prefix if the handler has already serialized a prefix/IRI binding.

        `prefix`
            The prefix to remove.
        """
        if self._header_written:
            raise MIOException('The prefix "%s" has been serialized already' % prefix)
        self._prefixes.pop(prefix, None)

    def add_association_template(self, name, type, focus, *roles):
        roles_ = [focus]
        roles_.extend(roles)
        tpl = _AssociationTemplate(name, type, roles_)
        self._association_templates[(type, focus, tpl.arity)] = tpl

    #
    # MIO handler methods
    #
    def startTopicMap(self):
        super(CTMHandler, self).startTopicMap()
        self._write_header()

    def endTopicMap(self):
        super(CTMHandler, self).endTopicMap()
        self._finish_pending_topic()
        self._out.write(u'\n')
        self._out.flush()

    def startTopic(self, identity):
        super(CTMHandler, self).startTopic(identity)
        self._start_topic(identity)

    #
    # Hamster handler methods:
    #
    def _create_topic_by_iid(self, iri):
        return ITEM_IDENTIFIER, iri

    def _create_topic_by_sid(self, iri):
        return SUBJECT_IDENTIFIER, iri

    def _create_topic_by_slo(self, iri):
        return SUBJECT_LOCATOR, iri

    def _handle_type_instance(self, instance, type):
        self._start_topic(instance)
        self._out.write(self._indent + u'isa ')
        self._write_topic_ref(type)
        self._out.write(_END_OF_STATEMENT)

    def _handle_item_identifier(self, topic, iri):
        self._write_topic_identity(topic, (ITEM_IDENTIFIER, iri))

    def _handle_subject_identifier(self, topic, iri):
        self._write_topic_identity(topic, (SUBJECT_IDENTIFIER, iri))

    def _handle_subject_locator(self, topic, iri):
        self._write_topic_identity(topic, (SUBJECT_LOCATOR, iri))

    def _handle_topicmap_item_identifier(self, iri):
        pass

    def _handle_topicmap_reifier(self, reifier):
        if reifier:
            if self._something_written:
                kind, iri = reifier
                if kind == ITEM_IDENTIFIER:
                    kind = u'item identifier'
                elif kind == SUBJECT_IDENTIFIER:
                    kind = u'subject identifier'
                elif kind == SUBJECT_LOCATOR:
                    kind = u'subject locator'
                msg = 'Ignoring the topic map reifier with the %s <%s>' % (kind, iri)
                logging.warn(msg)
            else:
                self._something_written = True
                self._out.write(u'~ ')
                self._write_topic_ref(reifier)
                self._out.write(_NL)

    def _create_association(self, type, scope, reifier, iids, roles):
        if self._handle_association_template(type, scope, reifier, roles):
            return
        self._something_written = True
        write_reifier = self._write_reifier
        write_topic_ref = self._write_topic_ref
        write = self._out.write
        self._finish_pending_topic()
        write(_NL)
        write_topic_ref(type)
        write(u'(')
        for i, role in enumerate(roles):
            if i > 0:
                write(u', ')
            if i > 3:
                write(_NL)
                write(self._indent * 2)
            write_topic_ref(role.type)
            write(u': ')
            write_topic_ref(role.player)
            write_reifier(role.reifier)
        write(u')')
        self._write_scope(scope)
        write_reifier(reifier)
        write(_NL)

    def _create_occurrence(self, parent, type, value, datatype, scope, reifier, iids):
        write = self._out.write
        self._start_topic(parent)
        write(self._indent)
        self._write_topic_ref(type)
        write(u': ')
        self._write_value_datatype(value, datatype)
        self._write_scope(scope)
        self._write_reifier(reifier)
        write(_END_OF_STATEMENT)

    def _create_name(self, parent, type, value, scope, reifier, iids, variants):
        write = self._out.write
        self._start_topic(parent)
        write(self._indent)
        write(u'- ')
        if _DEFAULT_NAME_TYPE != type:
            self._write_topic_ref(type)
            write(u': ')
        self._write_string(value)
        self._write_scope(scope)
        self._write_reifier(reifier)
        for variant in variants:
            write(_NL)
            write(self._indent * 2)
            write(u'(')
            self._write_value_datatype(variant.value, variant.datatype)
            self._write_scope(variant.scope)
            self._write_reifier(variant.reifier)
            write(u')')
        write(_END_OF_STATEMENT)

    #
    # Private methods
    #
    def _handle_association_template(self, type, scope, reifier, roles):
        """\

        """
        def is_role_reified(roles):
            for r in roles:
                if r.reifier:
                    return True
            return False
        def focus_role_type(roles):
            focus_identities = self._last_topic.identities
            for role in roles:
                if role.player in focus_identities:
                    return role.type
            return None
        if not self._last_topic or scope or reifier or is_role_reified(roles):
            return False
        focus_role_type = focus_role_type(roles)
        if not focus_role_type:
            return False
        tpl = self._association_templates.get((type, focus_role_type, len(roles)))
        if not tpl:
            return False
        tpl_roles = tpl.roles
        try:
            roles_ = sorted(roles, key=lambda r: tpl_roles.index(r.type))
        except ValueError:
            return False
        write, write_topic_ref = self._out.write, self._write_topic_ref
        write(self._indent)
        write(tpl.name)
        write(u'(')
        i = 0
        for role in roles_:
            if role.type == focus_role_type:
                continue
            if i > 0:
                write(u', ')
            write_topic_ref(role.player)
            i += 1
        write(u')')
        write(_END_OF_STATEMENT)
        return True
    
    def _start_topic(self, identity):
        if self._last_topic and identity in self._last_topic:
            return
        should_merge = self._last_topic and self._last_topic.should_merge_with(identity)
        if should_merge:
            self._last_topic.add_identity(identity)
            self._write_identity(identity)
        else:
            self._something_written = True
            self._finish_pending_topic()
            self._last_topic = _Topic(identity)
            self._out.write(_NL)
            self._write_topic_ref(identity)
            self._out.write(_NL)

    def _finish_pending_topic(self):
        if self._last_topic:
            self._out.write(u'.%s' % _NL)
            self._last_topic = None
        if self._pending_prefix_iris:
            self._out.write(_NL)
        while self._pending_prefix_iris:
            self._prefix_counter+=1
            prefix = u'ns%d' % self._prefix_counter
            while prefix in self._prefixes:
                self._prefix_counter+=1
                prefix = u'ns%d' % self._prefix_counter
            self.add_prefix(prefix, self._pending_prefix_iris.pop())

    def _write_header(self):
        """\

        """
        def tpl_comparator(a, b):
            res = cmp(a.name, b.name)
            return res if res != 0 else cmp(a.arity, b.arity)
        self._header_written = True
        write = self._out.write
        if self._encoding != u'utf-8':
            write(u'%%encoding "%s"%s' % (self._encoding, _NL))
        if self.title or self.author or self.creation_date \
                or self.modification_date or self.license or self.comment:
            write(u'#(%s' % _NL)
            if self.title:
                title = self.title
                sep = u'=' * len(title)
                write(sep)
                write(_NL)
                write(u'%s%s' % (title, _NL))
                write(sep)
                write(_NL)
            if self.author:
                write(u'Author:   %s%s' % (self.author, _NL))
            if self.creation_date:
                write(u'Created:  %s%s' % (self.creation_date, _NL))
            if self.modification_date:
                write(u'Modified: %s%s' % (self.modification_date, _NL))
            if self.license:
                write(u'License:  %s%s' % (self.license, _NL))
            if self.comment:
                write(u'%s%s%s' % (_NL, self.comment, _NL))
            write(u'%s)#%s' % (_NL, _NL))
        write(_NL)
        for prefix in sorted(self._prefixes.keys()):
            self._write_prefix(prefix, self._prefixes[prefix])
        if self._association_templates:
            write(u'%s#%s' % (_NL, _NL))
            write(u'# Templates')
            write(u'%s#%s%s' % (_NL, _NL, _NL))
        for tpl in sorted(self._association_templates.values(), tpl_comparator):
            self._write_assoc_tpl(tpl)

    def _write_assoc_tpl(self, tpl):
        """\

        """
        def variable_name(variables, iri):
            name = None
            idx = iri.rfind(u'/')
            if idx == -1:
                idx = iri.rfind(u'#')
            if idx > -1:
                name = iri[idx+1:]
                if not is_valid_id(name) or name in variables:
                    name = None
            if not name:
                name = len(variables)
            return u'$%s' % name
            
        write = self._out.write
        write_topic_ref = self._write_topic_ref
        write(u'def %s(' % tpl.name)
        variables = []
        for _, iri in tpl.roles:
            variables.append(variable_name(variables, iri))
        for i, name in enumerate(variables):
            if i:
                write(u', ')
            write(name)
        write(u')%s' % _NL)
        write(self._indent)
        write_topic_ref(tpl.type)
        write(u'(')
        i = 1
        want_comma = False
        for r in tpl.roles:
            if want_comma:
                write(u', ')
            write_topic_ref(r)
            if r != tpl.focus:
                write(u': %s' % variables[i])
                want_comma = True
            else:
                i -= 1
                write(u': %s' % variables[0])
                want_comma = True
            i += 1
        write(u')%s' % _NL)
        write(u'end%s%s' % (_NL, _NL))

    def _write_prefix(self, prefix, iri):
        self._out.write(u'%%prefix %s <%s>%s' % (prefix, iri, _NL))

    def _write_reifier(self, reifier):
        if reifier:
            self._out.write(u' ~ ')
            self._write_topic_ref(reifier)

    def _write_scope(self, scope):
        if scope:
            write, write_topic_ref = self._out.write, self._write_topic_ref
            write(u' @')
            for i, theme in enumerate(scope):
                if i:
                    write(u', ')
                write_topic_ref(theme)

    def _write_topic_identity(self, main_identity, identity):
        written = False
        if self._last_topic:
            if main_identity in self._last_topic:
                if identity in self._last_topic:
                    return
                self._write_identity(identity)
                self._last_topic.add_identity(identity)
                written = True
            elif identity in self._last_topic:
                self._write_identity(main_identity)
                self._last_topic.add_identity(main_identity)
                written = True
            elif self._last_topic.should_merge_with(main_identity) \
                     or self._last_topic.should_merge_with(identity):
                self._last_topic.add_identity(main_identity)
                self._last_topic.add_identity(identity)
                self._write_identity(main_identity)
                self._write_identity(identity)
                written = True
        if not written:
            self._start_topic(main_identity)
            self._write_identity(identity)
            self._last_topic.add_identity(identity)

    def _write_identity(self, identity):
        self._out.write(self._indent)
        self._write_topic_ref(identity)
        self._out.write(_END_OF_STATEMENT)

    def _write_topic_ref(self, topicref):
        kind, iri = topicref
        if kind == SUBJECT_LOCATOR:
            self._out.write(u'= ')
        elif kind == ITEM_IDENTIFIER:
            self._out.write(u'^ ')
        self._write_uri(iri)

    def _write_string(self, value):
        write = self._out.write
        if u'"' in value and value[-1] != u'"':
            write(u'"""')
            for c in value:
                if c == u'\\':
                    write(u'\\')
                write(c)
            write(u'"""')
        else:
            write(u'"')
            for c in value:
                if c in u'"\\':
                    write(u'\\')
                write(c)
            write(u'"')

    def _write_uri(self, uri):
        for prefix, iri in self._prefixes.iteritems():
            if uri.startswith(iri):
                lp = uri[len(iri):]
                if is_valid_local_part(lp):
                    self._out.write(u':'.join((prefix, lp)))
                    return
        self._out.write(u'<%s>' % uri)
        if self.detect_prefixes:
            idx = uri.rfind(u'#')
            if idx < 0:
                idx = uri.rfind(u'/')
            if idx < 0:
                return
            iri, lp = uri[:idx+1], uri[idx+1:]
            if iri in self._pending_prefix_iris or len(iri) < 5:
                return
            if iri in self._prefix_iri_candidates or is_valid_local_part(lp):
                self._prefix_iri_candidates[iri] += 1
                if self._prefix_iri_candidates[iri] >= self._min_prefix:
                    self._pending_prefix_iris.append(iri)
                    del self._prefix_iri_candidates[iri]

    def _write_value_datatype(self, value, datatype):
        if XSD.anyURI == datatype:
            self._write_uri(value)
        elif XSD.string == datatype:
            self._write_string(value)
        elif is_native_datatype(datatype):
            self._out.write(value)
        else:
            self._write_string(value)
            self._out.write(u'^^')
            self._write_uri(datatype)


class _Topic(object):
    """\
    Internal class to keep track about a topic and its identities.

    >>> sid = (SUBJECT_IDENTIFIER, 'http://psi.example.org/something')
    >>> t = _Topic(sid)
    >>> sid in t
    True
    >>> iid = ITEM_IDENTIFIER, 'http://www.example.org'
    >>> iid in t
    False
    >>> t.add_identity(iid)
    >>> iid in t
    True
    >>> iid2 = ITEM_IDENTIFIER, sid[1]
    >>> t.should_merge_with(iid2)
    True
    >>> t.should_merge_with(sid)
    True
    >>> t.should_merge_with(iid)
    True
    >>> slo = SUBJECT_LOCATOR, sid[1]
    >>> t.should_merge_with(slo)
    False
    >>> t.add_identity(slo)
    >>> t.should_merge_with(slo)
    True
    """
    def __init__(self, ref):
        self._refs = [ref]

    def add_identity(self, ref):
        self._refs.append(ref)

    def should_merge_with(self, ref):
        kind, iri = ref
        if kind == SUBJECT_LOCATOR:
            return ref in self._refs
        return (SUBJECT_IDENTIFIER, iri) in self._refs or (ITEM_IDENTIFIER, iri) in self._refs

    def __contains__(self, ref):
        return ref in self._refs

    @property
    def identities(self):
        return tuple(self._refs)


class _AssociationTemplate(object):
    """\
    
    """
    def __init__(self, name, type, roles):
        self.name = name
        self.type = type
        self.roles = roles

    @property
    def focus(self):
        return self.roles[0]

    @property
    def other_roles(self):
        return self.roles[1:]

    @property
    def arity(self):
        return len(self.roles)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
