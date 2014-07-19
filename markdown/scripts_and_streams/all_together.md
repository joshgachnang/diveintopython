

10.7. Putting it all together
-----------------------------

You've covered a lot of ground. Let's step back and see how all the
pieces fit together.

To start with, this is a script that [takes its arguments on the command
line](command_line_arguments.html "10.6. Handling command-line arguments"),
using the `getopt` module.

    def main(argv):                         
    ...
        try:                                
            opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
        except getopt.GetoptError:          
    ...
        for opt, arg in opts:               
    ...

You create a new instance of the `KantGenerator` class, and pass it the
grammar file and source that may or may not have been specified on the
command line.

        k = KantGenerator(grammar, source)

The `KantGenerator` instance automatically loads the grammar, which is
an XML file. You use your custom `openAnything` function to open the
file (which [could be stored in a local file or a remote web
server](index.html#kgp.openanything "10.1. Abstracting input sources")),
then use the built-in `minidom` parsing functions to [parse the XML into
a tree of Python
objects](../xml_processing/parsing_xml.html "9.3. Parsing XML").

        def _load(self, source):
            sock = toolbox.openAnything(source)
            xmldoc = minidom.parse(sock).documentElement
            sock.close()

Oh, and along the way, you take advantage of your knowledge of the
structure of the XML document to [set up a little cache of
references](caching.html "10.3. Caching node lookups"), which are just
elements in the XML document.

        def loadGrammar(self, grammar):                         
            for ref in self.grammar.getElementsByTagName("ref"):
                self.refs[ref.attributes["id"].value] = ref     

If you specified some source material on the command line, you use that;
otherwise you rip through the grammar looking for the "top-level"
reference (that isn't referenced by anything else) and use that as a
starting point.

        def getDefaultSource(self):
            xrefs = {}
            for xref in self.grammar.getElementsByTagName("xref"):
                xrefs[xref.attributes["id"].value] = 1
            xrefs = xrefs.keys()
            standaloneXrefs = [e for e in self.refs.keys() if e not in xrefs]
            return '<xref id="%s"/>' % random.choice(standaloneXrefs)

Now you rip through the source material. The source material is also
XML, and you parse it one node at a time. To keep the code separated and
more maintainable, you use [separate handlers for each node
type](handlers_by_node_type.html "10.5. Creating separate handlers by node type").

        def parse_Element(self, node): 
            handlerMethod = getattr(self, "do_%s" % node.tagName)
            handlerMethod(node)

You bounce through the grammar, [parsing all the
children](child_nodes.html "10.4. Finding direct children of a node") of
each `p` element,

        def do_p(self, node):
    ...
            if doit:
                for child in node.childNodes: self.parse(child)

replacing `choice` elements with a random child,

        def do_choice(self, node):
            self.parse(self.randomChildElement(node))

and replacing `xref` elements with a random child of the corresponding
`ref` element, which you previously cached.

        def do_xref(self, node):
            id = node.attributes["id"].value
            self.parse(self.randomChildElement(self.refs[id]))

Eventually, you parse your way down to plain text,

        def parse_Text(self, node):    
            text = node.data
    ...
                self.pieces.append(text)

which you print out.

    def main(argv):                         
    ...
        k = KantGenerator(grammar, source)
        print k.output()

  

