

Chapter 8. HTML Processing
--------------------------

-   [8.1. Diving in](index.html#dialect.divein)
-   [8.2. Introducing sgmllib.py](introducing_sgmllib.html)
-   [8.3. Extracting data from HTML documents](extracting_data.html)
-   [8.4. Introducing BaseHTMLProcessor.py](basehtmlprocessor.html)
-   [8.5. locals and globals](locals_and_globals.html)
-   [8.6. Dictionary-based string
    formatting](dictionary_based_string_formatting.html)
-   [8.7. Quoting attribute values](quoting_attribute_values.html)
-   [8.8. Introducing dialect.py](dialect.html)
-   [8.9. Putting it all together](all_together.html)
-   [8.10. Summary](summary.html)

8.1. Diving in
--------------

I often see questions on
[comp.lang.python](http://groups.google.com/groups?group=comp.lang.python)
like “How can I list all the [headers images links] in my HTML
document?” “How do I parse/translate/munge the text of my HTML document
but leave the tags alone?” “How can I add/remove/quote attributes of all
my HTML tags at once?” This chapter will answer all of these questions.

Here is a complete, working Python program in two parts. The first part,
`BaseHTMLProcessor.py`, is a generic tool to help you process HTML files
by walking through the tags and text blocks. The second part,
`dialect.py`, is an example of how to use `BaseHTMLProcessor.py` to
translate the text of an HTML document but leave the tags alone. Read
the `doc string`s and comments to get an overview of what's going on.
Most of it will seem like black magic, because it's not obvious how any
of these class methods ever get called. Don't worry, all will be
revealed in due time.

### Example 8.1. `BaseHTMLProcessor.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    from sgmllib import SGMLParser
    import htmlentitydefs

    class BaseHTMLProcessor(SGMLParser):
        def reset(self):                       
            # extend (called by SGMLParser.__init__)
            self.pieces =
            SGMLParser.reset(self)

        def unknown_starttag(self, tag, attrs):
            # called for each start tag
            # attrs is a list of (attr, value) tuples
            # e.g. for <pre class="screen">, tag="pre", attrs=[("class", "screen")]
            # Ideally we would like to reconstruct original tag and attributes, but
            # we may end up quoting attribute values that weren't quoted in the source
            # document, or we may change the type of quotes around the attribute value
            # (single to double quotes).
            # Note that improperly embedded non-HTML code (like client-side Javascript)
            # may be parsed incorrectly by the ancestor, causing runtime script errors.
            # All non-HTML code must be enclosed in HTML comment tags (<!-- code -->)
            # to ensure that it will pass through this parser unaltered (in handle_comment).
            strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
            self.pieces.append("<%(tag)s%(strattrs)s>" % locals())

        def unknown_endtag(self, tag):         
            # called for each end tag, e.g. for </pre>, tag will be "pre"
            # Reconstruct the original end tag.
            self.pieces.append("</%(tag)s>" % locals())

        def handle_charref(self, ref):         
            # called for each character reference, e.g. for "&#160;", ref will be "160"
            # Reconstruct the original character reference.
            self.pieces.append("&#%(ref)s;" % locals())

        def handle_entityref(self, ref):       
            # called for each entity reference, e.g. for "&copy;", ref will be "copy"
            # Reconstruct the original entity reference.
            self.pieces.append("&%(ref)s" % locals())
            # standard HTML entities are closed with a semicolon; other entities are not
            if htmlentitydefs.entitydefs.has_key(ref):
                self.pieces.append(";")

        def handle_data(self, text):           
            # called for each block of plain text, i.e. outside of any tag and
            # not containing any character or entity references
            # Store the original text verbatim.
            self.pieces.append(text)

        def handle_comment(self, text):        
            # called for each HTML comment, e.g. <!-- insert Javascript code here -->
            # Reconstruct the original comment.
            # It is especially important that the source document enclose client-side
            # code (like Javascript) within comments so it can pass through this
            # processor undisturbed; see comments in unknown_starttag for details.
            self.pieces.append("<!--%(text)s-->" % locals())

        def handle_pi(self, text):             
            # called for each processing instruction, e.g. <?instruction>
            # Reconstruct original processing instruction.
            self.pieces.append("<?%(text)s>" % locals())

        def handle_decl(self, text):
            # called for the DOCTYPE, if present, e.g.
            # <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            #     "http://www.w3.org/TR/html4/loose.dtd">
            # Reconstruct original DOCTYPE
            self.pieces.append("<!%(text)s>" % locals())

        def output(self):              
            """Return processed HTML as a single string"""
            return "".join(self.pieces)

### Example 8.2. `dialect.py`

    import re
    from BaseHTMLProcessor import BaseHTMLProcessor

    class Dialectizer(BaseHTMLProcessor):
        subs = ()

        def reset(self):
            # extend (called from __init__ in ancestor)
            # Reset all data attributes
            self.verbatim = 0
            BaseHTMLProcessor.reset(self)

        def start_pre(self, attrs):            
            # called for every <pre> tag in HTML source
            # Increment verbatim mode count, then handle tag like normal
            self.verbatim += 1                 
            self.unknown_starttag("pre", attrs)

        def end_pre(self):                     
            # called for every </pre> tag in HTML source
            # Decrement verbatim mode count
            self.unknown_endtag("pre")         
            self.verbatim -= 1                 

        def handle_data(self, text):                                        
            # override
            # called for every block of text in HTML source
            # If in verbatim mode, save text unaltered;
            # otherwise process the text with a series of substitutions
            self.pieces.append(self.verbatim and text or self.process(text))

        def process(self, text):
            # called from handle_data
            # Process text block by performing series of regular expression
            # substitutions (actual substitions are defined in descendant)
            for fromPattern, toPattern in self.subs:
                text = re.sub(fromPattern, toPattern, text)
            return text

    class ChefDialectizer(Dialectizer):
        """convert HTML to Swedish Chef-speak
        
        based on the classic chef.x, copyright (c) 1992, 1993 John Hagerman
        """
        subs = ((r'a([nu])', r'u\1'),
                (r'A([nu])', r'U\1'),
                (r'a\B', r'e'),
                (r'A\B', r'E'),
                (r'en\b', r'ee'),
                (r'\Bew', r'oo'),
                (r'\Be\b', r'e-a'),
                (r'\be', r'i'),
                (r'\bE', r'I'),
                (r'\Bf', r'ff'),
                (r'\Bir', r'ur'),
                (r'(\w*?)i(\w*?)$', r'\1ee\2'),
                (r'\bow', r'oo'),
                (r'\bo', r'oo'),
                (r'\bO', r'Oo'),
                (r'the', r'zee'),
                (r'The', r'Zee'),
                (r'th\b', r't'),
                (r'\Btion', r'shun'),
                (r'\Bu', r'oo'),
                (r'\BU', r'Oo'),
                (r'v', r'f'),
                (r'V', r'F'),
                (r'w', r'w'),
                (r'W', r'W'),
                (r'([a-z])[.]', r'\1.  Bork Bork Bork!'))

    class FuddDialectizer(Dialectizer):
        """convert HTML to Elmer Fudd-speak"""
        subs = ((r'[rl]', r'w'),
                (r'qu', r'qw'),
                (r'th\b', r'f'),
                (r'th', r'd'),
                (r'n[.]', r'n, uh-hah-hah-hah.'))

    class OldeDialectizer(Dialectizer):
        """convert HTML to mock Middle English"""
        subs = ((r'i([bcdfghjklmnpqrstvwxyz])e\b', r'y\1'),
                (r'i([bcdfghjklmnpqrstvwxyz])e', r'y\1\1e'),
                (r'ick\b', r'yk'),
                (r'ia([bcdfghjklmnpqrstvwxyz])', r'e\1e'),
                (r'e[ea]([bcdfghjklmnpqrstvwxyz])', r'e\1e'),
                (r'([bcdfghjklmnpqrstvwxyz])y', r'\1ee'),
                (r'([bcdfghjklmnpqrstvwxyz])er', r'\1re'),
                (r'([aeiou])re\b', r'\1r'),
                (r'ia([bcdfghjklmnpqrstvwxyz])', r'i\1e'),
                (r'tion\b', r'cioun'),
                (r'ion\b', r'ioun'),
                (r'aid', r'ayde'),
                (r'ai', r'ey'),
                (r'ay\b', r'y'),
                (r'ay', r'ey'),
                (r'ant', r'aunt'),
                (r'ea', r'ee'),
                (r'oa', r'oo'),
                (r'ue', r'e'),
                (r'oe', r'o'),
                (r'ou', r'ow'),
                (r'ow', r'ou'),
                (r'\bhe', r'hi'),
                (r've\b', r'veth'),
                (r'se\b', r'e'),
                (r"'s\b", r'es'),
                (r'ic\b', r'ick'),
                (r'ics\b', r'icc'),
                (r'ical\b', r'ick'),
                (r'tle\b', r'til'),
                (r'll\b', r'l'),
                (r'ould\b', r'olde'),
                (r'own\b', r'oune'),
                (r'un\b', r'onne'),
                (r'rry\b', r'rye'),
                (r'est\b', r'este'),
                (r'pt\b', r'pte'),
                (r'th\b', r'the'),
                (r'ch\b', r'che'),
                (r'ss\b', r'sse'),
                (r'([wybdp])\b', r'\1e'),
                (r'([rnt])\b', r'\1\1e'),
                (r'from', r'fro'),
                (r'when', r'whan'))

    def translate(url, dialectName="chef"):
        """fetch URL and translate using dialect
        
        dialect in ("chef", "fudd", "olde")"""
        import urllib                      
        sock = urllib.urlopen(url)         
        htmlSource = sock.read()           
        sock.close()                       
        parserName = "%sDialectizer" % dialectName.capitalize()
        parserClass = globals()[parserName]                    
        parser = parserClass()                                 
        parser.feed(htmlSource)
        parser.close()         
        return parser.output() 

    def test(url):
        """test all dialects against URL"""
        for dialect in ("chef", "fudd", "olde"):
            outfile = "%s.html" % dialect
            fsock = open(outfile, "wb")
            fsock.write(translate(url, dialect))
            fsock.close()
            import webbrowser
            webbrowser.open_new(outfile)

    if __name__ == "__main__":
        test("http://diveintopython.net/odbchelper_list.html")

### Example 8.3. Output of `dialect.py`

Running this script will translate [Section 3.2, “Introducing
Lists”](../native_data_types/lists.html "3.2. Introducing Lists") into
[mock Swedish Chef-speak](../native_data_types/chef.html) (from The
Muppets), [mock Elmer Fudd-speak](../native_data_types/fudd.html) (from
Bugs Bunny cartoons), and [mock Middle
English](../native_data_types/olde.html) (loosely based on Chaucer's
*The Canterbury Tales*). If you look at the HTML source of the output
pages, you'll see that all the HTML tags and attributes are untouched,
but the text between the tags has been “translated” into the mock
language. If you look closer, you'll see that, in fact, only the titles
and paragraphs were translated; the code listings and screen examples
were left untouched.

    <div class="abstract">
    <p>Lists awe <span class="application">Pydon</span>'s wowkhowse datatype.
    If youw onwy expewience wif wists is awways in
    <span class="application">Visuaw Basic</span> ow (God fowbid) de datastowe
    in <span class="application">Powewbuiwdew</span>, bwace youwsewf fow
    <span class="application">Pydon</span> wists.</p>
    </div>

  

