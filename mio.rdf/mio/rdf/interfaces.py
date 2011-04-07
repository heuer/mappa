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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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

