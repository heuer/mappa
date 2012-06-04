<?xml version="1.0" encoding="utf-8"?>
<!--

  This stylesheet replaces QNames, CURIES and topic identifiers with 
  IRIs.
  
  Experimental, needs more testing.

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

  <xsl:param name="base"/>

  <xsl:variable name="base-directive" select="tl:base/@iri"/>
    
  <xsl:key name="namespaces"
             match="tl:namespace[@kind!='module']"
             use="@identifier"/>


  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="tl:curie[@kind!='module']|tl:qname[@kind!='module']">
    <xsl:variable name="iri" select="key('namespaces', @prefix)/@iri"/>
    <xsl:element name="{@kind}">
      <xsl:attribute name="value"><xsl:value-of select="concat($iri, @localpart)"/></xsl:attribute>  
    </xsl:element>
  </xsl:template>

</xsl:stylesheet>
