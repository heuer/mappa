<?xml version="1.0" encoding="utf-8"?>
<!--

  Removes redundant predicates
    
    
    Input:
      topic($t), topic-name($t, $n)

    Output:
      topic-name($t, $n)

  Supported predicates:
  * topic
  * association
  
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

  <xsl:key name="topic" 
            match="tl:builtin-predicate[@name='subject-identifier'
                                        or @name='subject-locator'
                                        or @name='topic-name'
                                        or @name='occurrence'
                                        or @name='reifies'
                                        or @name='direct-instance-of'
                                        or @name='instance-of'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="topic2" 
            match="tl:builtin-predicate[@name='type'
                                        or @name='role-player'
                                        or @name='scope'
                                        or @name='direct-instance-of'
                                        or @name='instance-of'][tl:*[2][local-name(.) = 'variable']]"
            use="tl:*[2]/@name"/>

  <xsl:key name="association" 
            match="tl:builtin-predicate[@name='association-role'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='topic'][tl:*[1][local-name(.)='variable']]">
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:variable name="key" select="tl:*[1]/@name"/>
    <xsl:variable name="want-it" select="count(key('topic', $key)[generate-id(..)=$parent]|key('topic2', $key)[generate-id(..)=$parent]) = 0"/>
    <xsl:if test="$want-it">
        <xsl:copy-of select="."/>
    </xsl:if>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='association'][tl:*[1][local-name(.)='variable']]">
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:if test="count(key(@name, tl:*[1]/@name)[generate-id(..)=$parent]) = 0">
        <xsl:copy-of select="."/>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
