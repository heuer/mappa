# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Vocabularies.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import Namespace

XSD = Namespace(u'http://www.w3.org/2001/XMLSchema#')
"""\
Namespace for the XML Schema Datatypes
"""

TM = Namespace(u'http://psi.topicmaps.org/iso13250/')
"""\
Namespace for Topic Maps
"""

TMDM = Namespace(u'http://psi.topicmaps.org/iso13250/model/')
"""\
Namespace for the Topic Maps -- Data Model
"""

TMCL = Namespace(u'http://psi.topicmaps.org/tmcl/')
"""\
Namespace for the Topic Maps - Constraint Language
"""

TMQL = Namespace(u'http://psi.topicmaps.org/tmql/1.0/')
"""\
Namespace for Topic Maps - Query Language
"""

XTM_10 = Namespace(u'http://www.topicmaps.org/xtm/1.0/')
"""\
XML Topic Maps 1.0 namespace.
"""

XTM = Namespace(u'http://www.topicmaps.org/xtm/')
"""\
XML Topic Maps 2.0/2.1 namespace.
"""

DC = Namespace(u'http://purl.org/dc/elements/1.1/')
"""\
Dublin Core namespace.
"""

XLINK = Namespace(u'http://www.w3.org/1999/xlink')
"""\
XLink namespace.
"""

TMXML = Namespace(u'http://psi.ontopia.net/xml/tm-xml/')
"""\
TM/XML namespace.
"""

FOAF = Namespace(u'http://xmlns.com/foaf/0.1/')
"""\
Friend of a Friend namespace.
"""

SIOC = Namespace(u'http://rdfs.org/sioc/ns#')
"""\
SIOC (Semantically-Interlinked Online Communities) core namespace.
"""

RDF2TM = Namespace(u'http://psi.ontopia.net/rdf2tm/#')
"""\
RDF to Topic Maps (RTM) namespace.
"""

GR = Namespace(u'http://purl.org/goodrelations/v1#')
"""\
GoodRelations (GR) namespace.
"""

VCARD = Namespace(u'http://www.w3.org/2006/vcard/ns#')
"""\
VCard namespace.
"""

MIO_PROPS = Namespace(u'http://psi.semagia.com/mio/property/')
"""\
MIO Properties namespace.
"""

del Namespace
