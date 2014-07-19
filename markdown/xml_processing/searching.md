

9.5. Searching for elements
---------------------------

Traversing XML documents by stepping through each node can be tedious.
If you're looking for something in particular, buried deep within your
XML document, there is a shortcut you can use to find it quickly:
`getElementsByTagName`.

For this section, you'll be using the `binary.xml` grammar file, which
looks like this:

### Example 9.20. `binary.xml`

    <?xml version="1.0"?>
    <!DOCTYPE grammar PUBLIC "-//diveintopython.net//DTD Kant Generator Pro v1.0//EN" "kgp.dtd">
    <grammar>
    <ref id="bit">
      <p>0</p>
      <p>1</p>
    </ref>
    <ref id="byte">
      <p><xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/>\
    <xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/></p>
    </ref>
    </grammar>

It has two `ref`s, `'bit'` and `'byte'`. A `bit` is either a `'0'` or
`'1'`, and a `byte` is 8 `bit`s.

### Example 9.21. Introducing `getElementsByTagName`

    >>> from xml.dom import minidom
    >>> xmldoc = minidom.parse('binary.xml')
    >>> reflist = xmldoc.getElementsByTagName('ref') 
    >>> reflist
    [<DOM Element: ref at 136138108>, <DOM Element: ref at 136144292>]
    >>> print reflist[0].toxml()
    <ref id="bit">
      <p>0</p>
      <p>1</p>
    </ref>
    >>> print reflist[1].toxml()
    <ref id="byte">
      <p><xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/>\
    <xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/></p>
    </ref>



[![1](../images/callouts/1.png)](#kgp.search.1.1) `getElementsByTagName` takes one argument, the name of the element you wish to find. It returns a list of `Element` objects, corresponding to the XML elements that have that name. In this case, you find two `ref` elements. 

### Example 9.22. Every element is searchable

    >>> firstref = reflist[0]                      
    >>> print firstref.toxml()
    <ref id="bit">
      <p>0</p>
      <p>1</p>
    </ref>
    >>> plist = firstref.getElementsByTagName("p") 
    >>> plist
    [<DOM Element: p at 136140116>, <DOM Element: p at 136142172>]
    >>> print plist[0].toxml()                     
    <p>0</p>
    >>> print plist[1].toxml()
    <p>1</p>



[![1](../images/callouts/1.png)](#kgp.search.2.1) Continuing from the previous example, the first object in your `reflist` is the `'bit'` `ref` element. 

[![2](../images/callouts/2.png)](#kgp.search.2.2) You can use the same `getElementsByTagName` method on this `Element` to find all the `<p>` elements within the `'bit'` `ref` element. 

[![3](../images/callouts/3.png)](#kgp.search.2.3) Just as before, the `getElementsByTagName` method returns a list of all the elements it found. In this case, you have two, one for each bit. 

### Example 9.23. Searching is actually recursive

    >>> plist = xmldoc.getElementsByTagName("p") 
    >>> plist
    [<DOM Element: p at 136140116>, <DOM Element: p at 136142172>, <DOM Element: p at 136146124>]
    >>> plist[0].toxml()                         
    '<p>0</p>'
    >>> plist[1].toxml()
    '<p>1</p>'
    >>> plist[2].toxml()                         
    '<p><xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/>\
    <xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/></p>'



[![1](../images/callouts/1.png)](#kgp.search.3.1) Note carefully the difference between this and the previous example. Previously, you were searching for `p` elements within `firstref`, but here you are searching for `p` elements within `xmldoc`, the root-level object that represents the entire XML document. This *does* find the `p` elements nested within the `ref` elements within the root `grammar` element. 

[![2](../images/callouts/2.png)](#kgp.search.3.2) The first two `p` elements are within the first `ref` (the `'bit'` `ref`). 

[![3](../images/callouts/3.png)](#kgp.search.3.3) The last `p` element is the one within the second `ref` (the `'byte'` `ref`). 

  

