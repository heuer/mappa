<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet converts clause queries into select queries and renames
  the "source-locator" predicate into "item-identifier"

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

  <xsl:variable name="MOD_EXPERIMENTAL" select="'http://psi.ontopia.net/tolog/experimental/'"/>

  <xsl:key name="modns"
           match="tl:namespace[@kind='module']"
           use="@identifier"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:tolog[not(tl:select)]
                               [not(tl:insert)]
                               [not(tl:merge)]
                               [not(tl:update)]
                               [not(tl:delete)]">
    <!--** Converts a clause query (a query without a select statement) into a select query. -->
    <tolog>
      <xsl:apply-templates select="tl:base"/>
      <xsl:apply-templates select="tl:namespace"/>
      <xsl:apply-templates select="tl:rule"/>
      <select>
        <xsl:for-each select="descendant::tl:*[not(ancestor-or-self::tl:rule)]/tl:variable[not(@name=preceding::tl:variable/@name)]">
          <xsl:copy-of select="."/>
        </xsl:for-each>
        <where>
          <xsl:apply-templates select="tl:*[local-name(.) != 'base']
                                           [local-name(.) != 'namespace']
                                           [local-name(.) != 'rule']"/>
        </where>
      </select>
    </tolog>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@kind='module']]">
    <xsl:variable name="iri" select="key('modns', tl:name/tl:qname/@prefix)/@iri"/>
      <xsl:choose>
        <xsl:when test="$iri=$MOD_EXPERIMENTAL"><xsl:apply-templates select="." mode="module-experimental"/></xsl:when>
        <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
      </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:qname[@localpart='gt'
                                                     or @localpart='lt'
                                                     or @localpart='gteq'
                                                     or @localpart='lteq']]" mode="module-experimental">
    <xsl:variable name="lp" select="tl:name/tl:qname/@localpart"/>
    <xsl:element name="infix-predicate">
      <xsl:attribute name="name">
        <xsl:choose>
            <xsl:when test="$lp='gteq'"><xsl:text>ge</xsl:text></xsl:when>
            <xsl:when test="$lp='lteq'"><xsl:text>le</xsl:text></xsl:when>
            <xsl:otherwise><xsl:value-of select="tl:name/tl:qname/@localpart"/></xsl:otherwise>
        </xsl:choose>
      </xsl:attribute>
      <xsl:apply-templates select="@*|node()[local-name(.) != 'name']"/>
    </xsl:element>
  </xsl:template>

  <xsl:template match="@*|node()" mode="module-experimental">
    <xsl:copy-of select="."/>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='source-locator']">
    <!--** Converts a source-locator predicate into an item-identifier predicate -->
    <builtin-predicate name="item-identifier">
      <xsl:apply-templates/>
    </builtin-predicate>
  </xsl:template>

</xsl:stylesheet>
