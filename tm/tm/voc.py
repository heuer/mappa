# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Vocabularies.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.namespace import Namespace

#pylint: disable-msg=W0105

XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
"""\
Namespace for the XML Schema Datatypes
"""

TMDM = Namespace('http://psi.topicmaps.org/iso13250/model/')
"""\
Namespace for the Topic Maps -- Data Model
"""

TMCL = Namespace('http://psi.topicmaps.org/tmcl/')
"""\
Namespace for the Topic Maps - Constraint Language
"""

TMQL = Namespace('http://psi.topicmaps.org/tmql/1.0/')
"""\
Namespace for Topic Maps - Query Language
"""

XTM_10 = Namespace('http://www.topicmaps.org/xtm/1.0/')
"""\
XML Topic Maps 1.0 namespace.
"""

XTM = Namespace('http://www.topicmaps.org/xtm/')
"""\
XML Topic Maps 2.0/2.1 namespace.
"""

DC = Namespace('http://purl.org/dc/elements/1.1/')
"""\
Dublin Core namespace.
"""

XLINK = Namespace('http://www.w3.org/1999/xlink')
"""\
XLink namespace.
"""

TMXML = Namespace('http://psi.ontopia.net/xml/tm-xml/')
"""\
TM/XML namespace.
"""

FOAF = Namespace('http://xmlns.com/foaf/0.1/')
"""\
Friend of a Friend namespace.
"""

SIOC = Namespace('http://rdfs.org/sioc/ns#')
"""\
SIOC (Semantically-Interlinked Online Communities) core namespace.
"""

RDF2TM = Namespace('http://psi.ontopia.net/rdf2tm/#')
"""\
RDF to Topic Maps (RTM) namespace.
"""

del Namespace
