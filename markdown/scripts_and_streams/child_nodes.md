

10.4. Finding direct children of a node
---------------------------------------

Another useful techique when parsing XML documents is finding all the
direct child elements of a particular element. For instance, in the
grammar files, a `ref` element can have several `p` elements, each of
which can contain many things, including other `p` elements. You want to
find just the `p` elements that are children of the `ref`, not `p`
elements that are children of other `p` elements.

You might think you could simply use `getElementsByTagName` for this,
but you can't. `getElementsByTagName` searches recursively and returns a
single list for all the elements it finds. Since `p` elements can
contain other `p` elements, you can't use `getElementsByTagName`,
because it would return nested `p` elements that you don't want. To find
only direct child elements, you'll need to do it yourself.

### Example 10.16. Finding direct child elements

        def randomChildElement(self, node):
            choices = [e for e in node.childNodes
                       if e.nodeType == e.ELEMENT_NODE]   
            chosen = random.choice(choices)             
            return chosen                              



[![1](../images/callouts/1.png)](#kgp.child.1.1) As you saw in [Example 9.9, “Getting child nodes”](../xml_processing/parsing_xml.html#kgp.parse.gettingchildnodes.example "Example 9.9. Getting child nodes"), the `childNodes` attribute returns a list of all the child nodes of an element. 

[![2](../images/callouts/2.png)](#kgp.child.1.2) However, as you saw in [Example 9.11, “Child nodes can be text”](../xml_processing/parsing_xml.html#kgp.parse.childnodescanbetext.example "Example 9.11. Child nodes can be text"), the list returned by `childNodes` contains all different types of nodes, including text nodes. That's not what you're looking for here. You only want the children that are elements. 

[![3](../images/callouts/3.png)](#kgp.child.1.3) Each node has a `nodeType` attribute, which can be `ELEMENT_NODE`, `TEXT_NODE`, `COMMENT_NODE`, or any number of other values. The complete list of possible values is in the `__init__.py` file in the `xml.dom` package. (See [Section 9.2, “Packages”](../xml_processing/packages.html "9.2. Packages") for more on packages.) But you're just interested in nodes that are elements, so you can filter the list to only include those nodes whose `nodeType` is `ELEMENT_NODE`. 

[![4](../images/callouts/4.png)](#kgp.child.1.4) Once you have a list of actual elements, choosing a random one is easy. Python comes with a module called `random` which includes several useful functions. The `random.choice` function takes a list of any number of items and returns a random item. For example, if the `ref` elements contains several `p` elements, then `choices` would be a list of `p` elements, and `chosen` would end up being assigned exactly one of them, selected at random. 

  

