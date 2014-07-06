# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
XTM 1.0 PSIs.

These PSIs can be used to work with topic maps which assume a XTM 1.0 model.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import XTM_10

DISPLAY = XTM_10['core.xtm#display']

SORT = XTM_10['core.xtm#sort']

DEFAULT_ASSOCIATION_TYPE = XTM_10[u'core.xtm#association']
"""\
Default association type.
"""

DEFAULT_OCCURRENCE_TYPE = XTM_10[u'core.xtm#occurrence']
"""\
Default occurrence type.
"""

DEFAULT_ROLE_TYPE = u'http://psi.semagia.com/xtm/1.0/role'
"""\
Default role type (it is legal to omit the role type in XTM 1.0)
"""

del XTM_10
