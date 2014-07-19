

9.4. Unicode
------------

Unicode is a system to represent characters from all the world's
different languages. When Python parses an XML document, all data is
stored in memory as unicode.

You'll get to all that in a minute, but first, some background.

**Historical note. **Before unicode, there were separate character
encoding systems for each language, each using the same numbers (0-255)
to represent that language's characters. Some languages (like Russian)
have multiple conflicting standards about how to represent the same
characters; other languages (like Japanese) have so many characters that
they require multiple-byte character sets. Exchanging documents between
systems was difficult because there was no way for a computer to tell
for certain which character encoding scheme the document author had
used; the computer only saw numbers, and the numbers could mean
different things. Then think about trying to store these documents in
the same place (like in the same database table); you would need to
store the character encoding alongside each piece of text, and make sure
to pass it around whenever you passed the text around. Then think about
multilingual documents, with characters from multiple languages in the
same document. (They typically used escape codes to switch modes; poof,
you're in Russian koi8-r mode, so character 241 means this; poof, now
you're in Mac Greek mode, so character 241 means something else. And so
on.) These are the problems which unicode was designed to solve.

To solve these problems, unicode represents each character as a 2-byte
number, from 0 to 65535.<sup>[[5](#ftn.d0e23786)]</sup> Each 2-byte
number represents a unique character used in at least one of the world's
languages. (Characters that are used in multiple languages have the same
numeric code.) There is exactly 1 number per character, and exactly 1
character per number. Unicode data is never ambiguous.

Of course, there is still the matter of all these legacy encoding
systems. 7-bit ASCII, for instance, which stores English characters as
numbers ranging from 0 to 127. (65 is capital “`A`”, 97 is lowercase
“`a`”, and so forth.) English has a very simple alphabet, so it can be
completely expressed in 7-bit ASCII. Western European languages like
French, Spanish, and German all use an encoding system called ISO-8859-1
(also called “latin-1”), which uses the 7-bit ASCII characters for the
numbers 0 through 127, but then extends into the 128-255 range for
characters like n-with-a-tilde-over-it (241), and
u-with-two-dots-over-it (252). And unicode uses the same characters as
7-bit ASCII for 0 through 127, and the same characters as ISO-8859-1 for
128 through 255, and then extends from there into characters for other
languages with the remaining numbers, 256 through 65535.

When dealing with unicode data, you may at some point need to convert
the data back into one of these other legacy encoding systems. For
instance, to integrate with some other computer system which expects its
data in a specific 1-byte encoding scheme, or to print it to a
non-unicode-aware terminal or printer. Or to store it in an XML document
which explicitly specifies the encoding scheme.

And on that note, let's get back to Python.

Python has had unicode support throughout the language since version
2.0. The XML package uses unicode to store all parsed XML data, but you
can use unicode anywhere.

### Example 9.13. Introducing unicode

    >>> s = u'Dive in'            
    >>> s
    u'Dive in'
    >>> print s                   
    Dive in



[![1](../images/callouts/1.png)](#kgp.unicode.1.1) To create a unicode string instead of a regular ASCII string, add the letter “`u`” before the string. Note that this particular string doesn't have any non-ASCII characters. That's fine; unicode is a superset of ASCII (a very large superset at that), so any regular ASCII string can also be stored as unicode. 

[![2](../images/callouts/2.png)](#kgp.unicode.1.2) When printing a string, Python will attempt to convert it to your default encoding, which is usually ASCII. (More on this in a minute.) Since this unicode string is made up of characters that are also ASCII characters, printing it has the same result as printing a normal ASCII string; the conversion is seamless, and if you didn't know that `s` was a unicode string, you'd never notice the difference. 

### Example 9.14. Storing non-ASCII characters

    >>> s = u'La Pe\xf1a'         
    >>> print s                   
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    UnicodeError: ASCII encoding error: ordinal not in range(128)
    >>> print s.encode('latin-1') 
    La Peña



[![1](../images/callouts/1.png)](#kgp.unicode.2.1) The real advantage of unicode, of course, is its ability to store non-ASCII characters, like the Spanish “`ñ`” (`n` with a tilde over it). The unicode character code for the tilde-n is `0xf1` in hexadecimal (241 in decimal), which you can type like this: `\xf1`. 

[![2](../images/callouts/2.png)](#kgp.unicode.2.2) Remember I said that the `print` function attempts to convert a unicode string to ASCII so it can print it? Well, that's not going to work here, because your unicode string contains non-ASCII characters, so Python raises a `UnicodeError` error. 

[![3](../images/callouts/3.png)](#kgp.unicode.2.3) Here's where the conversion-from-unicode-to-other-encoding-schemes comes in. `s` is a unicode string, but `print` can only print a regular string. To solve this problem, you call the `encode` method, available on every unicode string, to convert the unicode string to a regular string in the given encoding scheme, which you pass as a parameter. In this case, you're using `latin-1` (also known as `iso-8859-1`), which includes the tilde-n (whereas the default ASCII encoding scheme did not, since it only includes characters numbered 0 through 127). 

Remember I said Python usually converted unicode to ASCII whenever it
needed to make a regular string out of a unicode string? Well, this
default encoding scheme is an option which you can customize.

### Example 9.15. `sitecustomize.py`

    # sitecustomize.py                   
    # this file can be anywhere in your Python path,
    # but it usually goes in ${pythondir}/lib/site-packages/
    import sys
    sys.setdefaultencoding('iso-8859-1') 



[![1](../images/callouts/1.png)](#kgp.unicode.3.1) `sitecustomize.py` is a special script; Python will try to import it on startup, so any code in it will be run automatically. As the comment mentions, it can go anywhere (as long as `import` can find it), but it usually goes in the `site-packages` directory within your Python `lib` directory. 

[![2](../images/callouts/2.png)](#kgp.unicode.3.2) `setdefaultencoding` function sets, well, the default encoding. This is the encoding scheme that Python will try to use whenever it needs to auto-coerce a unicode string into a regular string. 

### Example 9.16. Effects of setting the default encoding

    >>> import sys
    >>> sys.getdefaultencoding() 
    'iso-8859-1'
    >>> s = u'La Pe\xf1a'
    >>> print s                  
    La Peña



[![1](../images/callouts/1.png)](#kgp.unicode.4.1) This example assumes that you have made the changes listed in the previous example to your `sitecustomize.py` file, and restarted Python. If your default encoding still says `'ascii'`, you didn't set up your `sitecustomize.py` properly, or you didn't restart Python. The default encoding can only be changed during Python startup; you can't change it later. (Due to some wacky programming tricks that I won't get into right now, you can't even call `sys.setdefaultencoding` after Python has started up. Dig into `site.py` and search for “`setdefaultencoding`” to find out how.) 

[![2](../images/callouts/2.png)](#kgp.unicode.4.2) Now that the default encoding scheme includes all the characters you use in your string, Python has no problem auto-coercing the string and printing it. 

### Example 9.17. Specifying encoding in `.py` files

If you are going to be storing non-ASCII strings within your Python
code, you'll need to specify the encoding of each individual `.py` file
by putting an encoding declaration at the top of each file. This
declaration defines the `.py` file to be UTF-8:

    #!/usr/bin/env python
    # -*- coding: UTF-8 -*-

Now, what about XML? Well, every XML document is in a specific encoding.
Again, ISO-8859-1 is a popular encoding for data in Western European
languages. KOI8-R is popular for Russian texts. The encoding, if
specified, is in the header of the XML document.

### Example 9.18. `russiansample.xml`

    <?xml version="1.0" encoding="koi8-r"?>       
    <preface>
    <title>Предисловие</title>                    
    </preface>



[![1](../images/callouts/1.png)](#kgp.unicode.5.1) This is a sample extract from a real Russian XML document; it's part of a Russian translation of this very book. Note the encoding, `koi8-r`, specified in the header. 

[![2](../images/callouts/2.png)](#kgp.unicode.5.2) These are Cyrillic characters which, as far as I know, spell the Russian word for “Preface”. If you open this file in a regular text editor, the characters will most likely like gibberish, because they're encoded using the `koi8-r` encoding scheme, but they're being displayed in `iso-8859-1`. 

### Example 9.19. Parsing `russiansample.xml`

    >>> from xml.dom import minidom
    >>> xmldoc = minidom.parse('russiansample.xml') 
    >>> title = xmldoc.getElementsByTagName('title')[0].firstChild.data
    >>> title                                       
    u'\u041f\u0440\u0435\u0434\u0438\u0441\u043b\u043e\u0432\u0438\u0435'
    >>> print title                                 
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    UnicodeError: ASCII encoding error: ordinal not in range(128)
    >>> convertedtitle = title.encode('koi8-r')     
    >>> convertedtitle
    '\xf0\xd2\xc5\xc4\xc9\xd3\xcc\xcf\xd7\xc9\xc5'
    >>> print convertedtitle                        
    Предисловие



[![1](../images/callouts/1.png)](#kgp.unicode.6.1) I'm assuming here that you saved the previous example as `russiansample.xml` in the current directory. I am also, for the sake of completeness, assuming that you've changed your default encoding back to `'ascii'` by removing your `sitecustomize.py` file, or at least commenting out the `setdefaultencoding` line. 

[![2](../images/callouts/2.png)](#kgp.unicode.6.2) Note that the text data of the `title` tag (now in the `title` variable, thanks to that long concatenation of Python functions which I hastily skipped over and, annoyingly, won't explain until the next section) -- the text data inside the XML document's `title` element is stored in unicode. 

[![3](../images/callouts/3.png)](#kgp.unicode.6.3) Printing the title is not possible, because this unicode string contains non-ASCII characters, so Python can't convert it to ASCII because that doesn't make sense. 

[![4](../images/callouts/4.png)](#kgp.unicode.6.4) You can, however, explicitly convert it to `koi8-r`, in which case you get a (regular, not unicode) string of single-byte characters (`f0`, `d2`, `c5`, and so forth) that are the `koi8-r`-encoded versions of the characters in the original unicode string. 

[![5](../images/callouts/5.png)](#kgp.unicode.6.5) Printing the `koi8-r`-encoded string will probably show gibberish on your screen, because your Python IDE is interpreting those characters as `iso-8859-1`, not `koi8-r`. But at least they do print. (And, if you look carefully, it's the same gibberish that you saw when you opened the original XML document in a non-unicode-aware text editor. Python converted it from `koi8-r` into unicode when it parsed the XML document, and you've just converted it back.) 

To sum up, unicode itself is a bit intimidating if you've never seen it
before, but unicode data is really very easy to handle in Python. If
your XML documents are all 7-bit ASCII (like the examples in this
chapter), you will literally never think about unicode. Python will
convert the ASCII data in the XML documents into unicode while parsing,
and auto-coerce it back to ASCII whenever necessary, and you'll never
even notice. But if you need to deal with that in other languages,
Python is ready.

### Further reading

-   [Unicode.org](http://www.unicode.org/) is the home page of the
    unicode standard, including a brief [technical
    introduction](http://www.unicode.org/standard/principles.html).
-   [Unicode
    Tutorial](http://www.reportlab.com/i18n/python_unicode_tutorial.html)
    has some more examples of how to use Python's unicode functions,
    including how to force Python to coerce unicode into ASCII even when
    it doesn't really want to.
-   [PEP 263](http://www.python.org/peps/pep-0263.html) goes into more
    detail about how and when to define a character encoding in your
    `.py` files.

### Footnotes

<sup>[[5](#d0e23786)]</sup>This, sadly, is *still* an
oversimplification. Unicode now has been extended to handle ancient
Chinese, Korean, and Japanese texts, which had so many different
characters that the 2-byte unicode system could not represent them all.
But Python doesn't currently support that out of the box, and I don't
know if there is a project afoot to add it. You've reached the limits of
my expertise, sorry.

  

