# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.proto import Interface, Attribute


class IMapper(Interface):
    """\
    Represents a handler which can map a RDF predicate IRI to a Topic Maps
    statement.
    """
    def handle_literal(handler, error_handler, subject, predicate, value, datatype, language):
        """\
        Handles a statement with a literal value.

        `handler`
            IMapHandler instance.
        `error_handler`
            IErrorHandler instance.
        `subject`
            The (absolute) IRI (a string) of the subject.
        `predicate`
            The (absolute) IRI (a string) of the predicate.
        `value`
            The literal's value
        `datatype`
            The literal's datatype.
        `language`
            The literal's language or ``None``.
        """

    def handle_object(handler, error_handler, subject, predicate, obj, is_blank_node):
        """\
        Handles a statement with an object.

        `handler`
            IMapHandler instance.
        `error_handler`
            IErrorHandler instance.
        `subject`
            The (absolute) IRI (a string) of the subject.
        `predicate`
            The (absolute) IRI (a string) of the predicate.
        `obj`
            The (absolute) IRI (a string) of the object.
        `is_blank_node`
            Indicates if the object's IRI was created from a blank node.
        """


class IMappingHandler(Interface):
    """\
    
    
    """
    def start():
        """\

        """

    def end():
        """\

        """

    def handleComment(comment):
        """\

        """
    
    def handlePrefix(prefix, iri):
        """\

        """

    def handleAssociation(predicate, subject_role, object_role, scope, type):
        """\

        """

    def handleOccurrence(predicate, scope, type, lang2scope=False):
        """\

        """

    def handleName(predicate, scope, type, lang2scope=False):
        """\

        """

    def handleInstanceOf(predicate, scope):
        """\

        """

    def handleSubtypeOf(predicate, scope):
        """\

        """

    def handleSubjectIdentifier(predicate):
        """\

        """

    def handleSubjectLocator(predicate):
        """\

        """

    def handleItemIdentifier(predicate):
        """\

        """


class IMappingReader(Interface):
    """\
    
    """
    def read(source):
        """\
        
        """

    mapping_handler = Attribute("Returns/sets the mapping handler")
    prefix_listener = Attribute("Returns/sets the prefix listener")


class IErrorHandler(Interface):
    """\
    Handler which receives notifications about errors.
    """
    def reject_literal(name, value, datatype):
        """\
        
        `value`
            The value of the literal.
        `datatype`
            The IRI of the datatype.
        """

    def reject_nonliteral(name, obj_iri):
        """\
        
        `obj_iri`
            The IRI of the object.
        """

    def reject_blank_node(name):
        """\
        
        `name`
            The name of the IMapper.
        """

