# Introduction #

Install:

```
easy_install Mappa tm.reader.ctm tm.reader.ltm tm.reader.tmxml tm.reader.jtm
```

# Usage #
```
import mappa
conn = mappa.connect()

# Creating a topic map
tm = conn.create('http://www.semagia.com/map1')

# Creating a topic with a subject identifier
t = tm.create_topic(sid='http://psi.example.org/topic')
# Creating a topic with a subject locator
t2 = tm.create_topic(slo='http://www.google.com/')
# Creating a topic with an item identifier
t3 = tm.create_topic(iid='http://www.example.org/map1#topic')
```

More docs will follow, see the interface description here:
https://code.google.com/p/mappa/source/browse/mappa/mappa/interfaces.py


# Creating associations #
```
>>> import mappa
>>> conn = mappa.connect()
>>> tm = conn.create('http://www.semagia.com/example-map')
>>> member_of = tm.create_topic(sid='http://psi.example.org/member-of')
>>> beatles = tm.create_topic(sid='http://psi.example.org/The_Beatles')
>>> john = tm.create_topic(sid='http://psi.example.org/John_Lennon')
>>> membership_john = tm.create_association(type=member_of)
>>> role = membership_john.create_role(type=tm.create_topic(sid='http://psi.exmaple.org/member'), player=john)
>>> role2 = membership_john.create_role(type=tm.create_topic(sid='http://psi.exmaple.org/group'), player=beatles)
>>>

```

# Creating names #
```
>>> from mappa import TMDM
>>> firstname = john.create_name(type=tm.create_topic(sid=TMDM.topic_name),
			     value='John')
>>> firstname.value
u'John'

```

It's also possible to save some code and use the following short cut to create new names (although the newly name is not returned). The part behind the hyphen (`-`) is interpreted as item identifier of the topic which should be used as name type. If the topic does not exists, it is automatically created.
```
>>> john['- surname'] = 'Lennon'
>>> for name in john.names:
	print name.value

	
Lennon
John
```

# Creating occurrences #
```
>>> from mappa import XSD
>>> # The value of a occurrence takes an optional datatype component
>>> # if the datatype is not specified, the datatype is set to xsd:string
>>> homepage = john.create_occurrence(type=tm.create_topic(sid='http://psi.example.org/homepage'), 
        value=('http://en.wikipedia.org/wiki/John_Lennon', XSD.anyURI))
>>> homepage.value
u'http://en.wikipedia.org/wiki/John_Lennon'
>>> homepage.datatype
u'http://www.w3.org/2001/XMLSchema#anyURI'
>>> 
```

Creating occurrences is also possible using a shortcut:
```
>>> john['http://psi.example.org/homepage'] = 'http://de.wikipedia.org/wiki/John_Lennon', XSD.anyURI
>>> #Filtering occurrences by using the [] notation is also possible
>>> for homepage in john['http://psi.example.org/homepage']:
	print homepage.value, homepage.datatype

	
http://de.wikipedia.org/wiki/John_Lennon http://www.w3.org/2001/XMLSchema#anyURI
http://en.wikipedia.org/wiki/John_Lennon http://www.w3.org/2001/XMLSchema#anyURI
>>> 

```

# Loading topic maps #
```
>>> import mappa
>>> conn = mappa.connect()
>>> src_iri = 'http://cxtm-tests.svn.sourceforge.net/viewvc/cxtm-tests/trunk/ctm/in/association.ctm'
>>> conn.load(src_iri, into='http://www.example.org/schema.map', format='ctm')
```

# Importing a fragment #
```
>>> import mappa
>>> conn = mappa.connect()
>>> # Importing a LTM fragment, requires the tm.reader.ltm package
>>> # By default, only the XTM readers are installed
>>> conn.loads('''
[Mappa = "Mappa Topic Maps engine"]
''',
into='http://www.example.org/map',
format='ltm')
>>> tm = conn.get('http://www.example.org/map')
>>> t_mappa = tm.topic('http://www.example.org/map#Mappa')
>>> for name in t_mappa.names:
	print name.value

	
Mappa Topic Maps engine
>>> 
```

# Exporting Topic Maps #
```
>>> from cStringIO import StringIO
>>> out = StringIO()
>>> conn.write('http://www.example.org/map',
	   out=out,
	   format='jtm')
>>> print out.getvalue()
{"version":"1.0","item_type":"topicmap","topics":[{"subject_identifiers":["http:\/\/psi.topicmaps.org\/iso13250\/model\/topic-name"]},{"item_identifiers":["http:\/\/www.example.org\/map#Mappa"],"names":[{"value":"Mappa Topic Maps engine"}]}]}

>>> # The output is meant to be used by machines, if you want to prettify it, 
>>> # you have to use the 'prettify' keyword (works also for the 'xtm' serializer)
>>> out.truncate(0)
>>> conn.write('http://www.example.org/map',
	   out=out,
	   format='jtm',prettify=True)
>>> print out.getvalue()
{"version":"1.0",
  "item_type":"topicmap",
  "topics":[
    {"subject_identifiers":["http:\/\/psi.topicmaps.org\/iso13250\/model\/topic-name"]},
    {"item_identifiers":["http:\/\/www.example.org\/map#Mappa"],
      "names":[
        {"value":"Mappa Topic Maps engine"}]}]}

>>> 
```

## Exporting to XTM ##
```
>>> # Now we want to export the tm into the XTM format
>>> # Let's use XTM 2.0 first
>>> out.truncate(0)
>>> conn.write('http://www.example.org/map',
	   out=out,
	   format='xtm',prettify=True)
>>> print out.getvalue()
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!-- Generated by Mappa - http://mappa.semagia.com/ -->
<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.0">
  <topic id="id-257859927226702976729448316754989795419">
    <subjectIdentifier href="http://psi.topicmaps.org/iso13250/model/topic-name"/>
  </topic>
  <topic id="Mappa">
    <itemIdentity href="http://www.example.org/map#Mappa"/>
    <name>
      <value>Mappa Topic Maps engine</value>
    </name>
  </topic>
</topicMap>

>>> # By default, Mappa uses always the latest available version
>>> # The user can specify the version of the serialization format
>>> # with the 'version' keyword
>>> out.truncate(0)
>>> conn.write('http://www.example.org/map',
	   out=out,
	   format='xtm', version=1.0, prettify=True)
>>> print out.getvalue()
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<!-- Generated by Mappa - http://mappa.semagia.com/ -->
<topicMap xmlns="http://www.topicmaps.org/xtm/1.0/" xmlns:xlink="http://www.w3.org/1999/xlink">
  <topic id="id-257859927226702976729448316754989795419">
    <subjectIdentity>
      <subjectIndicatorRef xlink:href="http://psi.topicmaps.org/iso13250/model/topic-name"/>
    </subjectIdentity>
  </topic>
  <topic id="Mappa">
    <baseName>
      <baseNameString>Mappa Topic Maps engine</baseNameString>
    </baseName>
  </topic>
</topicMap>

>>> 
```