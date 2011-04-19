<?xml version="1.0" encoding="utf-8"?>
<!--


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

  <xsl:variable name="INFINITE_RESULT" select="10000"/>
  <xsl:variable name="WHOLE_TM_RESULT" select="1000"/>
  <xsl:variable name="BIG_RESULT"      select="100"/>
  <xsl:variable name="MEDIUM_RESULT"   select="10"/>
  <xsl:variable name="SMALL_RESULT"    select="3"/>
  <xsl:variable name="SINGLE_RESULT"   select="1"/>
  <xsl:variable name="FILTER_RESULT"   select="0"/>
  <xsl:variable name="FAIL_RESULT"     select="-1"/>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='base-locator'
                                            or @name='topic-map']">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='base-locator'
                                            or @name='topic-map'][count(tl:variable)=0]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='association'
                                            or @name='topic']">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='association'
                                            or @name='topic'][count(tl:variable)=0]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$INFINITE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[count(tl:variable)=0]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=0]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$SINGLE_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=1]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$FILTER_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:infix-predicate[@name='eq'][count(tl:variable)=2]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:occurrence-predicate">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$BIG_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:occurrence-predicate[count(tl:variable)=2]">
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost" select="$WHOLE_TM_RESULT"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:association-predicate">
    <xsl:variable name="pair-count" select="count(tl:pair)*2"/>
    <xsl:variable name="bound" select="count(tl:pair/tl:*/tl:*[local-name(.) != 'variable'])"/>
    <xsl:call-template name="annotate">
      <xsl:with-param name="cost">
        <xsl:choose>
          <xsl:when test="$bound = $pair-count"><xsl:value-of select="$FILTER_RESULT"/></xsl:when>
          <xsl:otherwise>
            <xsl:choose>
              <xsl:when test="$bound = 0"><xsl:value-of select="$BIG_RESULT"/></xsl:when>
              <xsl:otherwise><xsl:value-of select="$MEDIUM_RESULT - $bound"/></xsl:otherwise>
            </xsl:choose>
          </xsl:otherwise>
        </xsl:choose>
       </xsl:with-param>
    </xsl:call-template>
  </xsl:template>


  <xsl:template name="annotate">
    <xsl:param name="cost"/>
    <xsl:element name="{name(.)}">
      <xsl:copy-of select="@*"/>
      <xsl:attribute name="cost" select="$cost"/>
      <xsl:copy-of select="*"/>
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
