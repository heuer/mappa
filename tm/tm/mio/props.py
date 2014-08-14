# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides access to standard MIO properties.

By convention, the hyphen (``-``) in the PSIs is replaced by an underscore
character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import MIO_PROPS

# Indicates that the syntax of the source should be validated if this property
# is set to ``True``
validate = MIO_PROPS[u'validate']

# Indicates that any directive to merge in another topic map is ignored if
# this property is set to ``True``
ignore_mergemap = MIO_PROPS[u'ignore-mergemap']

# Indicates that any directive to include another topic map is ignored if
# this property is set to ``True``.
# Example: The ``#INCLUDE`` directive in LTM or ``%include`` in CTM.
ignore_include = MIO_PROPS[u'ignore-include']

# Indicates a RDF to Topic Maps mapping (RTM).
rdf2tm_mapping = MIO_PROPS[u'rdf2tm-mapping']

# Indicates the RDF mapping syntax for RDF to Topic Maps (RTM).
rdf2tm_mapping_syntax = MIO_PROPS[u'rdf2tm-mapping-syntax']

# Indicates an IRI to the mapping source for RDF to Topic Maps (RTM).
rdf2tm_mapping_iri = MIO_PROPS[u'rdf2tm-mapping-iri']

# Indicates if unhandled statements (triples) should be logged.
rdf2tm_report_unhandled_statements = MIO_PROPS[u'rdf2tm-report-unhandled-statements']

# Indicates if the translation process should be stopped if an error occurs.
rdf2tm_stop_on_error = MIO_PROPS[u'rdf2tm-stop-on-error']

# Indicates the language tag provider
rdf2tm_language_provider = MIO_PROPS[u'rdf2tm-language-provider']

# Indicates that the LTM deserializer should act in the legacy mode
# if set to ``True``.
ltm_legacy = MIO_PROPS[u'ltm-legacy']
