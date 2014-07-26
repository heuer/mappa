<?xml version="1.0" encoding="utf-8"?>
<!--
  This stylesheet translates a tolog XML representation back to a tolog
  query string.

  Copyright (c) 2010 - 2014, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns:str="http://exslt.org/strings"
                extension-element-prefixes="str">

  <xsl:output method="text"/>

  <xsl:param name="tolog-plus" select="false()"/>
  <xsl:param name="render-hints" select="false()"/>

  <xsl:template match="*">
    <xsl:apply-templates select="tl:base|tl:namespace|tl:x-directive"/>
    <xsl:if test="count(tl:base|tl:namespace|tl:x-directive) > 0"><xsl:text>&#xA;</xsl:text></xsl:if>
    <xsl:apply-templates select="tl:rule"/>
    <xsl:choose>
      <xsl:when test="tl:select|tl:merge|tl:delete|tl:update|tl:insert">
        <xsl:apply-templates select="tl:select|tl:merge|tl:delete|tl:update|tl:insert"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:call-template name="predicates">
        <xsl:with-param name="items" select="tl:*[local-name(.) != 'orderby' 
                                                  and local-name(.) != 'namespace' 
                                                  and local-name(.) != 'pagination' 
                                                  and local-name(.) != 'rule' 
                                                  and local-name(.) != 'base'
                                                  and local-name(.) != 'x-directive']"/>
          <xsl:with-param name="indent" select="false()"/>
        </xsl:call-template>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:apply-templates select="tl:*/tl:orderby|tl:orderby"/>
    <xsl:apply-templates select="tl:*/tl:pagination|tl:pagination"/>
    <xsl:if test="$tolog-plus = 'false' and not(tl:merge|tl:delete|tl:update|tl:insert)"><xsl:text>?</xsl:text></xsl:if>
    <xsl:text>&#xA;</xsl:text>
  </xsl:template>

  <xsl:template match="tl:create|tl:drop|tl:load">
    <xsl:value-of select="concat(local-name(.), '&#xA;    ')"/>
    <xsl:apply-templates select="*"/>
  </xsl:template>

  <xsl:template match="tl:into|tl:from">
      <xsl:value-of select="concat('&#xA;', local-name(.), '&#xA;    ')"/>
      <xsl:call-template name="parameters">
          <xsl:with-param name="items" select="*"/>
      </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:select|tl:merge|tl:delete|tl:update">
    <xsl:value-of select="concat(local-name(.), '&#xA;    ')"/>
    <xsl:call-template name="predicates">
        <xsl:with-param name="items" select="tl:*[local-name(.) != 'from'
                                                    and local-name(.) != 'into'
                                                    and local-name(.) != 'where' 
                                                    and local-name(.) != 'orderby' 
                                                    and local-name(.) != 'namespace' 
                                                    and local-name(.) != 'pagination']"/>
        <xsl:with-param name="nl" select="local-name(.) != 'select' and local-name(.) != 'merge'"/>
    </xsl:call-template>
    <xsl:apply-templates select="tl:into|tl:from"/>
    <xsl:apply-templates select="tl:where"/>
  </xsl:template>

  <xsl:template match="tl:insert">
    <xsl:text>insert&#xA;    </xsl:text>
  <xsl:value-of select="tl:fragment/tl:content"/>
  <xsl:apply-templates select="tl:into"/>
  <xsl:apply-templates select="tl:where"/>
  </xsl:template>

  <xsl:template match="tl:namespace[@kind!='module']">
    <xsl:choose>
      <xsl:when test="$tolog-plus = 'true'">
        <xsl:value-of select="concat('%prefix ', @identifier, ' &lt;', @iri,'&gt;&#xA;')"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="concat('using ', @identifier, ' for ')"/>
        <xsl:if test="@kind='subjectidentifier'"><xsl:text>i</xsl:text></xsl:if>
        <xsl:if test="@kind='subjectlocator'"><xsl:text>a</xsl:text></xsl:if>
        <xsl:if test="@kind='itemidentifier'"><xsl:text>s</xsl:text></xsl:if>
        <xsl:value-of select="concat('&quot;', @iri, '&quot;&#xA;')"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:namespace[@kind='module']">
    <xsl:if test="$tolog-plus = 'true'">%</xsl:if>
    <xsl:text>import </xsl:text>
    <xsl:if test="$tolog-plus = 'false'">
      <xsl:call-template name="iri"><xsl:with-param name="iri" select="@iri"/></xsl:call-template>
      <xsl:text> as </xsl:text>
    </xsl:if>
    <xsl:value-of select="@identifier"/>
    <xsl:if test="$tolog-plus = 'true'">
      <xsl:text> </xsl:text>
      <xsl:call-template name="iri"><xsl:with-param name="iri" select="@iri"/></xsl:call-template>
    </xsl:if>
    <xsl:text>&#xA;</xsl:text>
  </xsl:template>

  <xsl:template match="tl:namespace[not(@kind)]">
    <xsl:value-of select="concat('%prefix ', @identifier, ' &lt;', @iri,'&gt;&#xA;')"/>
  </xsl:template>
    
  <xsl:template match="tl:base">
    <xsl:text>%base </xsl:text>
    <xsl:call-template name="iri"><xsl:with-param name="iri" select="@iri"/></xsl:call-template>
    <xsl:text>&#xA;</xsl:text>
  </xsl:template>

  <xsl:template match="tl:x-directive">
    <xsl:value-of select="concat('%x-', @name, ' &lt;', @iri,'&gt;&#xA;')"/>
  </xsl:template>

  <xsl:template match="tl:where">
    <xsl:choose>
      <xsl:when test="$tolog-plus = 'true'"><xsl:text>&#xA;where&#xA;    </xsl:text></xsl:when>
      <xsl:otherwise><xsl:text>&#xA;from&#xA;    </xsl:text></xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="predicates">
      <xsl:with-param name="items" select="tl:*[local-name(.)!='orderby']"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:rule">
    <xsl:value-of select="concat(@name, '(')"/>
    <xsl:call-template name="parameters">
      <xsl:with-param name="items" select="tl:variable"/>
    </xsl:call-template>
    <xsl:text>) :-&#xA;    </xsl:text>
    <xsl:call-template name="predicates">
      <xsl:with-param name="items" select="tl:body/*"/>
    </xsl:call-template>
    <xsl:text>&#xA;.&#xA;&#xA;</xsl:text>
  </xsl:template>

  <xsl:template match="tl:association-predicate">
    <xsl:apply-templates select="tl:name/tl:*"/>
    <xsl:text>(</xsl:text>
    <xsl:for-each select="tl:pair">
      <xsl:apply-templates select="."/>
      <xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
    </xsl:for-each>
    <xsl:text>)</xsl:text>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate|tl:function|tl:internal-predicate">
    <xsl:if test="local-name(.) = 'internal-predicate'"><xsl:text>:</xsl:text></xsl:if>
    <xsl:value-of select="concat(@name, '(')"/>
    <xsl:call-template name="parameters">
      <xsl:with-param name="items" select="tl:*"/>
    </xsl:call-template>
    <xsl:text>)</xsl:text>
    <xsl:apply-templates select="." mode="annotate"/>
    <xsl:if test="$render-hints = 'true' and local-name(.) = 'internal-predicate'"><xsl:text>  /* optimizer */</xsl:text></xsl:if>
  </xsl:template>

  <xsl:template match="tl:predicate|tl:dynamic-predicate">
    <xsl:apply-templates select="tl:name/*"/>
    <xsl:text>(</xsl:text>
    <xsl:call-template name="parameters">
      <xsl:with-param name="items" select="tl:*[local-name() != 'name']"/>
    </xsl:call-template>
    <xsl:text>)</xsl:text>
  </xsl:template>
    
  <xsl:template match="tl:builtin-predicate[@hint]" mode="annotate">
    <xsl:if test="$render-hints = 'true'">
      <xsl:variable name="kind" select="@name"/>
      <xsl:text>  /* </xsl:text>
      <xsl:for-each select="str:split(@hint, ' ')">
        <xsl:choose>
            <xsl:when test="position() = last() and position() > 1"><xsl:text> and </xsl:text></xsl:when>
            <xsl:when test="position() != 1"><xsl:text>, </xsl:text></xsl:when>
        </xsl:choose>
        <xsl:value-of select="."/>
        <xsl:choose>
            <xsl:when test="position() != last()"><xsl:text>-</xsl:text></xsl:when>
            <xsl:otherwise><xsl:value-of select="concat('-', $kind)"/></xsl:otherwise>
        </xsl:choose>
      </xsl:for-each>
      <xsl:text> */ </xsl:text>
    </xsl:if>
  </xsl:template>

  <xsl:template match="tl:infix-predicate">
    <xsl:apply-templates select="tl:*[1]"/>
    <xsl:text> </xsl:text>
    <xsl:if test="@name='ne'"><xsl:text>/=</xsl:text></xsl:if>
    <xsl:if test="@name='eq'"><xsl:text>=</xsl:text></xsl:if>
    <xsl:if test="@name='lt'"><xsl:text>&lt;</xsl:text></xsl:if>
    <xsl:if test="@name='gt'"><xsl:text>&gt;</xsl:text></xsl:if>
    <xsl:if test="@name='le'"><xsl:text>&lt;=</xsl:text></xsl:if>
    <xsl:if test="@name='ge'"><xsl:text>&gt;=</xsl:text></xsl:if>
    <xsl:text> </xsl:text>
    <xsl:apply-templates select="tl:*[2]"/>
  </xsl:template>

  <xsl:template match="tl:not">
    <xsl:text>not(</xsl:text> 
    <xsl:call-template name="predicates">
        <xsl:with-param name="items" select="tl:*"/>
    </xsl:call-template>
    <xsl:text>)</xsl:text>  
  </xsl:template>

  <xsl:template match="tl:or">
    <xsl:text>{ </xsl:text>
      <xsl:for-each select="tl:branch">
        <xsl:if test="position() != 1">
          <xsl:text> </xsl:text>
          <xsl:choose>
            <xsl:when test="@short-circuit='true'"><xsl:text>||</xsl:text></xsl:when>
            <xsl:otherwise><xsl:text>|</xsl:text></xsl:otherwise>
          </xsl:choose>
          <xsl:text> </xsl:text>
        </xsl:if>
        <xsl:call-template name="predicates">
            <xsl:with-param name="items" select="tl:*"/>
        </xsl:call-template>
      </xsl:for-each>
    <xsl:text> }</xsl:text>
  </xsl:template>

  <xsl:template match="tl:pair">
    <xsl:choose>
      <xsl:when test="$tolog-plus = 'true'">
        <xsl:apply-templates select="tl:type/*"/>
        <xsl:text>: </xsl:text>
        <xsl:apply-templates select="tl:player/*"/>
      </xsl:when> 
      <xsl:otherwise>
        <xsl:apply-templates select="tl:player/*"/>
        <xsl:text>: </xsl:text>
        <xsl:apply-templates select="tl:type/*"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:orderby">
    <xsl:text>&#xA;order by </xsl:text>
    <xsl:call-template name="parameters">
      <xsl:with-param name="items" select="*"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:pagination">
    <xsl:text>&#xA;</xsl:text>
    <xsl:call-template name="parameters">
      <xsl:with-param name="items" select="*"/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:descending">
    <xsl:value-of select="concat('$', @name, ' desc')"/>
  </xsl:template>

  <xsl:template match="tl:limit|tl:offset">
     <xsl:value-of select="concat(local-name(.), ' ', @value)"/>
  </xsl:template>

  <xsl:template match="tl:variable|tl:ascending">
    <xsl:value-of select="concat('$', @name)"/>
  </xsl:template>

  <xsl:template match="tl:objectid">
    <xsl:value-of select="concat('@', @value)"/>
  </xsl:template>

  <xsl:template match="tl:parameter">
    <xsl:value-of select="concat('%', @name, '%')"/>
  </xsl:template>

  <xsl:template match="tl:string">
    <xsl:value-of select="concat('&quot;', @value, '&quot;')"/>
  </xsl:template>
  
  <xsl:template match="tl:iri">
    <xsl:call-template name="iri"><xsl:with-param name="iri" select="@value"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:integer|tl:decimal|tl:identifier">
    <xsl:value-of select="@value"/>
  </xsl:template>

  <xsl:template match="tl:curie|tl:qname">
    <xsl:if test="$tolog-plus = 'true' and @kind='item-identifier'">^ </xsl:if>
    <xsl:if test="$tolog-plus = 'true' and @kind='subject-locator'">= </xsl:if>
    <xsl:if test="local-name(.)='curie'">[</xsl:if>
    <xsl:value-of select="@prefix"/>
    <xsl:text>:</xsl:text>
    <xsl:value-of select="@localpart"/>
    <xsl:if test="local-name(.)='curie'">]</xsl:if>
  </xsl:template>

  <xsl:template match="tl:literal">
    <xsl:value-of select="concat('&quot;', @value, '&quot;^^')"/>
    <xsl:choose>
        <xsl:when test="@datatype-iri"><xsl:value-of select="concat('&lt;', @datatype-iri, '&gt;')"/></xsl:when>
        <xsl:otherwise><xsl:value-of select="concat(@datatype-prefix, ':', @datatype-localpart)"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:subjectidentifier">
    <xsl:if test="$tolog-plus != 'true'"><xsl:text>i</xsl:text></xsl:if>
    <xsl:call-template name="iri"><xsl:with-param name="iri" select="@value"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:subjectlocator">
    <xsl:choose>
      <xsl:when test="$tolog-plus = 'true'"><xsl:text>= </xsl:text></xsl:when>
      <xsl:otherwise><xsl:text>a</xsl:text></xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="iri"><xsl:with-param name="iri" select="@value"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:itemidentifier">
      <xsl:choose>
          <xsl:when test="$tolog-plus = 'true'"><xsl:text>^ </xsl:text></xsl:when>
          <xsl:otherwise><xsl:text>s</xsl:text></xsl:otherwise>
      </xsl:choose>
    <xsl:call-template name="iri"><xsl:with-param name="iri" select="@value"/></xsl:call-template>
  </xsl:template>

  <xsl:template match="tl:count">
    <xsl:value-of select="concat('count', '($', @name, ')')"/>
  </xsl:template>
  
  <xsl:template name="predicates">
    <xsl:param name="items"/>
    <xsl:param name="nl" select="true()"/>
    <xsl:param name="indent" select="true()"/>
    <xsl:for-each select="$items">
      <xsl:if test="$nl and position() != 1">
        <xsl:text>&#xA;</xsl:text>
        <xsl:if test="$indent"><xsl:text>    </xsl:text></xsl:if>
      </xsl:if>
       <xsl:apply-templates select="."/>
      <xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
      <xsl:if test="$render-hints = 'true' and @cost"><xsl:text> /* costs: </xsl:text><xsl:value-of select="@cost"/><xsl:text> */</xsl:text></xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="parameters">
    <xsl:param name="items"/>
    <xsl:for-each select="$items">
       <xsl:apply-templates select="."/>
      <xsl:if test="position() != last()"><xsl:text>, </xsl:text></xsl:if>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="iri">
    <xsl:param name="iri" select="."/>
    <xsl:choose>
      <xsl:when test="$tolog-plus = 'true'"><xsl:value-of select="concat('&lt;', $iri, '&gt;')"/></xsl:when>
      <xsl:otherwise><xsl:value-of select="concat('&quot;', $iri, '&quot;')"/></xsl:otherwise>
    </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>
