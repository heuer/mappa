# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Table definitions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from sqlalchemy import Table, MetaData, Column, Integer, String, Text, Index

metadata = MetaData()

mysql_engine = u'InnoDB'  # u'MyISAM'


#
# -- TMO tables
#
topicmap = Table(u'TM_TOPIC_MAP', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'title', String(128), nullable=True),
    Column(u'base_address', String(255), nullable=True),
    Column(u'comments', Text, nullable=True),
    Index(u'TM_TOPIC_MAP_IX_ai', u'base_address', u'id'),
    mysql_engine=mysql_engine,
)

topic = Table(u'TM_TOPIC', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reified_id', String(32), nullable=True),
    Index(u'TM_TOPIC_IX_im', u'id', u'topicmap_id'),
    mysql_engine=mysql_engine,
)

association = Table(u'TM_ASSOCIATION', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'type_id', Integer, nullable=True),
    Index(u'TM_ASSOCIATION_IX_myi', u'topicmap_id', u'type_id', u'id'),
    mysql_engine=mysql_engine
)

role = Table(u'TM_ASSOCIATION_ROLE', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'assoc_id', Integer, nullable=False),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'type_id', Integer, nullable=True),
    Column(u'player_id', Integer, nullable=True),
    Index(u'TM_ASSOCIATION_ROLE_IX_o', u'assoc_id'),
    Index(u'TM_ASSOCIATION_ROLE_IX_io', u'id', u'assoc_id'),
    Index(u'TM_ASSOCIATION_ROLE_IX_t', u'player_id'),
    Index(u'TM_ASSOCIATION_ROLE_IX_it', u'id', u'player_id'),
    Index(u'TM_ASSOCIATION_ROLE_IX_myi', u'topicmap_id', u'type_id', u'id'),
    Index(u'TM_ASSOCIATION_ROLE_IX_mtyio', u'topicmap_id', u'player_id', u'type_id', u'id', u'assoc_id'),
    mysql_engine=mysql_engine,
)


occurrence = Table(u'TM_OCCURRENCE', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'topic_id', Integer, nullable=False),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'type_id', Integer, nullable=True),
    Column(u'datatype_address', String(255), nullable=True),
    Column(u'length', Integer, nullable=True),
    Column(u'hashcode', Integer, nullable=True),
    Column(u'content', Text, nullable=True),
    Index(u'TM_OCCURRENCE_IX_o', u'topic_id'),
    Index(u'TM_OCCURRENCE_IX_myi', u'topicmap_id', u'type_id', u'id'),
    Index(u'TM_OCCURRENCE_IX_mhi', u'topicmap_id', u'hashcode', u'id'),
    mysql_engine=mysql_engine,
)

name = Table(u'TM_TOPIC_NAME', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'topic_id', Integer, nullable=False),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'type_id', Integer, nullable=False),
    Column(u'content', Text, nullable=True),
    Index(u'TM_TOPIC_NAME_IX_o', u'topic_id'),
    Index(u'TM_TOPIC_NAME_IX_myi', u'topicmap_id', u'type_id', u'id'),
    Index(u'TM_TOPIC_NAME_IX_mvi', u'topicmap_id', u'content', u'id'),
    mysql_engine=mysql_engine,
)

variant = Table(u'TM_VARIANT_NAME', metadata,
    Column(u'id', Integer, nullable=False, primary_key=True),
    Column(u'name_id', Integer, nullable=False),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'reifier_id', Integer, nullable=True),
    Column(u'datatype_address', String(255), nullable=True),
    Column(u'length', Integer, nullable=True),
    Column(u'hashcode', Integer, nullable=True),
    Column(u'content', Text, nullable=True),
    Index(u'TM_VARIANT_NAME_IX_o', u'name_id'),
    Index(u'TM_VARIANT_NAME_IX_mhi', u'topicmap_id', 'hashcode', 'id'),
    mysql_engine=mysql_engine,
)

topic_type = Table(u'TM_TOPIC_TYPES', metadata,
    Column(u'topic_id', Integer, nullable=False, primary_key=True),
    Column(u'type_id', Integer, nullable=False, primary_key=True),
    Index(u'TM_TOPIC_TYPES_IX_yt', u'type_id', u'topic_id'),
    mysql_engine=mysql_engine,
)


#
# -- Identity tables
#
subject_identifier = Table(u'TM_SUBJECT_IDENTIFIERS', metadata,
    Column(u'topic_id', nullable=False),
    Column(u'address', String(255), nullable=False),
    Index(u'TM_SUBJECT_IDENTIFIERS_IX_oa', u'topic_id', u'address'),
    Index(u'TM_SUBJECT_IDENTIFIERS_IX_am', u'address', u'topic_id'),
    mysql_engine=mysql_engine,
)

subject_locator = Table(u'TM_SUBJECT_LOCATORS', metadata,
    Column(u'topic_id', nullable=False),
    Column(u'address', String(255), nullable=False),
    Index(u'TM_SUBJECT_LOCATORS_IX_oa', u'topic_id', u'address'),
    Index(u'TM_SUBJECT_LOCATORS_IX_am', u'address', u'topic_id'),
    mysql_engine=mysql_engine,
)

item_identifier = Table(u'TM_ITEM_IDENTIFIERS', metadata,
    Column(u'class', String(1), nullable=False),
    Column(u'tmobject_id', Integer, nullable=False),
    Column(u'topicmap_id', Integer, nullable=False),
    Column(u'address', String(255), nullable=False),
    Index(u'TM_ITEM_IDENTIFIERS_IX_o', u'tmobject_id'),
    Index(u'TM_ITEM_IDENTIFIERS_IX_maco', u'topicmap_id', u'address', u'class', u'tmobject_id'),
    mysql_engine=mysql_engine,
)


#
# -- Scope tables
#

association_scope = Table(u'TM_ASSOCIATION_SCOPE', metadata,
    Column(u'scoped_id', Integer, nullable=False),
    Column(u'theme_id', Integer, nullable=False),
    Index(u'TM_ASSOCIATION_SCOPE_IX_hs', u'theme_id', u'scoped_id'),
    mysql_engine=mysql_engine,
)

occurrence_scope = Table(u'TM_OCCURRENCE_SCOPE', metadata,
    Column(u'scoped_id', Integer, nullable=False),
    Column(u'theme_id', Integer, nullable=False),
    Index(u'TM_OCCURRENCE_SCOPE_IX_hs', u'theme_id', u'scoped_id'),
    mysql_engine=mysql_engine,
)

name_scope = Table(u'TM_TOPIC_NAME_SCOPE', metadata,
    Column(u'scoped_id', Integer, nullable=False),
    Column(u'theme_id', Integer, nullable=False),
    Index(u'TM_TOPIC_NAME_SCOPE_IX_hs', u'theme_id', u'scoped_id'),
    mysql_engine=mysql_engine,
)

variant_scope = Table(u'TM_VARIANT_NAME_SCOPE', metadata,
    Column(u'scoped_id', Integer, nullable=False),
    Column(u'theme_id', Integer, nullable=False),
    Index(u'TM_VARIANT_NAME_SCOPE_IX_hs', u'theme_id', u'scoped_id'),
    mysql_engine=mysql_engine,
)
