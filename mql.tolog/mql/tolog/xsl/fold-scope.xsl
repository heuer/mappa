<?xml version="1.0" encoding="utf-8"?>
<!--
  Stylesheet to convert several "scope($scoped, theme)" predicates into a
  a single "themes($scoped, theme1, theme2, ...)" predicate.
  
  I.e.:
  
    Input:
      scope($occ, theme1), scope($occ, theme2)

    Output:
      themes($occ, theme1, theme2)

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

  <!-- Index of all scope predicates which share the same "scoped" variable -->
  <xsl:key name="scopes" 
            match="tl:builtin-predicate[@name='scope'][tl:*[1][local-name(.)='variable']]"
            use="."/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='scope']">
    <!--** Merges 2 .. n scope predicates about the same scoped statement into one scope predicate -->
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:variable name="scope" select="key('scopes', .)[generate-id(..)=$parent]"/>
    <xsl:choose>
      <!--@ When we have more than one scope predicate about the same scoped statment -->
      <xsl:when test="count($scope) > 1">
        <xsl:if test="generate-id(.) = generate-id($scope[1])">
          <!--@ Create the predicate that unifies all scope($scoped, theme1), scope($scoped, theme2)... predicates -->
          <builtin-predicate>
            <!--@ Copy all attributes into the new predicate -->
            <xsl:apply-templates select="@*"/>
            <xsl:copy-of select="$scope/@*"/>
            <!--@ Rename predicate into "themes" -->
            <xsl:attribute name="name">themes</xsl:attribute>
            <!--@ Add the first parameter (a variable) to the parameter list -->
            <xsl:copy-of select="tl:*[1]"/>
            <!--@ Copy the themes into the predicate -->
            <xsl:copy-of select="$scope/tl:*[2]"/>
          </builtin-predicate>
        </xsl:if>
      </xsl:when>
      <xsl:otherwise>
        <!--@ If there is just one scope predicate, let it pass through unchanged. -->
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
