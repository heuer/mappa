<?xml version="1.0" encoding="utf-8"?>
<!--

  This stylesheet calculates the costs of the query predicates and adds
  a "cost" attribute to the predicates.

  TODO: Handle predicates created by "fold-type" and "fold-scope"


  Copyright (c) 2010 - 2014, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                exclude-result-prefixes="tl">

  <xsl:output method="xml" encoding="utf-8" standalone="yes"/>

  <xsl:variable name="INFINITE_RESULT" select="10000"/>
  <xsl:variable name="WHOLE_TM_RESULT" select="1000"/>
  <xsl:variable name="BIG_RESULT"      select="100"/>
  <xsl:variable name="MEDIUM_RESULT"   select="10"/>
  <xsl:variable name="SMALL_RESULT"    select="3"/>
  <xsl:variable name="SINGLE_RESULT"   select="1"/>
  <xsl:variable name="FILTER_RESULT"   select="0"/>
  <xsl:variable name="FAIL_RESULT"     select="-1"/>
  
  <xsl:variable name="MOD_EXPERIMENTAL" select="'http://psi.ontopia.net/tolog/experimental/'"/>
  <xsl:variable name="MOD_STRING" select="'http://psi.ontopia.net/tolog/string/'"/>
  <xsl:variable name="MOD_NUMBER" select="'http://psi.ontopia.net/tolog/number/'"/>

  <xsl:key name="namespaces"
             match="tl:namespace[@kind='module']"
             use="@identifier"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='base-locator'
                                            or @name='topic-map']">
    <!--** Generic match for base-locator and topic-map -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='base-locator'
                                            or @name='topic-map'][count(tl:variable)=0]">
    <!--** Match for base-locator and topic-map where all variables are bound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate">
    <!--** Generic match for all built-in predicates (worst case, assuming that the whole TM is returned) -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:*[local-name(.) = 'builtin-predicate'
                            or local-name(.) = 'infix-predicate'
                            or local-name(.) = 'dynamic-predicate'][count(tl:variable)=0]">
    <!--** Match for all built-in predicates, infix predicates, and 
           (dynamic) occurrence predicates where all variables are bound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>
    
  <xsl:template match="tl:internal-predicate[@name='types' or @name='direct-types']">
    <xsl:variable name="costs">
        <xsl:choose>
            <xsl:when test="@name='direct-types'"><xsl:value-of select="$BIG_RESULT - 1"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$BIG_RESULT"/></xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$costs"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='subject-identifier'
                                            or @name='subject-locator'
                                            or @name='variant'
                                            or @name='reifies'
                                            or @name='resource']
                                            [count(tl:variable)=2]">
    <!--** Matches those (binary) built-in predicates where all variables are unbound
           and produce a big result.

           * subject-identifier
           * subject-locator
           * variant
           * reifies
           * resource
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$BIG_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='subject-identifier'
                                            or @name='subject-locator'
                                            or @name='item-identifier'
                                            or @name='association-role'
                                            or @name='topic-name'
                                            or @name='occurrence'
                                            or @name='variant'
                                            or @name='reifies'
                                            or @name='object-id']
                                            [tl:*[1][local-name(.)='variable']]
                                            [tl:*[2][local-name(.)!='variable']]">
    <!--** Matches those (binary) built-in predicates where the first part is unbound and the 
           second part is bound and which produce a single result.

           * subject-identifier
           * subject-locator
           * item-identifier
           * association-role
           * topic-name
           * occurrence
           * variant
           * reifies
           * object-id
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='subject-identifier'
                                            or @name='subject-locator'
                                            or @name='item-identifier'
                                            or @name='association-role'
                                            or @name='topic-name'
                                            or @name='occurrence'
                                            or @name='variant'
                                            or @name='instance-of'
                                            or @name='direct-instance-of'
                                            or @name='scope']
                                            [tl:*[1][local-name(.)!='variable']]
                                            [tl:*[2][local-name(.)='variable']]">
    <!--** Matches those (binary) built-in predicates where the first part is bound and the 
           second part is unbound and which produce a small result.

           * subject-identifier
           * subject-locator
           * item-identifier
           * association-role
           * topic-name
           * occurrence
           * variant
           * instance-of
           * direct-instance-of
           * scope
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SMALL_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='role-player']
                                            [tl:*[1][local-name(.)='variable']]
                                            [tl:*[2][local-name(.)!='variable']]">
    <!--** Matches those (binary) built-in predicates where the first part is unbound and the 
           second part is bound and which produce a medium result.

           * role-player
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$MEDIUM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type'
                                            or @name='instance-of'
                                            or @name='direct-instance-of'
                                            or @name='scope'
                                            or @name='datatype']
                                            [tl:*[1][local-name(.)='variable']]
                                            [tl:*[2][local-name(.)!='variable']]">
    <!--** Matches those (binary) built-in predicates where the first part is unbound and the 
           second part is bound and which produce a big result.

           * type
           * instance-of
           * direct-instance-of
           * scope
           * datatype
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$BIG_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='role-player'
                                            or @name='type'
                                            or @name='reifies'
                                            or @name='object-id'
                                            or @name='datatype']
                                            [tl:*[1][local-name(.)!='variable']]
                                            [tl:*[2][local-name(.)='variable']]">
    <!--** Matches those (binary) built-in predicates where the first part is bound and the 
           second part is unbound and which produce a single result.

           * role-player
           * type
           * reifies
           * object-id
           * datatype
     -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate">
    <!--** Generic match all infix predicates (=, /=, >, >=, <, <=) -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$INFINITE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=0]">
    <!--** Matches the equals (=) predicate where all variables are bound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=1]">
    <!--** Matches the equals (=) predicate where one variable is bound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=2]">
    <!--** Matches the equals (=) predicate where all variables are unbound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:dynamic-predicate[count(tl:variable)=1]">
    <!--** Matches dynamic occurrence predicates where one variable is bound
    -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SMALL_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:dynamic-predicate[count(tl:variable)=2]">
    <!--** Matches dynamic occurrence predicates where all variables are unbound -->
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:association-predicate">
    <!--** Matches dynamic association predicates, i.e. member-of($member: member, $group: group) -->
    <xsl:variable name="pair-count" select="count(tl:pair)*2"/>
    <xsl:variable name="bound" select="count(tl:pair/tl:*/tl:*[local-name(.) != 'variable'])"/>
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost">
        <xsl:choose>
        <!--@ Check if all variables are bound -->
          <xsl:when test="$bound = $pair-count"><xsl:value-of select="$FILTER_RESULT"/></xsl:when>
          <!--@ Check if all variables are unbound -->
          <xsl:when test="$bound = 0"><xsl:value-of select="$BIG_RESULT"/></xsl:when>
          <!--@ Some variables are bound -->
          <xsl:otherwise><xsl:value-of select="$MEDIUM_RESULT - $bound"/></xsl:otherwise>
        </xsl:choose>
       </xsl:with-param>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@kind='module']]">
    <xsl:variable name="iri" select="key('namespaces', tl:name/tl:qname/@prefix)/@iri"/>
    <xsl:choose>
      <xsl:when test="$iri=$MOD_EXPERIMENTAL"><xsl:apply-templates select="." mode="module-experimental"/></xsl:when>
      <xsl:when test="$iri=$MOD_NUMBER"><xsl:apply-templates select="." mode="module-number"/></xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:identifier]">
    <!--** Matches rule invocations -->
    <xsl:variable name="open" select="count(tl:variable)"/>
    <xsl:choose>
      <xsl:when test="$open = 0">
        <xsl:call-template name="annotate">
          <xsl:with-param name="cost" select="$FILTER_RESULT"/>
        </xsl:call-template>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="annotate">
          <xsl:with-param name="cost" select="$BIG_RESULT + $open - 1"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
    
  <!--
        Module: Experimental
  -->
  <xsl:template match="@*|node()" mode="module-experimental">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='in']]
                                   [tl:*[1][local-name(.)='variable']]" mode="module-experimental">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SMALL_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='in']]
                                   [tl:*[1][local-name(.)!='variable']]" mode="module-experimental">
    <xsl:call-template name="annotate">
        <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='name']]
                                    [tl:*[1][local-name(.)!='variable']]
                                    [tl:*[2][local-name(.)!='variable']]" mode="module-experimental">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='name']]
                                    [tl:*[1][local-name(.)='variable']]
                                    [tl:*[2][local-name(.)!='variable']]" mode="module-experimental">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$INFINITE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='name']]
                                   [tl:*[1][local-name(.)!='variable']]
                                   [tl:*[2][local-name(.)='variable']]" mode="module-experimental">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

    
  <!--
        Module: Number
  -->

  <xsl:template match="@*|node()" mode="module-number">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <!--
        Module: String
  -->
  <xsl:template match="@*|node()" mode="module-string">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="annotate">
    <xsl:param name="cost"/>
    <xsl:element name="{name(.)}">
      <xsl:copy-of select="@*"/>
      <xsl:attribute name="cost"><xsl:value-of select="$cost"/></xsl:attribute>
      <xsl:apply-templates select="*"/>
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
