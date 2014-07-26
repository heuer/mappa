<?xml version="1.0" encoding="utf-8"?>
<!--
  Inlines rule bodies into the queries, iff the rule body does not include a predicate 
  invocation (only builtin-predicates, and (dynamic) occurrence and (dynamic) association
  predicates are allowed).

  CAUTION: This needs more work/tests.

  Copyright (c) 2010 - 2014, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                xmlns:exsl="http://exslt.org/common"
                extension-element-prefixes="exsl"
                exclude-result-prefixes="tl">

  <xsl:output method="xml" encoding="utf-8" standalone="yes"/>

  <!-- Index for all rules which have no predicate invocations -->
  <xsl:key name="rules"
           match="tl:rule[count(tl:body//tl:predicate) = 0]"
           use="@name"/>

  <!-- Indicates the query has a where clause, otherwise this stylesheet would 
       introduce bindings the user hasn't asked for -->
  <xsl:variable name="allowed" select="count(/tl:tolog/tl:*/tl:where)=1"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:rule[key('rules', @name)]">
    <!--** Removes those rules from the query which are inlined -->
    <xsl:if test="not($allowed)"><xsl:copy-of select="."/></xsl:if>
  </xsl:template>

  <xsl:template match="tl:predicate[tl:name/tl:identifier]">
    <!--** Replaces rule invocations with the content of the rule body if possible -->
    <xsl:variable name="rule" select="key('rules', tl:name/tl:identifier/@value)"/>
    <xsl:choose>
      <xsl:when test="$allowed and $rule">
        <xsl:variable name="pred-args" select="tl:*[local-name(.)!='name']"/>
        <xsl:variable name="rule2arg">
          <xsl:for-each select="$rule/tl:variable">
            <xsl:variable name="pos" select="position()"/>
            <entry key="{@name}"><xsl:copy-of select="$pred-args[$pos]"/></entry>
          </xsl:for-each>
        </xsl:variable>
        <xsl:apply-templates select="$rule/tl:body/tl:*" mode="variable-replacement">
          <xsl:with-param name="map" select="exsl:node-set($rule2arg)"/>
        </xsl:apply-templates>
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="@*|node()" mode="variable-replacement">
    <xsl:param name="map"/>
    <xsl:copy>
      <xsl:apply-templates select="@*|node()" mode="variable-replacement">
        <xsl:with-param name="map" select="$map"/>
      </xsl:apply-templates>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:variable" mode="variable-replacement">
    <xsl:param name="map"/>
    <xsl:variable name="arg" select="$map/*[@key=current()/@name]/*"/>
    <xsl:choose>
      <xsl:when test="$arg"><xsl:copy-of select="$arg"/></xsl:when>
      <xsl:otherwise><variable name="{concat('__inlined__', @name)}"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
