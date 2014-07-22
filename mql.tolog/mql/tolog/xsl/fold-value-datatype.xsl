<?xml version="1.0" encoding="utf-8"?>
<!--
  Merges value($datatype-aware, "value"), datatype($datatype-aware, "http://datatype") into
  a single literal($datatype-aware, "value", "http://datatype") predicate.
  Further, value-like($dt, "value"), datatype($dt, "http://...") is merged into 
  literal-like($dt, "value", "http://...").
  
  If the result is a literal-like predicate, the '-like' part references the value, not the datatype.

    Input:
      value($occ, "Semagia"), datatype($occ, "http://www.w3.org/2001/XMLSchema#string")

    Output:
      literal($occ, "Semagia", "http://www.w3.org/2001/XMLSchema#string")

  
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

  <xsl:key name="values" 
            match="tl:builtin-predicate[@name='value' or @name='value-like'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>

  <xsl:key name="datatypes" 
            match="tl:builtin-predicate[@name='datatype'][tl:*[1][local-name(.) = 'variable']]"
            use="tl:*[1]/@name"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='value' or @name='value-like'][tl:*[1][local-name(.)='variable']]">
    <!--** Matches all value(-like) predicates which contain a variable 
           at the first position (the object part) 
    -->
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:variable name="datatype-pred" select="key('datatypes', tl:*[1]/@name)[generate-id(..)=$parent]"/>
    <xsl:choose>
      <xsl:when test="count($datatype-pred) = 1">
        <!--@ Check if a corresponding datatype predicate exists -->
        <xsl:element name="builtin-predicate">
          <!--@ datatype predicate exists, create the new literal(-like) predicate -->
          <xsl:apply-templates select="@*"/>
          <xsl:attribute name="name">
            <xsl:value-of select="concat('literal', substring-after(@name, 'value'))"/>
          </xsl:attribute>
          <xsl:copy-of select="tl:*"/>
          <xsl:copy-of select="$datatype-pred/tl:*[2]"/>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <!--@ datatype predicate does not exist, leave the value(-like) predicate unchanged -->
        <xsl:copy-of select="."/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="tl:builtin-predicate[@name='datatype'][tl:*[1][local-name(.)='variable']]">
    <!--** Matches all datatype predicates which start with a variable -->
    <xsl:variable name="parent" select="generate-id(..)"/>
    <xsl:if test="not(key('values', tl:*[1]/@name)[generate-id(..)=$parent])">
      <!--@ If this predicate has been folded into a literal(-like) predicate, omit it, 
            otherwise it is kept unchanged.
      -->
      <xsl:copy-of select="."/>
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>
