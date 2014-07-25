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
      <builtin-predicate name="type" hint="association">
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
  * item-identifier

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

  <xsl:key name="topics"
            match="tl:builtin-predicate[@name='topic' or @name='topic-name' or @name='reifies' or @name='subject-identifier' or @name='subject-locator' or @name='occurrence' or @name='instance-of' or @name='direct-instance-of']/tl:*[1][local-name(.) = 'variable']
                   |tl:builtin-predicate[@name='type' or @name='scope' or @name='role-player' or @name='instance-of' or @name='direct-instance-of']/tl:*[2][local-name(.) = 'variable']"
            use="@name"/>

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
                                            or @name='resource'
                                            or @name='item-identifier'][tl:*[1][local-name(.)='variable']]">
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
    <xsl:variable name="hints">
        <association apply="{count(key('assocs', $key)) > 0}"/>
        <role apply="{count(key('roles', $key)) > 0}"/>
        <occurrence apply="{count(key('occs', $key)) > 0}"/>
        <name apply="{count(key('names', $key)) > 0}"/>
        <variant apply="{count(key('variants', $key)) > 0}"/>
        <topic apply="{count(key('topics', $key)) > 0}"/>
    </xsl:variable>
    <xsl:variable name="hint">
      <xsl:for-each select="exsl:node-set($hints)/tl:*[@apply='true']">
        <xsl:value-of select="local-name(.)"/>
        <xsl:if test="position() != last()"><xsl:text> </xsl:text></xsl:if>
      </xsl:for-each>
    </xsl:variable>
    
    <builtin-predicate>
      <xsl:copy-of select="@*"/>
      <xsl:if test="$hint != ''"><xsl:attribute name="hint"><xsl:value-of select="$hint"/></xsl:attribute></xsl:if>
      <xsl:copy-of select="*"/>
    </builtin-predicate>
  </xsl:template>

</xsl:stylesheet>
