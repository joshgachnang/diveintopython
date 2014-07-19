

Chapter 9. XML Processing
-------------------------

-   [9.1. Diving in](index.html#kgp.divein)
-   [9.2. Packages](packages.html)
-   [9.3. Parsing XML](parsing_xml.html)
-   [9.4. Unicode](unicode.html)
-   [9.5. Searching for elements](searching.html)
-   [9.6. Accessing element attributes](attributes.html)
-   [9.7. Segue](summary.html)

9.1. Diving in
--------------

These next two chapters are about XML processing in Python. It would be
helpful if you already knew what an XML document looks like, that it's
made up of structured tags to form a hierarchy of elements, and so on.
If this doesn't make sense to you, there are [many XML
tutorials](http://directory.google.com/Top/Computers/Data_Formats/Markup_Languages/XML/Resources/FAQs,_Help,_and_Tutorials/)
that can explain the basics.

If you're not particularly interested in XML, you should still read
these chapters, which cover important topics like Python packages,
Unicode, command line arguments, and how to use `getattr` for method
dispatching.

Being a philosophy major is not required, although if you have ever had
the misfortune of being subjected to the writings of Immanuel Kant, you
will appreciate the example program a lot more than if you majored in
something useful, like computer science.

There are two basic ways to work with XML. One is called SAX (“Simple
API for XML”), and it works by reading the XML a little bit at a time
and calling a method for each element it finds. (If you read [Chapter 8,
*HTML
Processing*](../html_processing/index.html "Chapter 8. HTML Processing"),
this should sound familiar, because that's how the `sgmllib` module
works.) The other is called DOM (“Document Object Model”), and it works
by reading in the entire XML document at once and creating an internal
representation of it using native Python classes linked in a tree
structure. Python has standard modules for both kinds of parsing, but
this chapter will only deal with using the DOM.

The following is a complete Python program which generates pseudo-random
output based on a context-free grammar defined in an XML format. Don't
worry yet if you don't understand what that means; you'll examine both
the program's input and its output in more depth throughout these next
two chapters.

### Example 9.1. `kgp.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Kant Generator for Python

    Generates mock philosophy based on a context-free grammar

    Usage: python kgp.py [options] [source]

    Options:
      -g ..., --grammar=...   use specified grammar file or URL
      -h, --help              show this help
      -d                      show debugging information while parsing

    Examples:
      kgp.py                  generates several paragraphs of Kantian philosophy
      kgp.py -g husserl.xml   generates several paragraphs of Husserl
      kpg.py "<xref id='paragraph'/>"  generates a paragraph of Kant
      kgp.py template.xml     reads from template.xml to decide what to generate
    """
    from xml.dom import minidom
    import random
    import toolbox
    import sys
    import getopt

    _debug = 0

    class NoSourceError(Exception): pass

    class KantGenerator:
        """generates mock philosophy based on a context-free grammar"""

        def __init__(self, grammar, source=None):
            self.loadGrammar(grammar)
            self.loadSource(source and source or self.getDefaultSource())
            self.refresh()

        def _load(self, source):
            """load XML input source, return parsed XML document

            - a URL of a remote XML file ("http://diveintopython.net/kant.xml")
            - a filename of a local XML file ("~/diveintopython/common/py/kant.xml")
            - standard input ("-")
            - the actual XML document, as a string
            """
            sock = toolbox.openAnything(source)
            xmldoc = minidom.parse(sock).documentElement
            sock.close()
            return xmldoc

        def loadGrammar(self, grammar):                         
            """load context-free grammar"""                     
            self.grammar = self._load(grammar)                  
            self.refs = {}                                      
            for ref in self.grammar.getElementsByTagName("ref"):
                self.refs[ref.attributes["id"].value] = ref     

        def loadSource(self, source):
            """load source"""
            self.source = self._load(source)

        def getDefaultSource(self):
            """guess default source of the current grammar
            
            The default source will be one of the <ref>s that is not
            cross-referenced.  This sounds complicated but it's not.
            Example: The default source for kant.xml is
            "<xref id='section'/>", because 'section' is the one <ref>
            that is not <xref>'d anywhere in the grammar.
            In most grammars, the default source will produce the
            longest (and most interesting) output.
            """
            xrefs = {}
            for xref in self.grammar.getElementsByTagName("xref"):
                xrefs[xref.attributes["id"].value] = 1
            xrefs = xrefs.keys()
            standaloneXrefs = [e for e in self.refs.keys() if e not in xrefs]
            if not standaloneXrefs:
                raise NoSourceError, "can't guess source, and no source specified"
            return '<xref id="%s"/>' % random.choice(standaloneXrefs)
            
        def reset(self):
            """reset parser"""
            self.pieces =
            self.capitalizeNextWord = 0

        def refresh(self):
            """reset output buffer, re-parse entire source file, and return output
            
            Since parsing involves a good deal of randomness, this is an
            easy way to get new output without having to reload a grammar file
            each time.
            """
            self.reset()
            self.parse(self.source)
            return self.output()

        def output(self):
            """output generated text"""
            return "".join(self.pieces)

        def randomChildElement(self, node):
            """choose a random child element of a node
            
            This is a utility method used by do_xref and do_choice.
            """
            choices = [e for e in node.childNodes
                       if e.nodeType == e.ELEMENT_NODE]
            chosen = random.choice(choices)            
            if _debug:                                 
                sys.stderr.write('%s available choices: %s\n' % \
                    (len(choices), [e.toxml() for e in choices]))
                sys.stderr.write('Chosen: %s\n' % chosen.toxml())
            return chosen                              

        def parse(self, node):         
            """parse a single XML node
            
            A parsed XML document (from minidom.parse) is a tree of nodes
            of various types.  Each node is represented by an instance of the
            corresponding Python class (Element for a tag, Text for
            text data, Document for the top-level document).  The following
            statement constructs the name of a class method based on the type
            of node we're parsing ("parse_Element" for an Element node,
            "parse_Text" for a Text node, etc.) and then calls the method.
            """
            parseMethod = getattr(self, "parse_%s" % node.__class__.__name__)
            parseMethod(node)

        def parse_Document(self, node):
            """parse the document node
            
            The document node by itself isn't interesting (to us), but
            its only child, node.documentElement, is: it's the root node
            of the grammar.
            """
            self.parse(node.documentElement)

        def parse_Text(self, node):    
            """parse a text node
            
            The text of a text node is usually added to the output buffer
            verbatim.  The one exception is that <p class='sentence'> sets
            a flag to capitalize the first letter of the next word.  If
            that flag is set, we capitalize the text and reset the flag.
            """
            text = node.data
            if self.capitalizeNextWord:
                self.pieces.append(text[0].upper())
                self.pieces.append(text[1:])
                self.capitalizeNextWord = 0
            else:
                self.pieces.append(text)

        def parse_Element(self, node): 
            """parse an element
            
            An XML element corresponds to an actual tag in the source:
            <xref id='...'>, <p chance='...'>, <choice>, etc.
            Each element type is handled in its own method.  Like we did in
            parse(), we construct a method name based on the name of the
            element ("do_xref" for an <xref> tag, etc.) and
            call the method.
            """
            handlerMethod = getattr(self, "do_%s" % node.tagName)
            handlerMethod(node)

        def parse_Comment(self, node):
            """parse a comment
            
            The grammar can contain XML comments, but we ignore them
            """
            pass
        
        def do_xref(self, node):
            """handle <xref id='...'> tag
            
            An <xref id='...'> tag is a cross-reference to a <ref id='...'>
            tag.  <xref id='sentence'/> evaluates to a randomly chosen child of
            <ref id='sentence'>.
            """
            id = node.attributes["id"].value
            self.parse(self.randomChildElement(self.refs[id]))

        def do_p(self, node):
            """handle <p> tag
            
            The <p> tag is the core of the grammar.  It can contain almost
            anything: freeform text, <choice> tags, <xref> tags, even other
            <p> tags.  If a "class='sentence'" attribute is found, a flag
            is set and the next word will be capitalized.  If a "chance='X'"
            attribute is found, there is an X% chance that the tag will be
            evaluated (and therefore a (100-X)% chance that it will be
            completely ignored)
            """
            keys = node.attributes.keys()
            if "class" in keys:
                if node.attributes["class"].value == "sentence":
                    self.capitalizeNextWord = 1
            if "chance" in keys:
                chance = int(node.attributes["chance"].value)
                doit = (chance > random.randrange(100))
            else:
                doit = 1
            if doit:
                for child in node.childNodes: self.parse(child)

        def do_choice(self, node):
            """handle <choice> tag
            
            A <choice> tag contains one or more <p> tags.  One <p> tag
            is chosen at random and evaluated; the rest are ignored.
            """
            self.parse(self.randomChildElement(node))

    def usage():
        print __doc__

    def main(argv):                         
        grammar = "kant.xml"                
        try:                                
            opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
        except getopt.GetoptError:          
            usage()                         
            sys.exit(2)                     
        for opt, arg in opts:               
            if opt in ("-h", "--help"):     
                usage()                     
                sys.exit()                  
            elif opt == '-d':               
                global _debug               
                _debug = 1                  
            elif opt in ("-g", "--grammar"):
                grammar = arg               
        
        source = "".join(args)              

        k = KantGenerator(grammar, source)
        print k.output()

    if __name__ == "__main__":
        main(sys.argv[1:])

### Example 9.2. `toolbox.py`

    """Miscellaneous utility functions"""

    def openAnything(source):            
        """URI, filename, or string --> stream

        This function lets you define parsers that take any input source
        (URL, pathname to local or network file, or actual data as a string)
        and deal with it in a uniform manner.  Returned object is guaranteed
        to have all the basic stdio read methods (read, readline, readlines).
        Just .close() the object when you're done with it.
        
        Examples:
        >>> from xml.dom import minidom
        >>> sock = openAnything("http://localhost/kant.xml")
        >>> doc = minidom.parse(sock)
        >>> sock.close()
        >>> sock = openAnything("c:\\inetpub\\wwwroot\\kant.xml")
        >>> doc = minidom.parse(sock)
        >>> sock.close()
        >>> sock = openAnything("<ref id='conjunction'><text>and</text><text>or</text></ref>")
        >>> doc = minidom.parse(sock)
        >>> sock.close()
        """
        if hasattr(source, "read"):
            return source

        if source == '-':
            import sys
            return sys.stdin

        # try to open with urllib (if source is http, ftp, or file URL)
        import urllib                         
        try:                                  
            return urllib.urlopen(source)     
        except (IOError, OSError):            
            pass                              
        
        # try to open with native open function (if source is pathname)
        try:                                  
            return open(source)               
        except (IOError, OSError):            
            pass                              
        
        # treat source as string
        import StringIO                       
        return StringIO.StringIO(str(source)) 

Run the program `kgp.py` by itself, and it will parse the default
XML-based grammar, in `kant.xml`, and print several paragraphs worth of
philosophy in the style of Immanuel Kant.

### Example 9.3. Sample output of `kgp.py`

    [you@localhost kgp]$ python kgp.py
         As is shown in the writings of Hume, our a priori concepts, in
    reference to ends, abstract from all content of knowledge; in the study
    of space, the discipline of human reason, in accordance with the
    principles of philosophy, is the clue to the discovery of the
    Transcendental Deduction.  The transcendental aesthetic, in all
    theoretical sciences, occupies part of the sphere of human reason
    concerning the existence of our ideas in general; still, the
    never-ending regress in the series of empirical conditions constitutes
    the whole content for the transcendental unity of apperception.  What
    we have alone been able to show is that, even as this relates to the
    architectonic of human reason, the Ideal may not contradict itself, but
    it is still possible that it may be in contradictions with the
    employment of the pure employment of our hypothetical judgements, but
    natural causes (and I assert that this is the case) prove the validity
    of the discipline of pure reason.  As we have already seen, time (and
    it is obvious that this is true) proves the validity of time, and the
    architectonic of human reason, in the full sense of these terms,
    abstracts from all content of knowledge.  I assert, in the case of the
    discipline of practical reason, that the Antinomies are just as
    necessary as natural causes, since knowledge of the phenomena is a
    posteriori.
        The discipline of human reason, as I have elsewhere shown, is by
    its very nature contradictory, but our ideas exclude the possibility of
    the Antinomies.  We can deduce that, on the contrary, the pure
    employment of philosophy, on the contrary, is by its very nature
    contradictory, but our sense perceptions are a representation of, in
    the case of space, metaphysics.  The thing in itself is a
    representation of philosophy.  Applied logic is the clue to the
    discovery of natural causes.  However, what we have alone been able to
    show is that our ideas, in other words, should only be used as a canon
    for the Ideal, because of our necessary ignorance of the conditions.

    [...snip...]

This is, of course, complete gibberish. Well, not complete gibberish. It
is syntactically and grammatically correct (although very verbose --
Kant wasn't what you would call a get-to-the-point kind of guy). Some of
it may actually be true (or at least the sort of thing that Kant would
have agreed with), some of it is blatantly false, and most of it is
simply incoherent. But all of it is in the style of Immanuel Kant.

Let me repeat that this is much, much funnier if you are now or have
ever been a philosophy major.

The interesting thing about this program is that there is nothing
Kant-specific about it. All the content in the previous example was
derived from the grammar file, `kant.xml`. If you tell the program to
use a different grammar file (which you can specify on the command
line), the output will be completely different.

### Example 9.4. Simpler output from `kgp.py`

    [you@localhost kgp]$ python kgp.py -g binary.xml
    00101001
    [you@localhost kgp]$ python kgp.py -g binary.xml
    10110100

You will take a closer look at the structure of the grammar file later
in this chapter. For now, all you need to know is that the grammar file
defines the structure of the output, and the `kgp.py` program reads
through the grammar and makes random decisions about which words to plug
in where.

  

