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
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
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


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm import ANY, UCS
from itertools import chain

class TopicMapLayer(object):
    """\

    """
    def get_baseuri(self):
        """\
        Returns the base locator
        """

    def resolve_iri(self, iri):
        """\

        """
        
    def get_topic_by_subject_identifier(self, sid):
        """\

        """

    def get_topic_by_subject_locator(self, slo):
        """\

        """

    def get_topic_by_item_identifier(self, iid):
        """\

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

    def get_associations(self, types=ANY, scope=UCS):
        """\
        Returns an iterable of associations.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_occurrences(self, topic, types=ANY, scope=UCS):
        """\
        Returns an iterable of occurrences of the provided topic.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_names(self, topic, types=ANY, scope=UCS):
        """\
        Returns an iterable of names of the provided topic.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
        """

    def get_topic_children(self, topic, types=ANY, scope=UCS):
        """\
        Returns an iterable of occurrences and names of the provided topic.

        `types`
            An iterable of topics or ``ANY`` if the type is unconstrained.
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

    def get_topic_types(self):
        """\
        Returns an iterable of topics which play the type role within
        a type-instance association.
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

    def is_instance_of(self, instance, type, scope=UCS):
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
