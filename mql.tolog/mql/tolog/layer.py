# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm import ANY, mql
from itertools import chain

#TODO: This shouldn't belong to the mql.tolog package but to the generic mql package
class TopicMapLayer(object):
    """\

    """
    def get_topic_by_subject_identifier(self, sid):
        """\
        Returns a topic by its subject identifier or ``None`` if no topic
        could be found.

        `sid`
            An IRI.
        """

    def get_topic_by_subject_locator(self, slo):
        """\
        Returns a topic by its subject locator or ``None`` if no topic
        could be found.

        `slo`
            An IRI.
        """

    def get_topic_by_item_identifier(self, iid):
        """\
        Returns a topic by its item identifier or ``None`` if no topic
        could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_topic(obj) else None

    def get_object_by_item_identifier(self, iid):
        """\

        """

    def get_topicmap_by_item_identifier(self, iid):
        """\
        Returns a topic map by its item identifier or ``None`` if no
        topic map could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_topicmap(obj) else None

    def get_association_by_item_identifier(self, iid):
        """\
        Returns an association by its item identifier or ``None`` if no
        association could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_association(obj) else None

    def get_role_by_item_identifier(self, iid):
        """\
        Returns an association role by its item identifier or ``None`` if no
        association role could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_role(obj) else None

    def get_occurrence_by_item_identifier(self, iid):
        """\
        Returns an occurrence by its item identifier or ``None`` if no
        occurrence could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_occurrence(obj) else None

    def get_name_by_item_identifier(self, iid):
        """\
        Returns a name by its item identifier or ``None`` if no
        name could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_name(obj) else None

    def get_variant_by_item_identifier(self, iid):
        """\
        Returns a variant by its item identifier or ``None`` if no
        variant could be found.

        `iid`
            An IRI.
        """
        obj = self.get_object_by_item_identifier(iid)
        return obj if self.is_variant(obj) else None

    def get_parent(self, tmc):
        """\
        Returns the parent of the provided Topic Maps construct.
        """

    def get_children(self, tmc, types=ANY):
        """\
        Returns the children of the provided Topic Maps construct
        """
        if self.is_topic(tmc):
            return self.get_topic_children(tmc, types=types)
        elif self.is_association(tmc):
            return self.get_roles(tmc, types=types)
        elif self.is_name(tmc):
            return self.get_variants(tmc)
        elif self.is_topicmap(tmc):
            return chain(self.get_topics(types=types), self.get_associations(types=types))
        raise mql.InvalidQueryError()  #TODO: Msg.

    def get_topicmap(self):
        """\
        Returns the underlying topic map, never ``None``.
        """

    def get_topics(self, types=ANY):
        """\
        Returns an iterable of topics.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_associations(self, types=ANY, scope=ANY):
        """\
        Returns an iterable of associations.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        `scope`
            An iterable of topics or ``ANY`` if the scope is unconstrained.
        """

    def get_occurrences(self, topic, types=ANY, scope=ANY):
        """\
        Returns an iterable of occurrences of the provided topic.

        `topic`
            The context topic.
        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        `scope`
            An iterable of topics or ``ANY`` if the scope is unconstrained.
        """

    def get_names(self, topic, types=ANY, scope=ANY):
        """\
        Returns an iterable of names of the provided topic.

        `topic`
            The context topic.
        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        `scope`
            An iterable of topics or ``ANY`` if the scope is unconstrained.
        """

    def get_variants(self, name, scope=ANY):
        """\

        `scope`
            An iterable of topics or ``ANY`` if the scope is unconstrained.
        """

    def get_topic_children(self, topic, types=ANY, scope=ANY):
        """\
        Returns an iterable of occurrences and names of the provided topic.

        `topic`
            The context topic.
        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        `scope`
            An iterable of topics or ``ANY`` if the scope is unconstrained.
        """
        return chain(self.get_occurrences(topic, types, scope), self.get_names(topic, types, scope))

    def get_roles_played(self, topic, types=ANY):
        """\
        Returns an iterable of roles which the `topic` plays.

        `topic`
            The context topic.
        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_subject_identifiers(self, topic):
        """\
        Returns an iterable of subject identifiers of the `topic`.

        `topic`
            The context topic.
        """

    def get_subject_locators(self, topic):
        """\
        Returns an iterable of subject locators of the `topic`.

        `topic`
            The context topic.
        """

    def get_item_identifiers(self, tmc):
        """\
        Returns an iterable of item identifiers of `tmc`.

        `tmc`
            The context Topic Maps construct.
        """

    def get_roles(self, assoc, types=ANY):
        """\
        Returns an iterable of roles from the provided association.

        `assoc`
            The context association.
        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_reifier(self, reified):
        """\
        Returns the reifier of `reified` or ``None``.
        """

    def get_reified(self, reifier):
        """\
        Returns the reified Topic Maps construct of `reifier` or ``None``.
        """

    def get_names_by_value(self, value):
        """\
        Return an iterable of names which have the provided value.
        """
    
    def get_occurrences_by_value(self, value, datatype):
        """\
        Returns an iterable of occurrences which have the provided value/datatype.
        """
        
    def get_variants_by_value(self, value, datatype):
        """\
        Returns an iterable of variants which have the provided value/datatype.
        """

    def get_topic_direct_types(self):
        """\
        Returns an iterable of topic which play the ``type`` role within 
        a type-instance association.
        """

    def get_topic_types(self):
        """\
        Returns an iterable of topics which play the ``type`` role within
        a type-instance association and their supertypes.
        """

    def get_association_types(self):
        """\
        Returns an iterable of association types.
        """

    def get_role_types(self):
        """\
        Returns an iterable of role types.
        """

    def get_occurrence_types(self):
        """\
        Returns an iterable of occurrence types.
        """

    def get_name_types(self):
        """\
        Returns an iterable of name types.
        """

    def is_parent_of(self, parent, child):
        """\
        Returns if `parent` is the parent of `child`.
        """
        return self.get_parent(child) == parent

    def is_instance_of(self, instance, type, scope=ANY):
        """\
        Returns if `instance` is an instance of `type`.
        """

    def is_topicmap(self, obj):
        """\
        Indicates if the provided object is a topic map.
        """

    def is_topic(self, obj):
        """\
        Indicates if the provided object is a topic.
        """

    def is_association(self, obj):
        """\
        Indicates if the provided object is an association.
        """

    def is_role(self, obj):
        """"\
        Indicates if the provided object is a role.
        """

    def is_occurrence(self, obj):
        """\
        Indicates if the provided object is an occurrences.
        """

    def is_name(self, obj):
        """\
        Indicates if the provided object is a name.
        """

    def is_variant(self, obj):
        """\
        Indicates if the provided object is a variant.
        """


class AdvancedTopicMapLayer(TopicMapLayer):
    """\
    
    """
    def __init__(self, layer):
        self._layer = layer

    def get_topic_by_subject_identifier(self, sid):
        return self._layer.get_topic_by_subject_identifier(sid)

    def get_topic_by_subject_locator(self, slo):
        return self._layer.get_topic_by_subject_locator(slo)

    def get_topic_by_item_identifier(self, iid):
        return self._layer.get_topic_by_item_identifier(iid)

    def _topic(self, tmc, force=False):
        topic = tmc if self._layer.is_topic(tmc) else self.get_reifier(tmc)
        if force and topic is None:
            raise mql.InvalidQueryError()  #TODO: Msg.
        return topic
        
    def get_occurrences(self, tmc, types=ANY, scope=ANY):
        topic = self._topic(tmc)
        return () if not topic else self._layer.get_occurrences(topic, types, scope)
    
    def get_names(self, tmc, types=ANY, scope=ANY):
        topic = self._topic(tmc)
        return () if not topic else self._layer.get_names(topic, types, scope)

    def get_roles_played(self, tmc, types=ANY):
        topic = self._topic(tmc)
        return () if not topic else self._layer.get_roles_played(topic, types)

    def get_subject_identifiers(self, tmc):
        topic = self._topic(tmc)
        return () if not topic else self._layer.get_subject_identifiers(topic)

    def get_subject_locators(self, tmc):
        topic = self._topic(tmc)
        return () if not topic else self._layer.get_subject_locators(topic)

    def get_object_by_item_identifier(self, iid):
        return self._layer.get_object_by_item_identifier(iid)

    def get_names_by_value(self, value):
        return self._layer.get_names_by_value(value)

    def get_occurrences_by_value(self, value, datatype):
        return self._layer.get_occurrences_by_value(value, datatype)

    def get_variants_by_value(self, value, datatype):
        return self._layer.get_variants_by_value(value, datatype)

    def get_topic_direct_types(self):
        return self._layer.get_topic_direct_types()

    def get_topic_types(self):
        return self._layer.get_topic_types()

    def get_association_types(self):
        return self._layer.get_association_types()

    def get_role_types(self):
        return self._layer.get_role_types()

    def get_occurrence_types(self):
        return self._layer.get_occurrence_types()

    def get_name_types(self):
        return self._layer.get_name_types()

    def is_parent_of(self, parent, child):
        res = self._layer.is_parent_of(parent, child)
        if not res and self.is_topic(child):
            reified = self._layer.get_reified(child)
            res = self._layer.is_parent_of(parent, reified) if reified else False
        return res

    def is_instance_of(self, instance, type, scope=ANY):
        return self._layer.is_instance_of(instance, type, scope)

    def _is(self, obj, is_expected_type):
        res = is_expected_type(obj)
        if not res and self.is_topic(obj):
            reified = self._layer.get_reified(obj)
            res = is_expected_type(reified) if reified is not None else None
        return res

    def is_topicmap(self, obj):
        return self._is(obj, self._layer.is_topicmap)

    def is_association(self, obj):
        return self._is(obj, self._layer.is_association)

    def is_role(self, obj):
        return self._is(obj, self._layer.is_role)

    def is_occurrence(self, obj):
        return self._is(obj, self._layer.is_occurrence)

    def is_name(self, obj):
        return self._is(obj, self._layer.is_name)

    def is_variant(self, obj):
        return self._is(obj, self._layer.is_variant)
