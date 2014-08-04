# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Constants.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio

IID = mio.ITEM_IDENTIFIER
SID = mio.SUBJECT_IDENTIFIER
SLO = mio.SUBJECT_LOCATOR
IRI = SID
IDENT   = 1000
VARIABLE= 1001
STRING  = 1002
DATE    = 1003
DATE_TIME = 1004
INTEGER = 1005
DECIMAL = 1006
WILDCARD = 1007
NAMED_WILDCARD = 1008
LITERAL = 1009
CTM_INTEGER = 1010
VIID = 1011
VSLO = 1012
IN_FOCUS = 1013

TOPIC_IN_FOCUS = IN_FOCUS, IN_FOCUS
