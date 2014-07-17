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
from tm import ANY
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

    def get_parent(self, tmc):
        """\
        Returns the parent of the provided Topic Maps construct.
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
        else:
            topic = self._topic(tmc)
            if topic:
                return self.get_topic_children(topic, types=types)
            #TODO: Exception

    def _topic(self, tmc):
        return tmc if self.is_topic(tmc) else self.get_reifier(tmc)
        
    def get_occurrences(self, tmc, types=ANY, scope=ANY):
        topic = self._topic(tmc)
        return () if not topic else super(AdvancedTopicMapLayer, self).get_occurrences(topic, types, scope)
    
    def get_names(self, tmc, types=ANY, scope=ANY):
        topic = self._topic(tmc)
        return () if not topic else super(AdvancedTopicMapLayer, self).get_names(topic, types, scope)

    def get_roles_played(self, tmc, types=ANY):
        topic = self._topic(tmc)
        return () if not topic else super(AdvancedTopicMapLayer, self).get_roles_played(topic, types)

    def get_subject_identifiers(self, tmc):
        topic = self._topic(tmc)
        return () if not topic else super(AdvancedTopicMapLayer, self).get_subject_identifiers(topic)

    def get_subject_locators(self, tmc):
        topic = self._topic(tmc)
        return () if not topic else super(AdvancedTopicMapLayer, self).get_subject_locators(topic)
