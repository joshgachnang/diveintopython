

9.6. Accessing element attributes
---------------------------------

XML elements can have one or more attributes, and it is incredibly
simple to access them once you have parsed an XML document.

For this section, you'll be using the `binary.xml` grammar file that you
saw in the [previous
section](searching.html "9.5. Searching for elements").


![Note](../images/note.png) 
This section may be a little confusing, because of some overlapping terminology. Elements in an XML document have attributes, and Python objects also have attributes. When you parse an XML document, you get a bunch of Python objects that represent all the pieces of the XML document, and some of these Python objects represent attributes of the XML elements. But the (Python) objects that represent the (XML) attributes also have (Python) attributes, which are used to access various parts of the (XML) attribute that the object represents. I told you it was confusing. I am open to suggestions on how to distinguish these more clearly. 

### Example 9.24. Accessing element attributes

    >>> xmldoc = minidom.parse('binary.xml')
    >>> reflist = xmldoc.getElementsByTagName('ref')
    >>> bitref = reflist[0]
    >>> print bitref.toxml()
    <ref id="bit">
      <p>0</p>
      <p>1</p>
    </ref>
    >>> bitref.attributes          
    <xml.dom.minidom.NamedNodeMap instance at 0x81e0c9c>
    >>> bitref.attributes.keys()    
    [u'id']
    >>> bitref.attributes.values() 
    [<xml.dom.minidom.Attr instance at 0x81d5044>]
    >>> bitref.attributes["id"]    
    <xml.dom.minidom.Attr instance at 0x81d5044>



[![1](../images/callouts/1.png)](#kgp.attributes.1.1) Each `Element` object has an attribute called `attributes`, which is a `NamedNodeMap` object. This sounds scary, but it's not, because a `NamedNodeMap` is an object that [acts like a dictionary](../object_oriented_framework/userdict.html "5.5. Exploring UserDict: A Wrapper Class"), so you already know how to use it. 

[![2](../images/callouts/2.png)](#kgp.attributes.1.2) Treating the `NamedNodeMap` as a dictionary, you can get a list of the names of the attributes of this element by using `attributes.keys()`. This element has only one attribute, `'id'`. 

[![3](../images/callouts/3.png)](#kgp.attributes.1.3) Attribute names, like all other text in an XML document, are stored in [unicode](unicode.html "9.4. Unicode"). 

[![4](../images/callouts/4.png)](#kgp.attributes.1.4) Again treating the `NamedNodeMap` as a dictionary, you can get a list of the values of the attributes by using `attributes.values()`. The values are themselves objects, of type `Attr`. You'll see how to get useful information out of this object in the next example. 

[![5](../images/callouts/5.png)](#kgp.attributes.1.5) Still treating the `NamedNodeMap` as a dictionary, you can access an individual attribute by name, using normal dictionary syntax. (Readers who have been paying extra-close attention will already know how the `NamedNodeMap` class accomplishes this neat trick: by defining a [`__getitem__` special method](../object_oriented_framework/special_class_methods.html "5.6. Special Class Methods"). Other readers can take comfort in the fact that they don't need to understand how it works in order to use it effectively.) 

### Example 9.25. Accessing individual attributes

    >>> a = bitref.attributes["id"]
    >>> a
    <xml.dom.minidom.Attr instance at 0x81d5044>
    >>> a.name  
    u'id'
    >>> a.value 
    u'bit'



[![1](../images/callouts/1.png)](#kgp.attributes.2.1) The `Attr` object completely represents a single XML attribute of a single XML element. The name of the attribute (the same name as you used to find this object in the `bitref.attributes` `NamedNodeMap` pseudo-dictionary) is stored in `a.name`. 

[![2](../images/callouts/2.png)](#kgp.attributes.2.2) The actual text value of this XML attribute is stored in `a.value`. 


![Note](../images/note.png) 
Like a dictionary, attributes of an XML element have no ordering. Attributes may *happen to be* listed in a certain order in the original XML document, and the `Attr` objects may *happen to be* listed in a certain order when the XML document is parsed into Python objects, but these orders are arbitrary and should carry no special meaning. You should always access individual attributes by name, like the keys of a dictionary. 

  

