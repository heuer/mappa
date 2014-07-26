<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet tries to create dynamic occurrences.

  Input:
    
    occurrence($A, $O), type($O, homepage), value($O, $VALUE)

  Output:
  
    homepage($A, $VALUE)


  CAUTION: This needs more work/tests.


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

  <xsl:key name="stmts1" 
            match="tl:builtin-predicate[@name='occurrence'
                                        or @name='topic-name'
                                        or @name='association-role'][tl:*[2][local-name(.) = 'variable']]"
            use="tl:*[2]/@name"/>

  <xsl:key name="stmts2" 
            match="tl:builtin-predicate[@name='association'
                                        or @name='role-player'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="types" 
            match="tl:builtin-predicate[@name='type'][tl:*[2][local-name(.) != 'variable']][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="values"
            match="tl:builtin-predicate[@name='value'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="variables"
           match="tl:select/tl:variable
                  |tl:insert/tl:fragment/tl:variable
                  |tl:update/tl:function/tl:variable
                  |tl:delete/tl:variable
                  |tl:merge/tl:variable"
           use="@name"/>


  <!-- Indicates if this optimization is allowed (only if a where clause is available) -->
  <xsl:variable name="allowed" select="count(/tl:tolog/tl:*/tl:where)=1"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='occurrence'][tl:*[2][local-name(.)='variable']]">
    <xsl:choose>
      <xsl:when test="$allowed">
        <xsl:variable name="parent" select="generate-id(..)"/>
        <xsl:variable name="key" select="tl:*[2]/@name"/>
        <xsl:variable name="types" select="key('types', $key)[generate-id(..)=$parent]"/>
        <xsl:variable name="values" select="key('values', $key)[generate-id(..)=$parent]"/>
        <xsl:variable name="variables" select="key('variables', $key)"/>
        <xsl:choose>
          <xsl:when test="count($types) = 1 and count($values) = 1 and count($variables) = 0">
            <dynamic-predicate>
              <name>
                <xsl:copy-of select="$types/tl:*[2]"/>
              </name>
              <xsl:copy-of select="tl:*[1]"/>
              <xsl:copy-of select="$values/tl:*[2]"/>
            </dynamic-predicate>
          </xsl:when>
          <xsl:otherwise>
            <xsl:copy-of select="."/>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type'
                                            or @name='value'][tl:*[1][local-name(.)='variable']]">
    <xsl:choose>
      <xsl:when test="$allowed">
        <xsl:variable name="parent" select="generate-id(..)"/>
        <xsl:variable name="key" select="tl:*[1]/@name"/>
        <xsl:variable name="stmts" select="key('stmts1', $key)[generate-id(..)=$parent]|key('stmts2', $key)[generate-id(..)=$parent]"/>
        <xsl:variable name="types" select="key('types', $key)[generate-id(..)=$parent]"/>
        <xsl:variable name="values" select="key('values', $key)[generate-id(..)=$parent]"/>
        <xsl:variable name="variables" select="key('variables', $key)"/>
        <xsl:if test="count($stmts) > 1 or count($types) + count($values) + count($variables) != 2">
          <xsl:copy-of select="."/>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
