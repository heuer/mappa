<?xml version="1.0" encoding="utf-8"?>
<!--
  Merges role-player($x, x), type($x, z) into role-player($x, x, z) and
  occurrence(t, $x), type($x, z) into occurrence(t, $x, z)
  and topic-name(t, $x), type($x, z) into topic-name(t, $x, z)

  TODO: association($a), type($a, t) into association($a, t)

  
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

  <xsl:key name="stmts" 
            match="tl:builtin-predicate[@name='topic-name'
                                        or @name='occurrence'][tl:*[1][local-name(.) != 'variable']][tl:*[2][local-name(.) = 'variable']]"
            use="tl:*[2]/@name"/>

  <xsl:key name="role-player" 
            match="tl:builtin-predicate[@name='role-player'][tl:*[1][local-name(.) = 'variable']][tl:*[2][local-name(.) != 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="type" 
            match="tl:builtin-predicate[@name='type'][tl:*[1][local-name(.) = 'variable']][tl:*[2][local-name(.) != 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='role-player'][tl:*[1][local-name(.)='variable']][tl:*[2][local-name(.) != 'variable']]">
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:call-template name="enhance"><xsl:with-param name="types" select="key('type', tl:*[1]/@name)[generate-id(..)=$parent]"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='topic-name'
                                            or @name='occurrence'][tl:*[1][local-name(.)!='variable']][tl:*[2][local-name(.) = 'variable']]">
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:call-template name="enhance"><xsl:with-param name="types" select="key('type', tl:*[2]/@name)[generate-id(..)=$parent]"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='type'][tl:*[1][local-name(.) = 'variable']][tl:*[2][local-name(.) != 'variable']]">
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:if test="count(key('role-player', tl:*[1]/@name)[generate-id(..)=$parent]|key('stmts', tl:*[1]/@name)[generate-id(..)=$parent]) != 1">
        <xsl:copy-of select="."/>
    </xsl:if>
  </xsl:template>

  <xsl:template name="enhance">
    <xsl:param name="types"/>
    <xsl:choose>
      <xsl:when test="count($types)=1">
        <builtin-predicate>
          <xsl:copy-of select="@*"/>
          <xsl:copy-of select="*"/>
          <xsl:copy-of select="$types/tl:*[2]"/>
        </builtin-predicate>
      </xsl:when> 
      <xsl:otherwise>
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose> 
  </xsl:template>

</xsl:stylesheet>
