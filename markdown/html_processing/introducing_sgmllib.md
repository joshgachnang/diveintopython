

8.2. Introducing `sgmllib.py`
-----------------------------

HTML processing is broken into three steps: breaking down the HTML into
its constituent pieces, fiddling with the pieces, and reconstructing the
pieces into HTML again. The first step is done by `sgmllib.py`, a part
of the standard Python library.

The key to understanding this chapter is to realize that HTML is not
just text, it is structured text. The structure is derived from the
more-or-less-hierarchical sequence of start tags and end tags. Usually
you don't work with HTML this way; you work with it *textually* in a
text editor, or *visually* in a web browser or web authoring tool.
`sgmllib.py` presents HTML *structurally*.

`sgmllib.py` contains one important class: `SGMLParser`. `SGMLParser`
parses HTML into useful pieces, like start tags and end tags. As soon as
it succeeds in breaking down some data into a useful piece, it calls a
method on itself based on what it found. In order to use the parser, you
subclass the `SGMLParser` class and override these methods. This is what
I meant when I said that it presents HTML *structurally*: the structure
of the HTML determines the sequence of method calls and the arguments
passed to each method.

`SGMLParser` parses HTML into 8 kinds of data, and calls a separate
method for each of them:

Start tag
:   An HTML tag that starts a block, like `<html>`, `<head>`, `<body>`,
    or `<pre>`, or a standalone tag like `<br>` or `<img>`. When it
    finds a start tag *`tagname`*, `SGMLParser` will look for a method
    called `start_tagname` or `do_tagname`. For instance, when it finds
    a `<pre>` tag, it will look for a `start_pre` or `do_pre` method. If
    found, `SGMLParser` calls this method with a list of the tag's
    attributes; otherwise, it calls `unknown_starttag` with the tag name
    and list of attributes.
End tag
:   An HTML tag that ends a block, like `</html>`, `</head>`, `</body>`,
    or `</pre>`. When it finds an end tag, `SGMLParser` will look for a
    method called `end_tagname`. If found, `SGMLParser` calls this
    method, otherwise it calls `unknown_endtag` with the tag name.
Character reference
:   An escaped character referenced by its decimal or hexadecimal
    equivalent, like `&#160;`. When found, `SGMLParser` calls
    `handle_charref` with the text of the decimal or hexadecimal
    character equivalent.
Entity reference
:   An HTML entity, like `&copy;`. When found, `SGMLParser` calls
    `handle_entityref` with the name of the HTML entity.
Comment
:   An HTML comment, enclosed in `<!-- ... -->`. When found,
    `SGMLParser` calls `handle_comment` with the body of the comment.
Processing instruction
:   An HTML processing instruction, enclosed in `<? ... >`. When found,
    `SGMLParser` calls `handle_pi` with the body of the processing
    instruction.
Declaration
:   An HTML declaration, such as a `DOCTYPE`, enclosed in `<! ... >`.
    When found, `SGMLParser` calls `handle_decl` with the body of the
    declaration.
Text data
:   A block of text. Anything that doesn't fit into the other 7
    categories. When found, `SGMLParser` calls `handle_data` with the
    text.


![Important](../images/important.png) 
Python 2.0 had a bug where `SGMLParser` would not recognize declarations at all (`handle_decl` would never be called), which meant that `DOCTYPE`s were silently ignored. This is fixed in Python 2.1. 

`sgmllib.py` comes with a test suite to illustrate this. You can run
`sgmllib.py`, passing the name of an HTML file on the command line, and
it will print out the tags and other elements as it parses them. It does
this by subclassing the `SGMLParser` class and defining
`unknown_starttag`, `unknown_endtag`, `handle_data` and other methods
which simply print their arguments.


![Tip](../images/tip.png) 
In the ActivePython IDE on Windows, you can specify command line arguments in the “Run script” dialog. Separate multiple arguments with spaces. 

### Example 8.4. Sample test of `sgmllib.py`

Here is a snippet from the table of contents of the HTML version of this
book. Of course your paths may vary. (If you haven't downloaded the HTML
version of the book, you can do so at
[http://diveintopython.net/](http://diveintopython.net/).

    c:\python23\lib> type "c:\downloads\diveintopython\html\toc\index.html"

    <!DOCTYPE html
      PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
    <html lang="en">
       <head>
          <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
       
          <title>Dive Into Python</title>
          <link rel="stylesheet" href="diveintopython.css" type="text/css">

    ... rest of file omitted for brevity ...

Running this through the test suite of `sgmllib.py` yields this output:

    c:\python23\lib> python sgmllib.py "c:\downloads\diveintopython\html\toc\index.html"
    data: '\n\n'
    start tag: <html lang="en" >
    data: '\n   '
    start tag: <head>
    data: '\n      '
    start tag: <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" >
    data: '\n   \n      '
    start tag: <title>
    data: 'Dive Into Python'
    end tag: </title>
    data: '\n      '
    start tag: <link rel="stylesheet" href="diveintopython.css" type="text/css" >
    data: '\n      '

    ... rest of output omitted for brevity ...

Here's the roadmap for the rest of the chapter:

-   Subclass `SGMLParser` to create classes that extract interesting
    data out of HTML documents.
-   Subclass `SGMLParser` to create `BaseHTMLProcessor`, which overrides
    all 8 handler methods and uses them to reconstruct the original HTML
    from the pieces.
-   Subclass `BaseHTMLProcessor` to create `Dialectizer`, which adds
    some methods to process specific HTML tags specially, and overrides
    the `handle_data` method to provide a framework for processing the
    text blocks between the HTML tags.
-   Subclass `Dialectizer` to create classes that define text processing
    rules used by `Dialectizer.handle_data`.
-   Write a test suite that grabs a real web page from
    `http://diveintopython.net/` and processes it.

Along the way, you'll also learn about `locals`, `globals`, and
dictionary-based string formatting.

  

