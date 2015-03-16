Mappa is a Topic Maps engine that is written in [Python](http://www.python.org/).

Is it compatible to the [Topic Maps - Data Model](http://www.isotopicmaps.org/sam/sam-model/) and provides different backends. Some backends are also usable in a [Jython](http://www.jython.org/) environment.

The API is Pythonic and enables the developer to create and manipulate topic maps easily.

Additionally, Mappa provides the import and export of different Topic Maps syntaxes (i.e. XTM)

## Installing ##
Either you can use the files in the "Downloads" section, or (recommended):
```
easy_install -U Mappa tm.reader.ctm tm.reader.ltm tm.reader.tmxml tm.reader.jtm
```

This installs Mappa, and syntax readers for CTM, LTM, JTM and TM/XML. The XTM reader is installed by default from Mappa.

If you just want Mappa and no additional syntax readers, just do:
```
easy_install -U Mappa
```

This will install Mappa and a XTM reader for 1.0 and 2.0/2.1 and the `tm` package.


&lt;wiki:gadget url="http://www.ohloh.net/p/74351/widgets/project\_users\_logo.xml" height="43"  border="0" /&gt;