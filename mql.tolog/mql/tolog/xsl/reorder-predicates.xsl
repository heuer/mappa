<?xml version="1.0" encoding="utf-8"?>
<!--
  Reorder predicates by the "cost" attribute.

  Copyright (c) 2010 - 2012, Semagia - Lars Heuer <http://www.semagia.com/>
  All rights reserved.
  
  License: BSD
-->
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:tl="http://psi.semagia.com/tolog-xml/"
                xmlns="http://psi.semagia.com/tolog-xml/"
                exclude-result-prefixes="tl">

  <xsl:output method="xml" encoding="utf-8"/>

  <xsl:template match="tl:*">
    <xsl:element name="{name()}">
      <xsl:copy-of select="@*"/>
      <xsl:for-each select="*">
        <xsl:sort select="@cost" data-type="number"/>
        <xsl:apply-templates select="."/> 
      </xsl:for-each>
    </xsl:element>
  </xsl:template>
    
</xsl:stylesheet>
