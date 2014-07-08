# -*- coding: utf-8 -*-
#
#    ====================================
#    Topic Maps source -> PHPTMAPI script
#    ====================================
#
#    Donated to the public domain by Lars Heuer - Semagia <http://www.semagia.com/>.
#
"""\
``tm.mio.handler.MapHandler`` implementation for
`PHPTMAPI <http://phptmapi.sourceforge.net/>`_

TODOs:
 - Cases where a topic to $a is bound and $a is merged with $b --> $a disappears,
   later in the code we get again a reference to $a. Do we get a NPE?
   Ideally, $a should point to $b after it has been merged
 - Complicated reifier / duplicate reifiable statement relationships:
   If we try to set the reifier of $assoc_1 but the reifier is already assigned to
   $assoc_2, we should check if $assoc_1 is a duplicate of $assoc_2. If they
   are duplicates, we should merge them and do not throw a ModelConstraintException
 - Compliated item identifier / duplicate statement relationships:
   Same as with the reifier.
 - The import should be verfied through CXTM tests

I don't have a strong interest to fix the TODOs, contributions are welcome.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      Public Domain
"""
import tm.mio.handler as mio_handler

_SCRIPT_HOME = 'http://code.google.com/p/mappa/source/browse/sandbox/phptmapi/'


class PHPTMAPIMapHandler(mio_handler.HamsterMapHandler):
    """\
    MapHandler implementation that writes PHP statements for
    `PHPTMAPI <http://phptmapi.sourceforge.net/>`_
    """
    def __init__(self, out):
        """\
        Initializes the handler with the given topic map.
        
        `out`
            A file-alike object.
        """
        super(PHPTMAPIMapHandler, self).__init__()
        self._out = out
        self._counter = 0

    # PHPTMAPI 

    def startTopicMap(self):
        """\
        Writes the ``_HEADER``.
        """
        super(PHPTMAPIMapHandler, self).startTopicMap()
        self._out.write(_HEADER)

    def endTopicMap(self):
        """\
        Writes the function delimiter ``}`` and flushes the written
        PHP statements. ``out`` is not closed.
        """
        super(PHPTMAPIMapHandler, self).endTopicMap()
        self._out.write(_FOOTER)
        self._out.flush()

    def _create_topic_by_iid(self, iri):
        name = self._make_topic_variable()
        self._writeln(u"%s = $tm->createTopicByItemIdentifier('%s');" % (name, _escape(iri)))
        return name

    def _create_topic_by_sid(self, iri):
        name = self._make_topic_variable()
        self._writeln(u"%s = $tm->createTopicBySubjectIdentifier('%s');" % (name, _escape(iri)))
        return name

    def _create_topic_by_slo(self, iri):
        name = self._make_topic_variable()
        self._writeln(u"%s = $tm->createTopicBySubjectLocator('%s');" % (name, _escape(iri)))
        return name

    def _handle_item_identifier(self, topic, iri):
        self._writeln(u"_handle_item_identifier($tm, %s, '%s');" % (topic, _escape(iri)))

    def _handle_subject_identifier(self, topic, iri):
        self._writeln(u"_handle_subject_identifier($tm, %s, '%s');" % (topic, _escape(iri)))

    def _handle_subject_locator(self, topic, iri):
        self._writeln(u"_handle_subject_locator($tm, %s, '%s');" % (topic, _escape(iri)))

    def _handle_type_instance(self, instance, type):
        self._writeln(u'%s->addType(%s);' % (instance, type))

    def _handle_topicmap_item_identifier(self, iri):
        self._writeln(u"$tm->addItemIdentifier('%s');" % _escape(iri))

    def _handle_topicmap_reifier(self, reifier):
        self._writeln(u'$tm->setReifier(%s);' % reifier)

    def _create_association(self, type, scope, reifier, iids, roles):
        self._writeln(u'$assoc = $tm->createAssociation(%s, %s);' % (type, _make_scope(scope)))
        self._apply_reifier(u'$assoc', reifier)
        self._apply_iids(u'$assoc', iids)
        for role in roles:
            self._writeln(u'$role = $assoc->createRole(%s, %s);' % (role.type, role.player))
            self._apply_reifier(u'$role', role.reifier)
            self._apply_iids(u'$role', role.iids)

    def _create_occurrence(self, parent, type, value, datatype, scope, reifier, iids):
        self._writeln(u"$occ = %s->createOccurrence(%s, '%s', '%s', %s);" % (parent, type,
                                                                           _escape(value), _escape(datatype),
                                                                           _make_scope(scope)))
        self._apply_reifier(u'$occ', reifier)
        self._apply_iids(u'$occ', iids)

    def _create_name(self, parent, type, value, scope, reifier, iids, variants):
        self._writeln(u"$name = %s->createName('%s', %s, %s);" % (parent, _escape(value),
                                                                 type or 'null',
                                                                 _make_scope(scope)))
        self._apply_reifier(u'$name', reifier)
        self._apply_iids(u'$name', iids)
        for v in variants:
            self._writeln(u"$var = $name->createVariant('%s', '%s', %s);" % (_escape(v.value), _escape(v.datatype),
                                                                            _make_scope(v.scope)))
            self._apply_reifier(u'$var', v.reifier)
            self._apply_iids(u'$var', v.iids)
            

    #
    # -- Internal methods
    #
    def _apply_reifier(self, var, reifier):
        if reifier:
            self._writeln(u'%s->setReifier(%s);' % (var, reifier))

    def _apply_iids(self, var, iids):
        for iid in iids:
            self._writeln(u"%s->addItemIdentifier('%s');" % (var, _escape(iid)))

    def _make_topic_variable(self):
        self._counter+=1
        return u'$t_%d' % self._counter

    def _writeln(self, s, indent='    '):
        self._out.write(indent)
        if not isinstance(s, unicode):
            s = unicode(s, 'utf-8')
        self._out.write(s)
        self._out.write('\n')


def _escape(s):
    return s.replace(u"'", u"\\'")


def _make_scope(scope):
    if not scope:
        return u'$_UCS'
    return u'array(%s)' % ', '.join(scope)


# PHP script fragments
_HEADER = u'''<?php
/*
    DO NOT EDIT this file.

    It was automatically generated by <%s>.

    You need a PHPTMAPI implementation, i.e. QuaaxTM to run this script.

    PHPTMAPI: <http://phptmapi.sourceforge.net/>
    QuaaxTM:  <http://quaaxtm.sourceforge.net/>

*/

/**
 * Main entry point to fill a topic map with content.
 *
 * Note that this function should be called only once if the underlying
 * Topic Maps engine uses a persistent backend.
 * 
 * @param $tm An instance of PHPTMAPI ITopicMap.
 */
function populate_map($tm) {
    $_UCS = array();

''' % _SCRIPT_HOME

_FOOTER = u'''
}

function _get_topic_by_item_identifier($tm, $iri) {
    $existing = $tm->getConstructByItemIdentifier($iri);
    return ($existing instanceof Topic) ? $existing : null;
}

function _handle_subject_identifier($tm, $topic, $iri) {
    $existing = $tm->getTopicBySubjectIdentifier($iri);
    $existing = is_null($existing) ? _get_topic_by_item_identifier($tm, $iri) : $existing;
    if (!is_null($existing) && !$topic->equals($existing)) {
        $existing->mergeIn($topic);
        $topic = $existing;
    }
    $topic->addSubjectIdentifier($iri);
}

function _handle_item_identifier($tm, $topic, $iri) {
    $existing = _get_topic_by_item_identifier($tm, $iri);
    $existing = is_null($existing) ? $tm->getTopicBySubjectIdentifier($iri) : $existing;
    if (!is_null($existing) && !$topic->equals($existing)) {
        $existing->mergeIn($topic);
        $topic = $existing;
    }
    $topic->addItemIdentifier($iri);
}

function _handle_subject_locator($tm, $topic, $iri) {
    $existing = $tm->getTopicBySubjectLocator($iri);
    if (!is_null($existing) && !$topic->equals($existing)) {
        $existing->mergeIn($topic);
        $topic = $existing;
    }
    $topic->addSubjectLocator($iri);
}
?>
'''

