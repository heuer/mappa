<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet eliminates unused variables and introduces internal,
  non-standard tolog predicates.


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

  <xsl:key name="query-variables"
             match="tl:*[local-name() = 'select'
                         or local-name() = 'delete'
                         or local-name() = 'merge'
                         or local-name() = 'insert'
                         or local-name() = 'update']/tl:*[local-name(.) = 'variable' or local-name(.) = 'count']"
             use="@name"/>
    
  <xsl:key name="where-variables"
             match="tl:where//tl:variable"
             use="@name"/>

  <xsl:key name="eq-predicates"
             match="tl:infix-predicate[@name='eq'][count(tl:variable)=1]"
             use="tl:variable/@name"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='instance-of' or @name='direct-instance-of'][local-name(*[1]) = 'variable']">
    <!--** Replaces (direct-)instance-of($instance, $type) with (direct-)types($type) if the $instance variable is unused -->
    <xsl:variable name="instance-var" select="tl:variable[1]/@name"/>
    <xsl:choose>
      <xsl:when test="count(key('query-variables', $instance-var)) = 0 and count(key('where-variables', $instance-var)) = 1">
        <internal-predicate>
            <xsl:copy-of select="@*"/>
            <xsl:attribute name="name"><xsl:value-of select="concat(substring-before(@name, 'instance-of'), 'types')"/></xsl:attribute>
            <xsl:attribute name="removed-variables"><xsl:value-of select="$instance-var"/></xsl:attribute>
            <xsl:apply-templates select="tl:*[2]"/>
        </internal-predicate>
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>


<!--
  <xsl:template match="tl:variable">
    <!-** Replaces variables with a constant if an equals predicate exists: born-in($t, $city), $city = Bremen ==> born-in($t, Bremen) ->
    <xsl:variable name="eq-predicate" select="key('eq-predicates', @name)"/>
    <xsl:choose>
      <xsl:when test="$eq-predicate and count($eq-predicate) = 1 and generate-id(..) != generate-id($eq-predicate)">
        <xsl:copy-of select="$eq-predicate/tl:*[local-name() != 'variable']"/>
      </xsl:when>
      <xsl:otherwise><xsl:copy-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>
    
  <xsl:template match="tl:infix-predicate[@name='eq']
                                         [count(tl:variable) = 1]">
    <!-** Ignores those equals predicates where the constant part became part of the other predicates ->
    <xsl:variable name="var-name" select="tl:variable/@name"/>
    <xsl:variable name="eq-predicate" select="key('eq-predicates', $var-name)"/>
    <xsl:if test="count($eq-predicate) != 1 
                    or count(key('where-variables', $var-name)) = 1 
                    or generate-id(.) != generate-id($eq-predicate)">
      <xsl:copy-of select="."/>
    </xsl:if>
  </xsl:template>
-->

</xsl:stylesheet>
