<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet tries to create dynamic occurrences.

  Input:
    
    occurrence($A, $O), type($O, homepage), value($O, $VALUE)

  Output:
  
    homepage($A, $VALUE)


  CAUTION: This needs more work/tests. Queries like


    select $O from occurrence($A, $O), type($O, homepage), value($O, $VALUE)?
    
  will fail because the query becomes:
  
    select $O from homepage($A, $VALUE)


  Copyright (c) 2010 - 2011, Semagia - Lars Heuer <http://www.semagia.com/>
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


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='occurrence'][tl:*[2][local-name(.)='variable']]">
    <xsl:variable name="parent" select=".."/>
    <xsl:variable name="key" select="tl:*[2]/@name"/>
    <xsl:variable name="types" select="key('types', $key)[..=$parent]"/>
    <xsl:variable name="values" select="key('values', $key)[..=$parent]"/>
    <xsl:choose>
      <xsl:when test="count($types) = 1 and count($values) = 1">
        <occurrence-predicate>
          <name>
            <xsl:copy-of select="$types/tl:*[2]"/>
          </name>
          <xsl:copy-of select="tl:*[1]"/>
          <xsl:copy-of select="$values/tl:*[2]"/>
        </occurrence-predicate>
      </xsl:when>
      <xsl:otherwise>
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type'
                                            or @name='value'][tl:*[1][local-name(.)='variable']]">
    <xsl:variable name="parent" select=".."/>
    <xsl:variable name="key" select="tl:*[1]/@name"/>
    <xsl:variable name="stmts" select="key('stmts1', $key)[..=$parent]|key('stmts2', $key)[..=$parent]"/>
    <xsl:variable name="types" select="key('types', $key)[..=$parent]"/>
    <xsl:variable name="values" select="key('values', $key)[..=$parent]"/>
    <xsl:if test="count($stmts) > 1 or count($types) + count($values) != 2">
      <xsl:copy-of select="."/>       
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
