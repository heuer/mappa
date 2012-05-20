<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet annotates predicates like "type" and "value" with
  a "hint" attribute that indicates which kind of Topic Maps statement
  is meant.
  
  I.e.:
    
    association($a), type($a, $type)?

    Input XML:
      <builtin-predicate name="asssociation">
        [...]
      </builtin-predicate>
      <builtin-predicate name="type">
         [...]
      </builtin-predicate>

    Output XML:
      <builtin-predicate name="asssociation">
        [...]
      </builtin-predicate>
      <builtin-predicate name="type" hint="association-type">
        [...]
      </builtin-predicate>

  
  Supported predicates:
  * type
  * scope
  * value
  * value-like
  * datatype
  * reifies
  * resource

  Copyright (c) 2010 - 2012, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                exclude-result-prefixes="tl">

  <!-- Indicates if the predicates should be rewritten or just annotated -->
  <xsl:param name="rewrite_predicates" select="true()"/>

  <xsl:output method="xml" encoding="utf-8" standalone="yes"/>

  <xsl:key name="assocs" 
            match="tl:builtin-predicate[@name='association' or @name='association-role']/tl:*[1][local-name(.) = 'variable']" 
            use="@name"/>

  <xsl:key name="roles" 
            match="tl:builtin-predicate[@name='association-role']/tl:*[2][local-name(.) = 'variable']|tl:builtin-predicate[@name='role-player']/tl:*[1][local-name(.) = 'variable']" 
            use="@name"/>

  <xsl:key name="occs" 
            match="tl:builtin-predicate[@name='occurrence']/tl:*[2][local-name(.) = 'variable']"
            use="@name"/>

  <xsl:key name="names" 
            match="tl:builtin-predicate[@name='topic-name']/tl:*[2][local-name(.) = 'variable']|tl:builtin-predicate[@name='variant']/tl:*[1][local-name(.) = 'variable']"
            use="@name"/>

  <xsl:key name="variants"
            match="tl:builtin-predicate[@name='variant']/tl:*[2][local-name(.) = 'variable']"
            use="@name"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type' 
                                            or @name='scope' 
                                            or @name='value'
                                            or @name='value-like'
                                            or @name='datatype'
                                            or @name='resource'][tl:*[1][local-name(.)='variable']]">
    <xsl:call-template name="annotate"/>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='reifies'][tl:*[2][local-name(.)='variable']]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="index" select="2"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="annotate">
    <xsl:param name="index" select="1"/>
    <xsl:variable name="key" select="tl:*[$index][local-name(.) = 'variable']/@name"/>
    <xsl:variable name="is_association" select="count(key('assocs', $key)) > 0"/>
    <xsl:variable name="is_role" select="count(key('roles', $key)) > 0"/>
    <xsl:variable name="is_occurrence" select="count(key('occs', $key)) > 0"/>
    <xsl:variable name="is_name" select="count(key('names', $key)) > 0"/>
    <xsl:variable name="is_variant" select="count(key('variants', $key)) > 0"/>
    <xsl:variable name="hint">
      <xsl:choose>
        <xsl:when test="$rewrite_predicates and $is_association and not($is_role or $is_occurrence or $is_name or $is_variant)"><xsl:value-of select="'association'"/></xsl:when>
        <xsl:when test="$rewrite_predicates and $is_role and not($is_association or $is_occurrence or $is_name or $is_variant)"><xsl:value-of select="'role'"/></xsl:when>
        <xsl:when test="$rewrite_predicates and $is_occurrence and not($is_association or $is_role or $is_name or $is_variant)"><xsl:value-of select="'occurrence'"/></xsl:when>
        <xsl:when test="$rewrite_predicates and $is_name and not($is_association or $is_role or $is_occurrence or $is_variant)"><xsl:value-of select="'name'"/></xsl:when>
        <xsl:when test="$rewrite_predicates and $is_variant and not($is_association or $is_role or $is_occurrence or $is_name)"><xsl:value-of select="'variant'"/></xsl:when>
        <xsl:otherwise><xsl:value-of select="''"/></xsl:otherwise>
      </xsl:choose>
    </xsl:variable>
    <builtin-predicate>
      <xsl:copy-of select="@*"/>
      <xsl:choose>
          <xsl:when test="$hint = ''">
            <!-- Specialization isn't possible, annotate the predicate -->
            <xsl:if test="$is_association">
              <xsl:attribute name="association"><xsl:text>true</xsl:text></xsl:attribute>
            </xsl:if>
            <xsl:if test="$is_role">
              <xsl:attribute name="role"><xsl:text>true</xsl:text></xsl:attribute>
            </xsl:if>
            <xsl:if test="$is_occurrence">
              <xsl:attribute name="occurrence"><xsl:text>true</xsl:text></xsl:attribute>
            </xsl:if>
            <xsl:if test="$is_name">
              <xsl:attribute name="topic-name"><xsl:text>true</xsl:text></xsl:attribute>
            </xsl:if>
            <xsl:if test="$is_variant">
              <xsl:attribute name="variant"><xsl:text>true</xsl:text></xsl:attribute>
            </xsl:if>
          </xsl:when>
          <xsl:otherwise>
              <xsl:attribute name="hint"><xsl:value-of select="$hint"/></xsl:attribute>
          </xsl:otherwise>
        </xsl:choose>
      <xsl:copy-of select="*"/>
    </builtin-predicate>
  </xsl:template>

</xsl:stylesheet>
