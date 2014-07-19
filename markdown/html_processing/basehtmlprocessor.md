

8.4. Introducing `BaseHTMLProcessor.py`
---------------------------------------

`SGMLParser` doesn't produce anything by itself. It parses and parses
and parses, and it calls a method for each interesting thing it finds,
but the methods don't do anything. `SGMLParser` is an HTML *consumer*:
it takes HTML and breaks it down into small, structured pieces. As you
saw in the [previous
section](extracting_data.html "8.3. Extracting data from HTML documents"),
you can subclass `SGMLParser` to define classes that catch specific tags
and produce useful things, like a list of all the links on a web page.
Now you'll take this one step further by defining a class that catches
everything `SGMLParser` throws at it and reconstructs the complete HTML
document. In technical terms, this class will be an HTML *producer*.

`BaseHTMLProcessor` subclasses `SGMLParser` and provides all 8 essential
handler methods: `unknown_starttag`, `unknown_endtag`, `handle_charref`,
`handle_entityref`, `handle_comment`, `handle_pi`, `handle_decl`, and
`handle_data`.

### Example 8.8. Introducing `BaseHTMLProcessor`

    class BaseHTMLProcessor(SGMLParser):
        def reset(self):                        
            self.pieces =
            SGMLParser.reset(self)

        def unknown_starttag(self, tag, attrs): 
            strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
            self.pieces.append("<%(tag)s%(strattrs)s>" % locals())

        def unknown_endtag(self, tag):          
            self.pieces.append("</%(tag)s>" % locals())

        def handle_charref(self, ref):          
            self.pieces.append("&#%(ref)s;" % locals())

        def handle_entityref(self, ref):        
            self.pieces.append("&%(ref)s" % locals())
            if htmlentitydefs.entitydefs.has_key(ref):
                self.pieces.append(";")

        def handle_data(self, text):            
            self.pieces.append(text)

        def handle_comment(self, text):         
            self.pieces.append("<!--%(text)s-->" % locals())

        def handle_pi(self, text):              
            self.pieces.append("<?%(text)s>" % locals())

        def handle_decl(self, text):
            self.pieces.append("<!%(text)s>" % locals())



[![1](../images/callouts/1.png)](#dialect.basehtml.1.1) `reset`, called by `SGMLParser.__init__`, initializes `self.pieces` as an empty list before [calling the ancestor method](../object_oriented_framework/defining_classes.html#fileinfo.init.code.example "Example 5.6. Coding the FileInfo Class"). `self.pieces` is a [data attribute](../object_oriented_framework/userdict.html#fileinfo.userdict.init.example "Example 5.9. Defining the UserDict Class") which will hold the pieces of the HTML document you're constructing. Each handler method will reconstruct the HTML that `SGMLParser` parsed, and each method will append that string to `self.pieces`. Note that `self.pieces` is a list. You might be tempted to define it as a string and just keep appending each piece to it. That would work, but Python is much more efficient at dealing with lists.<sup>[[2](#ftn.d0e20702)]</sup> 

[![2](../images/callouts/2.png)](#dialect.basehtml.1.2) Since `BaseHTMLProcessor` does not define any methods for specific tags (like the `start_a` method in [`URLLister`](extracting_data.html#dialect.extract.links "Example 8.6. Introducing urllister.py")), `SGMLParser` will call `unknown_starttag` for every start tag. This method takes the tag (`tag`) and the list of attribute name/value pairs (`attrs`), reconstructs the original HTML, and appends it to `self.pieces`. The [string formatting](../native_data_types/formatting_strings.html "3.5. Formatting Strings") here is a little strange; you'll untangle that (and also the odd-looking `locals` function) later in this chapter. 

[![3](../images/callouts/3.png)](#dialect.basehtml.1.3) Reconstructing end tags is much simpler; just take the tag name and wrap it in the `</...>` brackets. 

[![4](../images/callouts/4.png)](#dialect.basehtml.1.4) When `SGMLParser` finds a character reference, it calls `handle_charref` with the bare reference. If the HTML document contains the reference `&#160;`, `ref` will be `160`. Reconstructing the original complete character reference just involves wrapping `ref` in `&#...;` characters. 

[![5](../images/callouts/5.png)](#dialect.basehtml.1.5) Entity references are similar to character references, but without the hash mark. Reconstructing the original entity reference requires wrapping `ref` in `&...;` characters. (Actually, as an erudite reader pointed out to me, it's slightly more complicated than this. Only certain standard HTML entites end in a semicolon; other similar-looking entities do not. Luckily for us, the set of standard HTML entities is defined in a dictionary in a Python module called `htmlentitydefs`. Hence the extra `if` statement.) 

[![6](../images/callouts/6.png)](#dialect.basehtml.1.6) Blocks of text are simply appended to `self.pieces` unaltered. 

[![7](../images/callouts/7.png)](#dialect.basehtml.1.7) HTML comments are wrapped in `<!--...-->` characters. 

[![8](../images/callouts/8.png)](#dialect.basehtml.1.8) Processing instructions are wrapped in `<?...>` characters. 


![Important](../images/important.png) 
The HTML specification requires that all non-HTML (like client-side JavaScript) must be enclosed in HTML comments, but not all web pages do this properly (and all modern web browsers are forgiving if they don't). `BaseHTMLProcessor` is not forgiving; if script is improperly embedded, it will be parsed as if it were HTML. For instance, if the script contains less-than and equals signs, `SGMLParser` may incorrectly think that it has found tags and attributes. `SGMLParser` always converts tags and attribute names to lowercase, which may break the script, and `BaseHTMLProcessor` always encloses attribute values in double quotes (even if the original HTML document used single quotes or no quotes), which will certainly break the script. Always protect your client-side script within HTML comments. 

### Example 8.9. `BaseHTMLProcessor` output

        def output(self):               
            """Return processed HTML as a single string"""
            return "".join(self.pieces) 



[![1](../images/callouts/1.png)](#dialect.basehtml.2.1) This is the one method in `BaseHTMLProcessor` that is never called by the ancestor `SGMLParser`. Since the other handler methods store their reconstructed HTML in `self.pieces`, this function is needed to join all those pieces into one string. As noted before, Python is great at lists and mediocre at strings, so you only create the complete string when somebody explicitly asks for it. 

[![2](../images/callouts/2.png)](#dialect.basehtml.2.2) If you prefer, you could use the `join` method of the `string` module instead: `string.join(self.pieces, "")` 

### Further reading

-   [W3C](http://www.w3.org/) discusses [character and entity
    references](http://www.w3.org/TR/REC-html40/charset.html#entities).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    confirms your suspicions that [the `htmlentitydefs`
    module](http://www.python.org/doc/current/lib/module-htmlentitydefs.html)
    is exactly what it sounds like.

### Footnotes

<sup>[[2](#d0e20702)]</sup>The reason Python is better at lists than
strings is that lists are mutable but strings are immutable. This means
that appending to a list just adds the element and updates the index.
Since strings can not be changed after they are created, code like
`s = s + newpiece` will create an entirely new string out of the
concatenation of the original and the new piece, then throw away the
original string. This involves a lot of expensive memory management, and
the amount of effort involved increases as the string gets longer, so
doing `s = s + newpiece` in a loop is deadly. In technical terms,
appending `n` items to a list is `O(n)`, while appending `n` items to a
string is `O(n2)`.

  

