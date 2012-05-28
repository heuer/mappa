<?xml version="1.0" encoding="utf-8"?>
<!--

  This stylesheet eliminates unused variables and introduces internal,
  non-standard tolog predicates.


  Copyright (c) 2010 - 2012, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                exclude-result-prefixes="tl">

  <xsl:output method="xml" encoding="utf-8" standalone="yes"/>

  <xsl:key name="select-variables"
             match="tl:select/tl:*[local-name(.) = 'variable' or local-name(.) = 'count']"
             use="@name"/>

  <xsl:key name="where-variables"
             match="tl:where//tl:variable"
             use="@name"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='instance-of' or @name='direct-instance-of'][local-name(*[1]) = 'variable']">
    <!--** Replaces (direct-)instance-of($instance, $type) with (direct-)types($type) if the $instance variable is unused -->
    <xsl:variable name="instance-var" select="tl:variable[1]/@name"/>
    <xsl:choose>
      <xsl:when test="count(key('select-variables', $instance-var)) = 0 and count(key('where-variables', $instance-var)) = 1">
        <builtin-predicate kind="internal">
            <xsl:copy-of select="@*"/>
            <xsl:attribute name="name"><xsl:value-of select="concat(substring-before(@name, 'instance-of'), 'types')"/></xsl:attribute>
            <xsl:copy-of select="tl:*[2]"/>
        </builtin-predicate>  
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

</xsl:stylesheet>
