<xsl:transform version="1.0"
 xmlns="http://www.w3.org/1999/xhtml"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:xhtml="http://www.w3.org/1999/xhtml"
 >

  <xsl:output
      method="xml"
      doctype-public="-//W3C//DTD XHTML 1.0 Transitional//EN"
      doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
      indent="no"
      encoding="UTF-8"
      />

  <xsl:template match="xhtml:p">
    <xsl:message terminate="no">foo</xsl:message>
    <xsl:copy>hello, test</xsl:copy>
  </xsl:template>

  <!-- copy by default -->
  <xsl:template match="@*|node()">
    <xsl:copy>
       <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

</xsl:transform>
