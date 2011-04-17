<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet converts clause queries into select queries.

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

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:query[not(tl:select)]
                               [not(tl:insert)]
                               [not(tl:merge)]
                               [not(tl:update)]
                               [not(tl:delete)]">
    <!--** Converts a clause query (a query without a select statement) into a select query. -->
    <query>
      <xsl:apply-templates select="tl:rule"/>
      <select>
        <xsl:for-each select="descendant::tl:*[local-name(.) != 'rule']/tl:variable[not(@name=preceding::tl:variable/@name)]">
          <xsl:copy-of select="."/>
        </xsl:for-each>
        <where>
          <xsl:apply-templates select="tl:*[local-name(.) != 'rule']"/>
        </where>
      </select>
    </query>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='source-locator']">
    <!--** Converts a source-locator predicate into an item-identifier predicate -->
    <builtin-predicate name="item-identifier">
      <xsl:apply-templates/>
    </builtin-predicate>
  </xsl:template>

</xsl:stylesheet>
