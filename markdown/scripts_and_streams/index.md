

Chapter 10. Scripts and Streams
-------------------------------

-   [10.1. Abstracting input sources](index.html#kgp.openanything)
-   [10.2. Standard input, output, and error](stdin_stdout_stderr.html)
-   [10.3. Caching node lookups](caching.html)
-   [10.4. Finding direct children of a node](child_nodes.html)
-   [10.5. Creating separate handlers by node
    type](handlers_by_node_type.html)
-   [10.6. Handling command-line arguments](command_line_arguments.html)
-   [10.7. Putting it all together](all_together.html)
-   [10.8. Summary](summary.html)

10.1. Abstracting input sources
-------------------------------

One of Python's greatest strengths is its dynamic binding, and one
powerful use of dynamic binding is the *file-like object*.

Many functions which require an input source could simply take a
filename, go open the file for reading, read it, and close it when
they're done. But they don't. Instead, they take a *file-like object*.

In the simplest case, a *file-like object* is any object with a `read`
method with an optional `size` parameter, which returns a string. When
called with no `size` parameter, it reads everything there is to read
from the input source and returns all the data as a single string. When
called with a `size` parameter, it reads that much from the input source
and returns that much data; when called again, it picks up where it left
off and returns the next chunk of data.

This is how [reading from real
files](../file_handling/file_objects.html "6.2. Working with File Objects")
works; the difference is that you're not limiting yourself to real
files. The input source could be anything: a file on disk, a web page,
even a hard-coded string. As long as you pass a file-like object to the
function, and the function simply calls the object's `read` method, the
function can handle any kind of input source without specific code to
handle each kind.

In case you were wondering how this relates to XML processing,
`minidom.parse` is one such function which can take a file-like object.

### Example 10.1. Parsing XML from a file

    >>> from xml.dom import minidom
    >>> fsock = open('binary.xml')    
    >>> xmldoc = minidom.parse(fsock) 
    >>> fsock.close()                 
    >>> print xmldoc.toxml()          
    <?xml version="1.0" ?>
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



[![1](../images/callouts/1.png)](#kgp.openanything.1.1) First, you open the file on disk. This gives you a [file object](../file_handling/file_objects.html "6.2. Working with File Objects"). 

[![2](../images/callouts/2.png)](#kgp.openanything.1.2) You pass the file object to `minidom.parse`, which calls the `read` method of `fsock` and reads the XML document from the file on disk. 

[![3](../images/callouts/3.png)](#kgp.openanything.1.3) Be sure to call the `close` method of the file object after you're done with it. `minidom.parse` will not do this for you. 

[![4](../images/callouts/4.png)](#kgp.openanything.1.4) Calling the `toxml()` method on the returned XML document prints out the entire thing. 

Well, that all seems like a colossal waste of time. After all, you've
already seen that `minidom.parse` can simply take the filename and do
all the opening and closing nonsense automatically. And it's true that
if you know you're just going to be parsing a local file, you can pass
the filename and `minidom.parse` is smart enough to Do The Right Thing™.
But notice how similar -- and easy -- it is to parse an XML document
straight from the Internet.

### Example 10.2. Parsing XML from a URL

    >>> import urllib
    >>> usock = urllib.urlopen('http://slashdot.org/slashdot.rdf') 
    >>> xmldoc = minidom.parse(usock)                              
    >>> usock.close()                                              
    >>> print xmldoc.toxml()                                       
    <?xml version="1.0" ?>
    <rdf:RDF xmlns="http://my.netscape.com/rdf/simple/0.9/"
     xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

    <channel>
    <title>Slashdot</title>
    <link>http://slashdot.org/</link>
    <description>News for nerds, stuff that matters</description>
    </channel>

    <image>
    <title>Slashdot</title>
    <url>http://images.slashdot.org/topics/topicslashdot.gif</url>
    <link>http://slashdot.org/</link>
    </image>

    <item>
    <title>To HDTV or Not to HDTV?</title>
    <link>http://slashdot.org/article.pl?sid=01/12/28/0421241</link>
    </item>

    [...snip...]



[![1](../images/callouts/1.png)](#kgp.openanything.2.1) As you saw [in a previous chapter](../html_processing/extracting_data.html#dialect.extract.urllib "Example 8.5. Introducing urllib"), `urlopen` takes a web page URL and returns a file-like object. Most importantly, this object has a `read` method which returns the HTML source of the web page. 

[![2](../images/callouts/2.png)](#kgp.openanything.2.2) Now you pass the file-like object to `minidom.parse`, which obediently calls the `read` method of the object and parses the XML data that the `read` method returns. The fact that this XML data is now coming straight from a web page is completely irrelevant. `minidom.parse` doesn't know about web pages, and it doesn't care about web pages; it just knows about file-like objects. 

[![3](../images/callouts/3.png)](#kgp.openanything.2.3) As soon as you're done with it, be sure to close the file-like object that `urlopen` gives you. 

[![4](../images/callouts/4.png)](#kgp.openanything.2.4) By the way, this URL is real, and it really is XML. It's an XML representation of the current headlines on [Slashdot](http://slashdot.org/), a technical news and gossip site. 

### Example 10.3. Parsing XML from a string (the easy but inflexible way)

    >>> contents = "<grammar><ref id='bit'><p>0</p><p>1</p></ref></grammar>"
    >>> xmldoc = minidom.parseString(contents) 
    >>> print xmldoc.toxml()
    <?xml version="1.0" ?>
    <grammar><ref id="bit"><p>0</p><p>1</p></ref></grammar>



[![1](../images/callouts/1.png)](#kgp.openanything.3.1) `minidom` has a method, `parseString`, which takes an entire XML document as a string and parses it. You can use this instead of `minidom.parse` if you know you already have your entire XML document in a string. 

OK, so you can use the `minidom.parse` function for parsing both local
files and remote URLs, but for parsing strings, you use... a different
function. That means that if you want to be able to take input from a
file, a URL, or a string, you'll need special logic to check whether
it's a string, and call the `parseString` function instead. How
unsatisfying.

If there were a way to turn a string into a file-like object, then you
could simply pass this object to `minidom.parse`. And in fact, there is
a module specifically designed for doing just that: `StringIO`.

### Example 10.4. Introducing `StringIO`

    >>> contents = "<grammar><ref id='bit'><p>0</p><p>1</p></ref></grammar>"
    >>> import StringIO
    >>> ssock = StringIO.StringIO(contents)   
    >>> ssock.read()                          
    "<grammar><ref id='bit'><p>0</p><p>1</p></ref></grammar>"
    >>> ssock.read()                          
    ''
    >>> ssock.seek(0)                         
    >>> ssock.read(15)                        
    '<grammar><ref i'
    >>> ssock.read(15)
    "d='bit'><p>0</p"
    >>> ssock.read()
    '><p>1</p></ref></grammar>'
    >>> ssock.close()                         



[![1](../images/callouts/1.png)](#kgp.openanything.4.1) The `StringIO` module contains a single class, also called `StringIO`, which allows you to turn a string into a file-like object. The `StringIO` class takes the string as a parameter when creating an instance. 

[![2](../images/callouts/2.png)](#kgp.openanything.4.2) Now you have a file-like object, and you can do all sorts of file-like things with it. Like `read`, which returns the original string. 

[![3](../images/callouts/3.png)](#kgp.openanything.4.3) Calling `read` again returns an empty string. This is how real file objects work too; once you read the entire file, you can't read any more without explicitly seeking to the beginning of the file. The `StringIO` object works the same way. 

[![4](../images/callouts/4.png)](#kgp.openanything.4.4) You can explicitly seek to the beginning of the string, just like seeking through a file, by using the `seek` method of the `StringIO` object. 

[![5](../images/callouts/5.png)](#kgp.openanything.4.5) You can also read the string in chunks, by passing a `size` parameter to the `read` method. 

[![6](../images/callouts/6.png)](#kgp.openanything.4.6) At any time, `read` will return the rest of the string that you haven't read yet. All of this is exactly how file objects work; hence the term *file-like object*. 

### Example 10.5. Parsing XML from a string (the file-like object way)

    >>> contents = "<grammar><ref id='bit'><p>0</p><p>1</p></ref></grammar>"
    >>> ssock = StringIO.StringIO(contents)
    >>> xmldoc = minidom.parse(ssock) 
    >>> ssock.close()
    >>> print xmldoc.toxml()
    <?xml version="1.0" ?>
    <grammar><ref id="bit"><p>0</p><p>1</p></ref></grammar>



[![1](../images/callouts/1.png)](#kgp.openanything.5.1) Now you can pass the file-like object (really a `StringIO`) to `minidom.parse`, which will call the object's `read` method and happily parse away, never knowing that its input came from a hard-coded string. 

So now you know how to use a single function, `minidom.parse`, to parse
an XML document stored on a web page, in a local file, or in a
hard-coded string. For a web page, you use `urlopen` to get a file-like
object; for a local file, you use `open`; and for a string, you use
`StringIO`. Now let's take it one step further and generalize *these*
differences as well.

### Example 10.6. `openAnything`

    def openAnything(source):                  
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



[![1](../images/callouts/1.png)](#kgp.openanything.6.1) The `openAnything` function takes a single parameter, `source`, and returns a file-like object. `source` is a string of some sort; it can either be a URL (like `'http://slashdot.org/slashdot.rdf'`), a full or partial pathname to a local file (like `'binary.xml'`), or a string that contains actual XML data to be parsed. 

[![2](../images/callouts/2.png)](#kgp.openanything.6.2) First, you see if `source` is a URL. You do this through brute force: you try to open it as a URL and silently ignore errors caused by trying to open something which is not a URL. This is actually elegant in the sense that, if `urllib` ever supports new types of URLs in the future, you will also support them without recoding. If `urllib` is able to open `source`, then the `return` kicks you out of the function immediately and the following `try` statements never execute. 

[![3](../images/callouts/3.png)](#kgp.openanything.6.3) On the other hand, if `urllib` yelled at you and told you that `source` wasn't a valid URL, you assume it's a path to a file on disk and try to open it. Again, you don't do anything fancy to check whether `source` is a valid filename or not (the rules for valid filenames vary wildly between different platforms anyway, so you'd probably get them wrong anyway). Instead, you just blindly open the file, and silently trap any errors. 

[![4](../images/callouts/4.png)](#kgp.openanything.6.4) By this point, you need to assume that `source` is a string that has hard-coded data in it (since nothing else worked), so you use `StringIO` to create a file-like object out of it and return that. (In fact, since you're using the `str` function, `source` doesn't even need to be a string; it could be any object, and you'll use its string representation, as defined by its `__str__` [special method](../object_oriented_framework/special_class_methods2.html "5.7. Advanced Special Class Methods").) 

Now you can use this `openAnything` function in conjunction with
`minidom.parse` to make a function that takes a `source` that refers to
an XML document somehow (either as a URL, or a local filename, or a
hard-coded XML document in a string) and parses it.

### Example 10.7. Using `openAnything` in `kgp.py`

    class KantGenerator:
        def _load(self, source):
            sock = toolbox.openAnything(source)
            xmldoc = minidom.parse(sock).documentElement
            sock.close()
            return xmldoc

  

