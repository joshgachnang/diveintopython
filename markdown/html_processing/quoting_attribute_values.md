

8.7. Quoting attribute values
-----------------------------

A common question on
[comp.lang.python](http://groups.google.com/groups?group=comp.lang.python)
is “I have a bunch of HTML documents with unquoted attribute values, and
I want to properly quote them all. How can I do
this?”<sup>[[4](#ftn.d0e21764)]</sup> (This is generally precipitated by
a project manager who has found the HTML-is-a-standard religion joining
a large project and proclaiming that all pages must validate against an
HTML validator. Unquoted attribute values are a common violation of the
HTML standard.) Whatever the reason, unquoted attribute values are easy
to fix by feeding HTML through `BaseHTMLProcessor`.

`BaseHTMLProcessor` consumes HTML (since it's descended from
`SGMLParser`) and produces equivalent HTML, but the HTML output is not
identical to the input. Tags and attribute names will end up in
lowercase, even if they started in uppercase or mixed case, and
attribute values will be enclosed in double quotes, even if they started
in single quotes or with no quotes at all. It is this last side effect
that you can take advantage of.

### Example 8.16. Quoting attribute values

    >>> htmlSource = """        
    ...     <html>
    ...     <head>
    ...     <title>Test page</title>
    ...     </head>
    ...     <body>
    ...     <ul>
    ...     <li><a href=index.html>Home</a></li>
    ...     <li><a href=toc.html>Table of contents</a></li>
    ...     <li><a href=history.html>Revision history</a></li>
    ...     </body>
    ...     </html>
    ...     """
    >>> from BaseHTMLProcessor import BaseHTMLProcessor
    >>> parser = BaseHTMLProcessor()
    >>> parser.feed(htmlSource) 
    >>> print parser.output()   
    <html>
    <head>
    <title>Test page</title>
    </head>
    <body>
    <ul>
    <li><a href="index.html">Home</a></li>
    <li><a href="toc.html">Table of contents</a></li>
    <li><a href="history.html">Revision history</a></li>
    </body>
    </html>



[![1](../images/callouts/1.png)](#dialect.basehtml.3.1) Note that the attribute values of the `href` attributes in the `<a>` tags are not properly quoted. (Also note that you're using [triple quotes](../getting_to_know_python/documenting_functions.html#odbchelper.triplequotes "Example 2.2. Defining the buildConnectionString Function's doc string") for something other than a `doc string`. And directly in the IDE, no less. They're very useful.) 

[![2](../images/callouts/2.png)](#dialect.basehtml.3.2) Feed the parser. 

[![3](../images/callouts/3.png)](#dialect.basehtml.3.3) Using the `output` function defined in `BaseHTMLProcessor`, you get the output as a single string, complete with quoted attribute values. While this may seem anti-climactic, think about how much has actually happened here: `SGMLParser` parsed the entire HTML document, breaking it down into tags, refs, data, and so forth; `BaseHTMLProcessor` used those elements to reconstruct pieces of HTML (which are still stored in `parser.pieces`, if you want to see them); finally, you called `parser.output`, which joined all the pieces of HTML into one string. 

### Footnotes

<sup>[[4](#d0e21764)]</sup>All right, it's not that common a question.
It's not up there with “What editor should I use to write Python code?”
(answer: Emacs) or “Is Python better or worse than Perl?” (answer: “Perl
is worse than Python because people wanted it worse.” -Larry Wall,
10/14/1998) But questions about HTML processing pop up in one form or
another about once a month, and among those questions, this is a popular
one.

  

