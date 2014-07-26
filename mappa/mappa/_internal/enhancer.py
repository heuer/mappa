# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides several ``enhance`` functions to add missing functionality to 
classes, mostly 'magic methods' or methods to filter constructs.

The classes are only enhanced iff the functionality is missing, otherwise these
utility functions assume that the backend implements the stuff natively.

These enhancers are used to avoid unncessary subclassing.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import ifilter, imap
from mappa import TMDM, UCS, ANY
from mappa.utils import is_binary, is_construct, is_scoped, is_topicmap, \
    is_topic, is_association, is_role, is_occurrence, is_name, is_variant
from mappa.predicates import parent, player
from mappa._internal.implhelper import topic_types, topic_instances, \
    topic_supertypes, create_topic_by_identity, \
    topic_by_identity, construct_by_identity, get_topic
from mappa._internal.itemexpr import filter_topic_children, add_topic_child, \
    filter_players, add_role
from mappa._internal.filter import filter_by_type_scope, filter_roles
from mappa._internal import mergeutils, siggen, atomification


def enhance(cls):
    """\
    Adds some methods to the specified class, if necessary.
    The class must provide a ``_kind`` attribute.
    """
    if not is_construct(cls):
        raise ValueError('Cannot enhance %s, seems to be no Topic Maps construct class' % cls.__name__)
    else:
        enhance_construct(cls)
    if is_topicmap(cls):
        enhance_topicmap(cls)
    elif is_topic(cls):
        enhance_topic(cls)
    elif is_association(cls):
        enhance_association(cls)
    elif is_role(cls):
        enhance_role(cls)
    elif is_occurrence(cls):
        enhance_occurrence(cls)
    elif is_name(cls):
        enhance_name(cls)
    elif is_variant(cls):
        enhance_variant(cls)


def enhance_connection(cls):
    def _post_process_loading(tm, format, version, deser):
        if format != 'xtm':
            return
        if version == '1.0' or deser.version == '1.0':
            from mappa.xtm1utils import convert_to_tmdm
            convert_to_tmdm(tm)
    if not hasattr(cls, '__getitem__'):
        def _get_tm(self, key):
            tm = self.get(key)
            if not tm:
                raise KeyError(key)
            return tm
        cls.__getitem__ = _get_tm
    if not hasattr(cls, '__delitem__'):
        cls.__delitem__ = lambda self, key: self.remove(key)
    if not hasattr(cls, '__contains__'):
        cls.__contains__ = lambda self, iri: iri in self.iris
    if not hasattr(cls, 'load'):
        import tm
        from tm import mio
        from mappa.miohandler import MappaMapHandler
        def _load(conn, source, into, base=None, format=None, **kw):
            extension = None
            src = None
            if hasattr(source, 'read'):
                src = tm.Source(file=source, iri=base)
            else:
                src = tm.Source(iri=source)
                dot = source.rfind('.')
                if dot != -1:
                    extension = source[dot+1:]
            deser = mio.create_deserializer(format=format, extension=extension, **kw)
            if not deser:
                raise IOError('No deserializer found for "%s"' % format)
            tmap = conn.get(into) or conn.create(into)
            deser.handler = MappaMapHandler(tmap)
            deser.parse(src)
            _post_process_loading(tmap, format, kw.get('version'), deser)
        cls.load = _load
    if not hasattr(cls, 'loads'):
        import tm
        from tm import mio
        from mappa.miohandler import MappaMapHandler
        def _loads(conn, source, into, base=None, format='ctm', **kw):
            src = tm.Source(data=source, iri=base or into)
            deser = mio.create_deserializer(format, **kw)
            if not deser:
                raise IOError('No deserializer found for "%s"' % format)
            tmap = conn.get(into) or conn.create(into)
            deser.handler = MappaMapHandler(tmap)
            deser.parse(src)
            _post_process_loading(tmap, format, kw.get('version'), deser)
        cls.loads = _loads
    if not hasattr(cls, 'write'):
        def _write(conn, iri, out, base=None, format='xtm', encoding=None, version=None, **kw):
            tm = conn.get(iri)
            if not tm:
                raise IOError('No topic map at "%s" available' % iri)
            import pkg_resources
            writer = None
            for ep in pkg_resources.iter_entry_points('mappa.writer'):
                if ep.name == format:
                    writer = ep.load().create_writer(out, base=base or iri, version=version, **kw)
                    break
            if not writer:
                raise IOError('No writer found for "%s"' % format)
            writer.write(tm)
        cls.write = _write


def enhance_construct(cls):
    """\
    
    """
    def _not_implemented(*args, **kw):
        raise NotImplementedError()
    if not hasattr(cls, 'find'):
        cls.find = _not_implemented
    if not hasattr(cls, 'findall'):
        cls.findall = _not_implemented


def enhance_topicmap(cls):
    if not hasattr(cls, 'create_topic'):
        cls.create_topic = create_topic_by_identity
    if not hasattr(cls, 'topic'):
        cls.topic = topic_by_identity
    if not hasattr(cls, 'construct'):
        cls.construct = construct_by_identity
    if not hasattr(cls, 'merge'):
        def _merge(tm, other):
            mergeutils. merge_topicmaps(other, tm)
        cls.merge = _merge


def enhance_topic(cls):
    def add_type(topic, tt):
        if tt in topic.types:
            return
        tm = topic.tm
        type_instance, typ, instance = map(tm.create_topic_by_sid, (TMDM.type_instance, TMDM.type, TMDM.instance))
        assoc = tm.create_association(type_instance)
        assoc.create_role(typ, tt)
        assoc.create_role(instance, topic)
    def remove_type(topic, tt):
        tm = topic.tm
        tmdm_type = tm.topic(sid=TMDM.type)
        for assoc in ifilter(is_binary, imap(parent, topic.roles_by(type=tm.topic(sid=TMDM.instance), assoc_type=tm.topic(sid=TMDM.type_instance), scope=UCS))):
            if tt in assoc.players_by(type=tmdm_type):
                assoc.remove()
                break
    def add_supertype(topic, st):
        tm = topic.tm
        supertype_subtype, supertype, subtype = map(tm.create_topic_by_sid, (TMDM.supertype_subtype, TMDM.supertype, TMDM.subtype))
        assoc = tm.create_association(supertype_subtype)
        assoc.create_role(supertype, st)
        assoc.create_role(subtype, topic)
    def remove_supertype(topic, st):
        tm = topic.tm
        supertype = tm.topic(sid=TMDM.supertype)
        for assoc in ifilter(is_binary, imap(parent, topic.roles_by(type=tm.topic(sid=TMDM.subtype), assoc_type=tm.topic(sid=TMDM.supertype_subtype), scope=UCS))):
            if st in assoc.players_by(type=supertype):
                assoc.remove()
                break
    if not hasattr(cls, 'types'): 
        cls.types = property(topic_types)
    if not hasattr(cls, 'instances'):
        cls.instances = property(topic_instances)
    if not hasattr(cls, 'add_type'):
        cls.add_type = add_type
    if not hasattr(cls, 'remove_type'):
        cls.remove_type = remove_type
    if not hasattr(cls, 'supertypes'):
        cls.supertypes = property(topic_supertypes)
    if not hasattr(cls, 'add_supertype'):
        cls.add_supertype = add_supertype
    if not hasattr(cls, 'remove_supertype'):
        cls.remove_supertype = remove_supertype
    if not hasattr(cls, '__atomify__'):
        def _atomify(topic, ctx=ANY):
            return atomification.atomify_topic(topic, ctx)
        cls.__atomify__ = _atomify
    if not hasattr(cls, '__getitem__'):
        cls.__getitem__ = filter_topic_children
    if not hasattr(cls, '__setitem__'):
        def _add_child(topic, expr, value):
            add_topic_child(topic, value, expr)
        cls.__setitem__ = _add_child
    if not hasattr(cls, '__div__'):
        def _filter_children(topic, expr):
            return filter_topic_children(topic, expr, all_children=True)
        cls.__div__ = _filter_children
    if not hasattr(cls, 'occurrences_by'):
        def _occurrences_by(topic, type, scope=ANY, exact=True):
            return filter_by_type_scope(type, scope, exact, topic.occurrences)
        cls.occurrences_by = _occurrences_by
    if not hasattr(cls, 'names_by'):
        def _names_by(topic, type, scope=ANY, exact=True):
            return filter_by_type_scope(type, scope, exact, topic.names)
        cls.names_by = _names_by
    if not hasattr(cls, 'roles_by'):
        def _roles_by(topic, type, assoc_type=ANY, scope=ANY, exact=True):
            return filter_roles(type, assoc_type, scope, exact, topic.roles_played)
        cls.roles_by = _roles_by
    if not hasattr(cls, 'played_types'):
        def _played_types(topic):
            return [role.type for role in topic.roles_played]
        cls.played_types = property(_played_types)
    if not hasattr(cls, 'merge'):
        def _merge(topic, other):
            mergeutils.merge_topics(other, topic)
        cls.merge = _merge
    if not hasattr(cls, '__iter__'):
        # Necessary, otherwise Python utilizes __getitem__ which results in errors
        def _iter(topic):
            raise TypeError('Topics are not iterable')
        cls.__iter__ = _iter


def enhance_association(cls):
    def _add_role(assoc, expr, player):
        add_role(assoc, player, expr)
    if not hasattr(cls, '__len__'):
        cls.__len__ = lambda self: len(self.roles)
    if not hasattr(cls, '__nonzero__'):
        cls.__nonzero__ = lambda self: True
    if not hasattr(cls, '__bool__'):
        cls.__bool__ = lambda self: True
    if not hasattr(cls, '__iter__'):
        cls.__iter__ = lambda self: iter(self.roles)
    if not hasattr(cls, '__contains__'):
        cls.__contains__ = lambda self, role: role in self.roles
    if not hasattr(cls, '__getitem__'):
        cls.__getitem__ =  filter_players
    if not hasattr(cls, '__setitem__'):
        cls.__setitem__ = _add_role
    if not hasattr(cls, '__sig__'):
        cls.__sig__ = siggen.association_signature
    if not hasattr(cls, 'players_by'):
        def _filter_players(assoc, type):
            return imap(player, assoc.roles_by(type))
        cls.players_by = _filter_players
    if not hasattr(cls, 'roles_by'):
        def _filter_roles(assoc, type):
            from mappa.utils import has_type
            return [role for role in assoc.roles if has_type(role, type)]
        cls.roles_by = _filter_roles


def enhance_role(cls):
    if not hasattr(cls, '__sig__'):
        cls.__sig__ = siggen.role_signature
    if not hasattr(cls, '__iter__'):
        def _iter(role):
            yield role.type
            yield role.player
        cls.__iter__ = _iter


def enhance_occurrence(cls):
    if not hasattr(cls, '__sig__'):
        cls.__sig__ = siggen.occurrence_signature
    if not hasattr(cls, '__atomify__'):
        cls.__atomify__ = atomification.atomify_dataobject


def enhance_name(cls):
    if not hasattr(cls, '__iter__'):
        cls.__iter__ = lambda self: iter(self.variants)
    if not hasattr(cls, '__sig__'):
        cls.__sig__ = siggen.name_signature
    if not hasattr(cls, '__atomify__'):
        cls.__atomify__ = atomification.atomify_name


def enhance_variant(cls):
    if not hasattr(cls, '__sig__'):
        cls.__sig__ = siggen.variant_signature
    if not hasattr(cls, '__atomify__'):
        cls.__atomify__ = atomification.atomify_dataobject
