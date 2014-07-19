

10.5. Creating separate handlers by node type
---------------------------------------------

The third useful XML processing tip involves separating your code into
logical functions, based on node types and element names. Parsed XML
documents are made up of various types of nodes, each represented by a
Python object. The root level of the document itself is represented by a
`Document` object. The `Document` then contains one or more `Element`
objects (for actual XML tags), each of which may contain other `Element`
objects, `Text` objects (for bits of text), or `Comment` objects (for
embedded comments). Python makes it easy to write a dispatcher to
separate the logic for each node type.

### Example 10.17. Class names of parsed XML objects

    >>> from xml.dom import minidom
    >>> xmldoc = minidom.parse('kant.xml') 
    >>> xmldoc
    <xml.dom.minidom.Document instance at 0x01359DE8>
    >>> xmldoc.__class__                   
    <class xml.dom.minidom.Document at 0x01105D40>
    >>> xmldoc.__class__.__name__          
    'Document'



[![1](../images/callouts/1.png)](#kgp.handler.1.1) Assume for a moment that `kant.xml` is in the current directory. 

[![2](../images/callouts/2.png)](#kgp.handler.1.2) As you saw in [Section 9.2, “Packages”](../xml_processing/packages.html "9.2. Packages"), the object returned by parsing an XML document is a `Document` object, as defined in the `minidom.py` in the `xml.dom` package. As you saw in [Section 5.4, “Instantiating Classes”](../object_oriented_framework/instantiating_classes.html "5.4. Instantiating Classes"), `__class__` is built-in attribute of every Python object. 

[![3](../images/callouts/3.png)](#kgp.handler.1.3) Furthermore, `__name__` is a built-in attribute of every Python class, and it is a string. This string is not mysterious; it's the same as the class name you type when you define a class yourself. (See [Section 5.3, “Defining Classes”](../object_oriented_framework/defining_classes.html "5.3. Defining Classes").) 

Fine, so now you can get the class name of any particular XML node
(since each XML node is represented as a Python object). How can you use
this to your advantage to separate the logic of parsing each node type?
The answer is `getattr`, which you first saw in [Section 4.4, “Getting
Object References With
getattr”](../power_of_introspection/getattr.html "4.4. Getting Object References With getattr").

### Example 10.18. `parse`, a generic XML node dispatcher

        def parse(self, node):          
            parseMethod = getattr(self, "parse_%s" % node.__class__.__name__)  
            parseMethod(node) 



[![1](../images/callouts/1.png)](#kgp.handler.2.1) First off, notice that you're constructing a larger string based on the class name of the node you were passed (in the `node` argument). So if you're passed a `Document` node, you're constructing the string `'parse_Document'`, and so forth. 

[![2](../images/callouts/2.png)](#kgp.handler.2.2) Now you can treat that string as a function name, and get a reference to the function itself using `getattr` 

[![3](../images/callouts/3.png)](#kgp.handler.2.3) Finally, you can call that function and pass the node itself as an argument. The next example shows the definitions of each of these functions. 

### Example 10.19. Functions called by the `parse` dispatcher

        def parse_Document(self, node): 
            self.parse(node.documentElement)

        def parse_Text(self, node):    
            text = node.data
            if self.capitalizeNextWord:
                self.pieces.append(text[0].upper())
                self.pieces.append(text[1:])
                self.capitalizeNextWord = 0
            else:
                self.pieces.append(text)

        def parse_Comment(self, node): 
            pass

        def parse_Element(self, node): 
            handlerMethod = getattr(self, "do_%s" % node.tagName)
            handlerMethod(node)



[![1](../images/callouts/1.png)](#kgp.handler.3.1) `parse_Document` is only ever called once, since there is only one `Document` node in an XML document, and only one `Document` object in the parsed XML representation. It simply turns around and parses the root element of the grammar file. 

[![2](../images/callouts/2.png)](#kgp.handler.3.2) `parse_Text` is called on nodes that represent bits of text. The function itself does some special processing to handle automatic capitalization of the first word of a sentence, but otherwise simply appends the represented text to a list. 

[![3](../images/callouts/3.png)](#kgp.handler.3.3) `parse_Comment` is just a `pass`, since you don't care about embedded comments in the grammar files. Note, however, that you still need to define the function and explicitly make it do nothing. If the function did not exist, the generic `parse` function would fail as soon as it stumbled on a comment, because it would try to find the non-existent `parse_Comment` function. Defining a separate function for every node type, even ones you don't use, allows the generic `parse` function to stay simple and dumb. 

[![4](../images/callouts/4.png)](#kgp.handler.3.4) The `parse_Element` method is actually itself a dispatcher, based on the name of the element's tag. The basic idea is the same: take what distinguishes elements from each other (their tag names) and dispatch to a separate function for each of them. You construct a string like `'do_xref'` (for an `<xref>` tag), find a function of that name, and call it. And so forth for each of the other tag names that might be found in the course of parsing a grammar file (`<p>` tags, `<choice>` tags). 

In this example, the dispatch functions `parse` and `parse_Element`
simply find other methods in the same class. If your processing is very
complex (or you have many different tag names), you could break up your
code into separate modules, and use dynamic importing to import each
module and call whatever functions you needed. Dynamic importing will be
discussed in [Chapter 16, *Functional
Programming*](../functional_programming/index.html "Chapter 16. Functional Programming").

  

