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
#     * Neither the name 'Semagia' nor the name 'Mappa' nor the names of the
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
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
Interfaces for Mappa.

These interfaces exist for documentation purposes.

.. Note::

   Everywhere, where a collection should be returned, the concrete
   implementation MAY return an iterable (generator / iterator). Avoid 
   something like ``len(t.names)`` since it does not work with generators / 
   iterators.


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm.proto import Interface, Attribute
from mappa import UCS, ANY

# pylint: disable-msg=E0213, E0211, W0622

class IConnection(Interface):
    """\
    A connection provides access to a collection of `ITopicMap`s.
    
    Any connection may provide access to ``0 .. n`` topic maps. Each topic map
    is accessible through an IRI.
    
    This interface has no representation in the TMDM.
    
    To create a connection, use `mappa.connect(...)`::
    
        >>> import mappa
        >>> conn = mappa.connect()
        >>> tm = conn.create('http://www.semagia.com/some-map')
        >>> # ... create topics, assocs, etc.
        >>> conn.commit() # Note: Since we use the memory impl, changes will be lost
        >>> conn.close()
    """
    def create(iri):
        """\
        Creates a new topic map under the specified ``iri``.
        
        `iri`
            The IRI (address) where the topic map should be stored.
        
        This method raises a ``ValueError`` if a topic map under the specified
        IRI exists.
        """
    def remove(iri):
        """\
        Removes / deletes the topic map under the specified ``iri``.
        
        `iri`
            The IRI (address) where the topic map is stored.
        
        ::
            >>> conn.remove('http://www.semagia.com/some-map')
        """
    def __delitem__(iri):
        """\
        Removes / deletes the topic map under the specified ``iri``.
        
        This is an alias for `remove`.
        
        `iri`
            The IRI (address) where the topic map is stored.
        
        ::
            >>> del conn['http://www.semagia.com/some-map']
        """
    def __getitem__(iri):
        """\
        Returns a topic map which is stored at the specified ``iri``.
        
        `iri`
            The IRI (address) where the topic map is stored.
        
        This method raises a ``KeyError`` if no topic map under the specified
        IRI exists.
        """
    def __contains__(iri):
        """\
        Returns if a topic map under the provided IRI exists.
        """
    def get(iri):
        """\
        Returns the topic map which is stored at ``iri``.
        
        `iri`
            The IRI (address) where the topic map is stored.
        """
    def close(commit=False):
        """\
        Closes this connection.
        
        After a connection has been closed, it must not be used further.
        
        `commit`
            Indicates if uncommitted changes should be committed (by default,
            uncommitted changes will be lost).
        """
    def abort():
        """\
        Aborts all changes made through this connection.
        """
    def commit():
        """\
        Commits all changes made through this connection.
        """
    def load(source, into, base=None, format=None, **kw):
        """\
        Loads a topic map.
        
        A ``source`` may be a file-like object or a string which represents
        an absolute IRI. If the source IRI should not be used,
        specify the ``base`` IRI which will be used to resolve the IRIs
        of the source against.
        
        `source`
            The source to read the topic map from.
        `into`
            An IRI indicating the storage address of the topic map. If a topic
            map under the specified IRI exists, the content of the ``source``
            is added to the existing topic map. If no topic map under the
            specified IRI exists, a topic map is created.
        `base`
            The IRI that is used to resolve IRIs against.
        `format`
            The input format. By default ``XTM`` is used.
            The format is a case-insensitive string.
        `**kw`
            Additional configuration parameters. Unsupported parameters are
            ignored by the parser.
        
        ::
        
            >>> conn = mappa.connect()
            >>> f = open('/var/maps/my-map.xtm')
            >>> conn.load(f, into='http://www.semagia.com/my-map')
            >>> tm = conn.get('http://www.semagia.com/my-map')
            >>> f.close()
            >>> for topic in tm.topics:
            ...     do_something_with(topic)
        """
    def loads(string, into, base=None, format=None, **kw):
        """\
        Loads a topic map from the provided ``string``.
        
        See `load` for parameter details. It is recommended to specify at least
        the `format` (by default set to 'ctm').
        If a `base` is not provided, the `into` IRI will be used.
        
        `string`
            A string that contains a topic map (fragment).
        `format`
            The input format.
        
        ::
        
            >>> conn = mappa.connect()
            >>> tm = conn.create('http://www.semagia.com/my-map')
            >>> '= http://mappa.semagia.com/' in tm
            False
            >>> 'http://www.semagia.com/my-map#description' in tm
            False
            >>> conn.loads('''\
            = http://mappa.semagia.com/
            description: "This is the homepage of the Mappa Topic Maps engine :)".
            ''',
            into='http://www.semagia.com/my-map', format='ctm')
            >>> '= http://mappa.semagia.com' in tm
            True
            >>> 'http://www.semagia.com/my-map#description' in tm
            True
        """
    def write(iri, out, base=None, format='xtm', encoding=None, version=None, **kw):
        """\
        Writes the topic map specified by its IRI `iri`.
        
        `iri`
            The IRI (address) of the topic map to serialize.
        `out`
            A `file`-like object that has a ``write`` method.
        `base`
            An alternative IRI which is used to resolve references against.
            If the ``base`` is set to ``None`` (the default), the ``iri``
            will be used to resolve IRIs against.
        `format`
            The serialization format. By default ``XTM`` is used.
            The format is a case-insensitive string.
        `encoding`
            The encoding. If the encoding is set to ``None`` the default 
            encoding of the serialization format will be used (in most cases 
            ``utf-8``).
        `version`
            The version of the serialization format. If it set to ``None``, the
            latest available version will be used (i.e. for ``XTM`` the version
            ``2.0``).
        `**kw`
            Additional configuration parameters. Unsupported parameters are
            ignored by the serializer.
        """
    iris = Attribute("""\
    Returns the IRIs of the topic maps which are accessible through this
    connection.
    
    This attribute is read-only.
    """)
    closed = Attribute("""\
    Returns if this connection is closed.
    
    This attribute is read-only.
    """)

class IItem(Interface):
    """\
    The smallest entity in the Mappa world. 
    
    This interface has no meaning for the end user.
    """

class IConstruct(IItem):
    """\
    Base interface for all Topic Maps constructs used by Mappa.
    
    This interface has no representation in the TMDM.
    """
    def findone(expr, lang=None):
        """\
        Evaluates the specified expression and returns one result.

        `expr`
            An expression, commonly a path expression.
        `lang`
            Optional string identifying the language of the expression.
            If the language is not specified, the defailt language
            will be used.
        """
    def find(expr, lang=None):
        """\
        Evaluates the specified expression and returns the result.

        `expr`
            An expression, commonly a path expression.
        `lang`
            Optional string identifying the language of the expression.
            If the language is not specified, the defailt language
            will be used.
        """
    def add_iid(iid):
        """\
        Adds the item identifier `iid` to this Topic Maps construct.
        
        Raises an `IdentityViolation` if another Topic Maps construct with
        the item identifier exists or if a topic with a subject identifier
        equals to the specified item identifier exists.
        """
    def remove_iid(iid):
        """\
        Removes the item identifier `iid` from this Topic Maps construct.
        """
    def __atomify__():
        """\
        Returns a representation of this Topic Maps construct.
        For Topic Maps constructs which have a value (names, occurrences, 
        variants), the representation of the value should be returned.
        """
    id = Attribute("""\
    Returns the (internal) identifier of this construct.
    If the identifier is stable depends on the backend. A backend implementation
    may decide to change the identifier at any time.
    
    It is highly recommended to stay in the Topic Maps Data Model and to use
    item identifiers, subject identifiers and subject locators to identify
    Topic Maps constructs.
    
    This attribute is read-only.
    """)
    parent = Attribute("""\
    Returns the parent of this Topic Maps construct.
    For topics and associations the parent must be equivalent to the `tm` 
    property.
    
    Instances of ``ITopicMap`` return ``None``.
    
    This attribute is read-only.
    """
    )
    tm = Attribute("""\
    Returns the topic map where this Topic Maps construct is part of.
    ``ITopicMap`` instances return theirself.
    
    This attribute is read-only.
    """
    )
    iids = Attribute("""\
    Returns the item identifiers.
    
    This attribute is read-only.
    """
    )

class IReifiable(IConstruct):
    """\
    Interface for all reifiable Topic Maps constructs (all constructs which
    are not topics).
    
    This interface has no representation in the TMDM.
    """
    reifier = Attribute("""\
    Returns / sets the reifier.
    
    If the topic that should reify this construct reifies another construct,
    a ModelConstraintViolation is raised.
    """
    )

class ITyped(IConstruct):
    """\
    Interface for all typed Topic Maps constructs (association, role,
    occurrence, and name).
    
    This interface has no representation in the TMDM.
    """
    type = Attribute("""\
    Returns / sets the type.
    
    The type is never ``None`` and cannot be set to ``None``.
    """
    )

class IScoped(IConstruct):
    """\
    Interface for all scoped Topic Maps constructs (association,
    occurrence, name, and variant).
    
    This interface has no representation in the TMDM.
    """
    scope = Attribute("""\
    Returns and sets the scope of this construct.
    
    The returned value is an iterable.
    It is allowed to set the scope to a single topic and to an iterable.
    """
    )

class ITopicMap(IConstruct, IReifiable):
    """\
    Represents a TMDM topic map.
    
    C.f. `5.2 The topic map item <http://www.isotopicmaps.org/sam/sam-model/#d0e654>`_
    """
    def __iand__(tm):
        """\
        Shortcut for `merge`
        
        ::
            >>> tm &= tm2 # Merges tm with tm2. tm2 won't be modified.
        """
    def merge(other):
        """\
        Merges this topic map with the ``other``. The ``other`` topic map
        won't be modified.
        
        .. Note:: Both topic maps must belong to the same connection. It is
                  not possible to merge a topic map from connection A with a
                  topic map from connection B).
        """
    def topic(*identity, **kw):
        """\
        Returns a topic by its subject identifier or item identifier, or
        subject locator.
        
        The caller may use one of the identity indicating keywords:
        
        ``sid``
            To retrieve a topic with the specified subject identifier.
            Returns the same result as ``tm.topic_by_sid(iri)``
        ``slo``
            To retrieve a topic with the specified subject locator.
            Returns the same result as ``tm.topic_by_slo(iri)``
        ``iid``
            To retrieve a topic with the specified item identifier.
            Returns the same result as ``tm.topic_by_iid(iri)``
        
        .. Note:: If the keyword ``iid`` or the ``identity`` is used and this 
                  method returns ``None``, a Topic Maps construct with the 
                  specified item identifier may exists (which is not a topic).
        
        ::
        
            >>> # Fetches a topic with the subject locator 'http://www.google.com/'
            >>> t = tm.topic('= http://www.google.com/')
            
            >>> # Fetches a topic by its subject identifier or item identifer
            >>> t = tm.topic('http://psi.semagia.com/something')
            
            >>> # Fetches a topic explicitly by its item identifier
            >>> t = tm.topic(iid='http://www.semagia.com/somemap/iid')
            
            >>> # Fetches a topic explicitly by its subject identifier
            >>> t = tm.topic(sid='http://psi.semagia.com/something')
            
            >>> # Fetches a topic explicitly by its subject locator
            >>> t = tm.topic(slo='http://www.semagia.com/')
            
            >>> # Example where a Topic Maps construct exists even if this method returns `None`
            >>> a = tm.create_association(tm.create_topic())
            >>> a.add_iid('http://www.semagia.com/some-map/somewhere')
            >>> t = tm.topic('http://www.semagia.com/some-map/somewhere')
            >>> t is None
            True
        """
    def topic_by_iid(iid):
        """\
        Returns a topic with the specified item identifier. 
        If no topic with that item identifier exists, ``None`` is returned.
        
        .. Note:: There may be a Topic Maps construct in the topic map with
                  the specified item identifier (i.e. a name) even if this
                  method return ``None``.
        """
    def topic_by_sid(sid):
        """\
        Returns a topic with the specified subject identifier.
        If no topic with that subject identifier exists, ``None`` is returned.
        """
    def topic_by_slo(slo):
        """\
        Returns a topic with the specified subject locator.
        If no topic with that subject locator exists, ``None`` is returned.
        """
    def construct(*identity, **kw):
        """\
        Returns a Topic Maps construct by its item identifier or internal
        identifier.
        
        ::
        
            >>> # Return a Topic Maps construct by its item identifier
            >>> a = tm.construct('http://www.semagia.com/some-map/assoc-iid')
            >>> # Return a Topic Maps construct by its internal identifier
            >>> a2 = tm.construct(id=a.id)
            >>> a == a2
            True
            >>> # With explicit keyword ``iid``
            >>> a3 = tm.construct(iid='http://www.semagia.com/some-map/assoc-iid')
            >>> a == a3
            True
        """
    def construct_by_id(ident):
        """\
        Returns a Topic Maps construct with the specified internal identifier.
        If no such construct exists, ``None`` is returned.
        """
    def construct_by_iid(iid):
        """\
        Returns a Topic Maps construct with the specified item identifier.
        If no such construct exists, ``None`` is returned.
        """
    def create_topic(*identity, **kw):
        """\
        Creates a topic with the specified identity.
        
        The caller may specify an IRI for the `identity`. That identity is
        used to resolve a topic by its subject identitfiers or item identifiers.
        If no topic with the specified `identity` exists, a topic with an item
        identifier equals to `identity` is created and returned.
        
        The caller may use one of the identity indicating keywords:
        
        ``sid``
            To create (or retrieve) a topic with the specified subject identifier.
        ``slo``
            To create (or retrieve) a topic with the specified subject locator.
        ``iid``
            To create (or retrieve) a topic with the specified item identifier.
        
        If no identity is provided (no identity, subject identifier,
        subject locator, or item identifier), a random item identifier is
        attached to the newly created topic.
        
        ::
        
            >>> 'http://www.semagia.com/some-map/id' in tm
            False
            >>> # t is created and the item identifier 'http://www.semagia.com/some-map/id' is assigned
            >>> t = tm.create_topic('http://www.semagia.com/some-map/id')
            >>> t2 = tm.create_topic('http://www.semagia.com/some-map/id')
            >>> t is t2
            True
            >>> 'http://www.semagia.com/some-map/id' in t.iids
            True
            >>> 'http://www.semagia.com/some-map/id' in t.sids
            False
            >>> t3 = tm.create_topic(sid='http://www.semagia.com/some-map/id')
            >>> t == t3
            True
            >>> 'http://www.semagia.com/some-map/id' in t.sids
            True
            >>> '= http://www.semagia.com/' in tm
            False
            >>> t4 = tm.create_topic('= http://www.semagia.com/')
            >>> '= http://www.semagia.com/' in tm
            True
            >>> t5 = tm.create_topic(slo='http://www.semagia.com/')
            >>> t4 == t5
            True
        """
    def create_topic_by_iid(iid):
        """\
        Creates and returns a topic with the specified item identifier.
        
        If a topic with the item identifier already exists, the existing 
        topic is retuned. If a topic with a subject identifier equal to 
        the provided item identifier exists, the item identifier is added
        to the existing topic and the existing topic is returned.
        """
    def create_topic_by_sid(sid):
        """\
        Creates and returns a topic with the specified subject identifier.
        
        If a topic with the subject identifier already exists, the existing 
        topic is retuned. If a topic with an item identifier equal to 
        the provided subject identifier exists, the subject identifier is added
        to the existing topic and the existing topic is returned.
        """
    def create_topic_by_slo(slo):
        """\
        Creates and returns a topic with the specified subject locator.
        
        If a topic with the subject locator already exists, the existing 
        topic is retuned.
        """
    def create_association(type, roles, scope=UCS):
        """\
        Creates an returns an association with the specified ``type`` and 
        ``roles`` and ``scope`` (by default the unconstrained scope).
        
        `type`
            The topic that represents the type of the occurrence.
            That value must not be ``None``.
        `roles`
            An iterable of (type, player) pairs.
        `scope`
            An iterable of topics which should become the scope of the
            occurrence.
        """
    iri = Attribute("""\
    The storage address of this topic map.
    
    This attribute is read-only.
    """)
    topics = Attribute("""\
    Returns the topics of this topic map.
    
    This attribute is read-only.
    """
    )
    associations = Attribute("""\
    Returns the associations of this topic map.
    
    This attribute is read-only.
    """
    )

class ITopic(IConstruct):
    """\
    Represents a TMDM topic.
    
    C.f. `5.3 Topic items <http://www.isotopicmaps.org/sam/sam-model/#d0e736>`_
    """
    def add_type(type):
        """\
        Creates a type-instance relationship in the unconstrained scope between
        this topic and the specified type. 
        
        This topic plays the instance role and the `type` plays the type role.
        """
    def remove_type(type):
        """\
        Removes a type-instance relationship between this topic and the
        specified `type`.
        """
    def add_sid(sid):
        """\
        Adds the specified subject identifier `sid` to the topic.
        
        Raises an `IdentityViolation` if another topic with the same
        subject identifier or item identifiers exists.
        """
    def remove_sid(sid):
        """\
        Removes the specified subject identifier `sid` from the topic.
        """
    def add_slo(slo):
        """\
        Adds the specified subject locator `slo` to the topic.
        
        Raises an `IdentityViolation` if another topic with the same
        subject locator exists.
        """
    def remove_slo(slo):
        """\
        Removes the specified subject locator `slo` from the topic.
        """
    def __iand__(tm):
        """\
        Shortcut for `merge`

        ::
            >>> topic &= topic2 # Merges topic with topic2
        """
    def merge(other):
        """\
        Merges this topic with the `other`. The `other` topic will be
        removed from the topic map.
        
        Both topics MUST have the same topic map parent.
        
        After calling this method, this topic will have all characteristics
        (occurrences, names, roles played) from the ``other`` topic.
        This method may cause side effects: If i.e. an occurrence from the
        ``other`` topic is equal to an occurrence of this topic and both
        occurrences are reified, the reifiers of the occurrences get merged, too.
        See `6 Merging <http://www.isotopicmaps.org/sam/sam-model/#sect-merging>`_
        for details.
        
        Raises a `ModelConstraintViolation` if both topics reify a Topic
        Maps construct.
        """
    def roles_by(type, assoc_type=ANY, scope=ANY):
        """\
        Returns the roles this topic plays with the specified `type`.
        If the `assoc_type` is specified, only those roles will be returned
        which are part of an association with the specified type.
        If the scope is specified, the scope of the associations is also taken
        into account.
        """
    def remove():
        """\
        Removes this topic from the parent.
        """
    def occurrences_by(type, scope=ANY, exact=True):
        """\
        Returns all occurrences with the specified type and scope. If ``exact``
        is set to ``False`` (set to ``True`` by default), an occurrence is valid
        in the specified scope if the scope is a subset of the occurrence
        scope property.
        """
    def create_occurrence(type, value, scope=UCS):
        """\
        Creates and returns an occurrence with the specified type, value and
        scope (by default the scope is set to the unconstrained scope).
        
        `type`
            The topic that represents the type of the occurrence.
            This value must not be ``None``.
        `value`
            The value of the occurrence. This may be string or one of Python's
            native datatypes like ``int``, ``float``, ``date`` etc. or a
            value/datatype-tuple.
        `scope`
            An iterable of topics which should become the scope of the
            occurrence.
        
        ::
        
            >>> occ = t.create_occurrence(homepage, ('http://www.semagia.com', XSD.anyURI))
            >>> occ2 = t.create_occurrence(shoesize, 46)
        """
    def names_by(type, scope=ANY, exact=True):
        """\
        Returns all names with the specified `type` and `scope`. If `exact` is
        set to `False` (set to ``True`` by default), a name is valid in the
        specified scope iff the name's scope is a superset of the provided scope.
        """
    def create_name(type, value, scope=UCS):
        """\
        Creates and returns a name with the specified type, value and scope
        (by default the scope is set to the unconstrained scope).
        
        `type`
            A topic which represents the type of the name.
            If `type` is set to ``None``, the type of the name
            if set to a topic which contains the subject identifier
            `http://psi.topicmaps.org/iso13250/model/topic-name` (if no such
            topic exists, a topic is created).
        `value`
            The value of the topic name.
        `scope`
            An iterable of topics which become the scope of the name.
        """
    def __setitem__(name_or_occ_expr, value):
        """\
        Creates an occurrence or a name with the specified value.
        
        ::
        
            >>> t = tm.create_topic()
            >>> len(tuple(t.names))
            0
            >>> t['- name'] = 'Some name'
            >>> len(tuple(t.names))
            1
            >>> t['-'] = 'Default name' # Create a name with the default TMDM name type
            >>> len(tuple(t.names))
            2
            >>> len(tuple(t.occurrences))
            0
            >>> t['homepage'] = 'http://www.example.org/', XSD.anyURI
            >>> len(tuple(t.occurrences))
            1
        """
    def __getitem__(name_or_occ):
        """\
        Returns names or occurrences with the specified type.
        
        
        """
    def close():
        """\
        Closes this topic map instance.
        """
    types = Attribute("""\
    Returns the types of this topic.
    
    Only those types are returned where the type-instance relationship is
    in the unconstrained scope.

    This attribute is read-only.
    """
    )
    sids = Attribute("""\
    Returns the subject identifiers.
    
    This attribute is read-only.
    """
    )
    slos = Attribute("""\
    Returns the subject locators.
    
    This attribute is read-only.
    """
    )
    occurrences = Attribute("""\
    Returns the ocurrences.
    
    This attribute is read-only.
    """
    )
    names = Attribute("""\
    Returns the names.
    
    This attribute is read-only.
    """
    )
    played_types = Attribute("""\
    Returns the role types played by this topic.

    This attribute is read-only.
    """)
    roles_played = Attribute("""\
    Returns the roles where this topic plays a role.
    
    This attribute is read-only.
    """
    )
    reified = Attribute("""\
    Returns the reified Topic Maps construct or `None` if this topic
    does not reify anything.
    
    This attribute is read-only.
    """
    )

class IAssociation(IScoped, ITyped, IReifiable):
    """\
    Represents a TMDM association.
    
    C.f. `5.7 Association items<http://www.isotopicmaps.org/sam/sam-model/#sect-association>`_
    """
    def players_by(type):
        """\
        Returns all players which play a role of the specified type.
        
        .. Note:: The result is the same as using the `assoc[type]` notation
        
        Examples::
        
            >>> for player in assoc.players_by(type):
            ...     do_something_with(player)
        """
    def create_role(type, player):
        """\
        Creates and returns a role with the specified type/player combination.
        """
    def __setitem__(type, player):
        """\
        Creates a new role with the specified type/player pair.
        
        The type and player may be strings, or topic instances.
        
        Examples::
        
            >>> # Using strings which are resolved into item identifiers
            >>> is_member_of = tm.create_topic(sid='http://psi.example.org/member-of')
            >>> assoc = tm.create_association(type=is_member_of)
            >>> assoc['group'] = 'the-beatles'
            >>> assoc['member'] = 'paul'
            >>> 
            >>> # Using strings and topics.
            >>> a2 = tm.create_association(type=is_member_of)
            >>> the_beatles = tm.create_topic(sid='http://psi.the-beatles.com/beatles')
            >>> john = tm.create_topic(sid='http://psi.the-beatles.com/john')
            >>> member = tm.create_topic(sid='http://psi.example.org/member')
            >>> a2['group'] = the_beatles
            >>> a2[member] = john
        """
    def __getitem__(type):
        """\
        Returns all players that play the specified role.
        
        The type may be a string or a topic instance.
        """
    def __contains__(role):
        """\
        Returns if the role is contained in this association.
        """
    def __iter__():
        """\
        Returns an iterable over the roles of this association.
        
        Algorithms which yield the same result::
        
            >>> for role in assoc.roles:
            ...     do_something_with(role)
        
            >>> for role in assoc:
            ...     do_something_with(role)
        
        It's also possible to access the type and the player of the association 
        roles as follows:
        
            >>> for role in assoc.roles:
            ...    do_something_with(role.type, role.player)
            
            >>> for type, player in assoc.roles:
            ...    do_something_with(type, player)
            
            >>> for type, player in assoc:
            ...    do_something_with(type, player)
        """
    def __len__():
        """\
        Returns the arity of this association.
        
        ::
        
            >>> assoc = tm.create_association(type=tm.create_topic())
            >>> len(assoc)
            0
            >>> r = assoc.create_role(type=tm.create_topic(), player=tm.create_topic())
            >>> len(assoc)
            1
        """
    def remove():
        """\
        Removes this association from the topic map.
        """
    roles = Attribute("""\
    Returns the association roles.
    
    This attribute is read-only.
    """
    )

class IRole(ITyped, IReifiable):
    """\
    Represents a TMDM association role.
    
    C.f. `5.8 Association role items<http://www.isotopicmaps.org/sam/sam-model/#sect-assoc-role>`_
    """
    def remove():
        """\
        Removes this role from its parent.
        """
    player = Attribute("""\
    Returns / sets the player.
    """
    )

class IDatatyped(IScoped, IReifiable):
    """\
    Represents a Topic Maps construct which has a value and a datatype property.
    
    `IOccurrence`s and `IVariant`s are derived from this iterface.
    
    This interface has no representation in the TMDM.
    """
    def __int__():
        """\
        Returns the integer representation of this construct.
        """
    def __long__():
        """\
        Returns the long representation of this construct.
        """
    def __float__():
        """\
        Returns the float representation of this construct.
        """
    def __str__():
        """\
        Returns the string representation of this construct.
        """
    value = Attribute("""\
    A string. If the datatype is ``xsd:anyURI``, a locator referring to the 
    information resource; otherwise the string is the value.
    
    To set the value, it is possible to use either one of the Python's native
    datatypes like ``int``, ``float`` etc. or to use a tuple where the first
    element represents the value and the second element represents an IRI::
    
        >>> occ.value = 2.0
        >>> occ.value
        u'2.0
        >>> occ.datatype
        u'http://www.w3.org/2001/XMLSchema#float'
        >>> occ.value = 1
        >>> occ.value
        u'1'
        >>> occ.datatype
        u'http://www.w3.org/2001/XMLSchema#integer'
        >>> occ.value = 'something', 'http://psi.example.org/this-is-not-a-string'
        >>> occ.value
        u'something'
        >>> occ.datatype
        u'http://psi.example.org/this-is-not-a-string'
    """
    )
    datatype = Attribute("""\
    A locator. A locator identifying the datatype of the value.
    
    This attribute is read-only.
    """
    )

class IOccurrence(IDatatyped, ITyped):
    """\
    Represents a TMDM occurrence.
    
    C.f. `5.6 Occurrence items<http://www.isotopicmaps.org/sam/sam-model/#sect-occurrence>`_
    """
    def remove():
        """\
        Removes this occurrence from its parent.
        """

class IName(IScoped, ITyped, IReifiable):
    """\
    Represents a TMDM topic name.
    
    C.f. `5.4 Topic name items<http://www.isotopicmaps.org/sam/sam-model/#sect-topic-name>`_
    """
    def create_variant(value, scope):
        """\
        Creates an returns a variant with the specified value and scope.
        """
    def __iter__():
        """\
        Returns an iterable over the variants of this name.
        
        ::
        
            >>> for variant in name.variants:
            ...     do_something_with(variant)
        
            >>> for variant in name: # Yields the same result
            ...     do_something_with(variant)
        """
    def remove():
        """\
        Removes this name from its parent.
        """
    value = Attribute("""\
    Returns / sets the value.
    """
    )
    variants = Attribute("""\
    Returns the variants.
    
    This attribute is read-only.
    """
    )

class IVariant(IDatatyped):
    """\
    Represents a TMDM variant.
    
    C.f. `5.5 Variant items<http://www.isotopicmaps.org/sam/sam-model/#sect-variant>`_
    """
    def remove():
        """\
        Removes this variant from its parent.
        """
    scope = Attribute("""\
    Returns the scope of this variant. The scope of the variant includes
    the scope of the parent topic name.
    
    This attribute is read-only.
    """
    )
