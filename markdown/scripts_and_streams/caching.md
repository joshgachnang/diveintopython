

10.3. Caching node lookups
--------------------------

`kgp.py` employs several tricks which may or may not be useful to you in
your XML processing. The first one takes advantage of the consistent
structure of the input documents to build a cache of nodes.

A grammar file defines a series of `ref` elements. Each `ref` contains
one or more `p` elements, which can contain a lot of different things,
including `xref`s. Whenever you encounter an `xref`, you look for a
corresponding `ref` element with the same `id` attribute, and choose one
of the `ref` element's children and parse it. (You'll see how this
random choice is made in the next section.)

This is how you build up the grammar: define `ref` elements for the
smallest pieces, then define `ref` elements which "include" the first
`ref` elements by using `xref`, and so forth. Then you parse the
"largest" reference and follow each `xref`, and eventually output real
text. The text you output depends on the (random) decisions you make
each time you fill in an `xref`, so the output is different each time.

This is all very flexible, but there is one downside: performance. When
you find an `xref` and need to find the corresponding `ref` element, you
have a problem. The `xref` has an `id` attribute, and you want to find
the `ref` element that has that same `id` attribute, but there is no
easy way to do that. The slow way to do it would be to get the entire
list of `ref` elements each time, then manually loop through and look at
each `id` attribute. The fast way is to do that once and build a cache,
in the form of a dictionary.

### Example 10.14. `loadGrammar`

        def loadGrammar(self, grammar):                         
            self.grammar = self._load(grammar)                  
            self.refs = {}                                       
            for ref in self.grammar.getElementsByTagName("ref"): 
                self.refs[ref.attributes["id"].value] = ref       



[![1](../images/callouts/1.png)](#kgp.cache.1.1) Start by creating an empty dictionary, `self.refs`. 

[![2](../images/callouts/2.png)](#kgp.cache.1.2) As you saw in [Section 9.5, “Searching for elements”](../xml_processing/searching.html "9.5. Searching for elements"), `getElementsByTagName` returns a list of all the elements of a particular name. You easily can get a list of all the `ref` elements, then simply loop through that list. 

[![3](../images/callouts/3.png)](#kgp.cache.1.3) As you saw in [Section 9.6, “Accessing element attributes”](../xml_processing/attributes.html "9.6. Accessing element attributes"), you can access individual attributes of an element by name, using standard dictionary syntax. So the keys of the `self.refs` dictionary will be the values of the `id` attribute of each `ref` element. 

[![4](../images/callouts/4.png)](#kgp.cache.1.4) The values of the `self.refs` dictionary will be the `ref` elements themselves. As you saw in [Section 9.3, “Parsing XML”](../xml_processing/parsing_xml.html "9.3. Parsing XML"), each element, each node, each comment, each piece of text in a parsed XML document is an object. 

Once you build this cache, whenever you come across an `xref` and need
to find the `ref` element with the same `id` attribute, you can simply
look it up in `self.refs`.

### Example 10.15. Using the `ref` element cache

        def do_xref(self, node):
            id = node.attributes["id"].value
            self.parse(self.randomChildElement(self.refs[id]))

You'll explore the `randomChildElement` function in the next section.

  

