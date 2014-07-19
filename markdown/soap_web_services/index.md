

Chapter 12. SOAP Web Services
-----------------------------

-   [12.1. Diving In](index.html#soap.divein)
-   [12.2. Installing the SOAP Libraries](install.html)
    -   [12.2.1. Installing PyXML](install.html#d0e29967)
    -   [12.2.2. Installing fpconst](install.html#d0e30070)
    -   [12.2.3. Installing SOAPpy](install.html#d0e30171)
-   [12.3. First Steps with SOAP](first_steps.html)
-   [12.4. Debugging SOAP Web Services](debugging.html)
-   [12.5. Introducing WSDL](wsdl.html)
-   [12.6. Introspecting SOAP Web Services with
    WSDL](introspection.html)
-   [12.7. Searching Google](google.html)
-   [12.8. Troubleshooting SOAP Web Services](troubleshooting.html)
-   [12.9. Summary](summary.html)

[Chapter 11](../http_web_services/index.html) focused on
document-oriented web services over HTTP. The “input parameter” was the
URL, and the “return value” was an actual XML document which it was your
responsibility to parse.

This chapter will focus on SOAP web services, which take a more
structured approach. Rather than dealing with HTTP requests and XML
documents directly, SOAP allows you to simulate calling functions that
return native data types. As you will see, the illusion is almost
perfect; you can “call” a function through a SOAP library, with the
standard Python calling syntax, and the function appears to return
Python objects and values. But under the covers, the SOAP library has
actually performed a complex transaction involving multiple XML
documents and a remote server.

SOAP is a complex specification, and it is somewhat misleading to say
that SOAP is all about calling remote functions. Some people would pipe
up to add that SOAP allows for one-way asynchronous message passing, and
document-oriented web services. And those people would be correct; SOAP
can be used that way, and in many different ways. But this chapter will
focus on so-called “RPC-style” SOAP -- calling a remote function and
getting results back.

12.1. Diving In
---------------

You use Google, right? It's a popular search engine. Have you ever
wished you could programmatically access Google search results? Now you
can. Here is a program to search Google from Python.

### Example 12.1. `search.py`

    from SOAPpy import WSDL

    # you'll need to configure these two values;
    # see http://www.google.com/apis/
    WSDLFILE = '/path/to/copy/of/GoogleSearch.wsdl'
    APIKEY = 'YOUR_GOOGLE_API_KEY'

    _server = WSDL.Proxy(WSDLFILE)
    def search(q):
        """Search Google and return list of {title, link, description}"""
        results = _server.doGoogleSearch(
            APIKEY, q, 0, 10, False, "", False, "", "utf-8", "utf-8")
        return [{"title": r.title.encode("utf-8"),
                 "link": r.URL.encode("utf-8"),
                 "description": r.snippet.encode("utf-8")}
                for r in results.resultElements]

    if __name__ == '__main__':
        import sys
        for r in search(sys.argv[1])[:5]:
            print r['title']
            print r['link']
            print r['description']
            print

You can import this as a module and use it from a larger program, or you
can run the script from the command line. On the command line, you give
the search query as a command-line argument, and it prints out the URL,
title, and description of the top five Google search results.

Here is the sample output for a search for the word “python”.

### Example 12.2. Sample Usage of `search.py`

    C:\diveintopython\common\py> python search.py "python"
    <b>Python</b> Programming Language
    http://www.python.org/
    Home page for <b>Python</b>, an interpreted, interactive, object-oriented,
    extensible<br> programming language. <b>...</b> <b>Python</b>
    is OSI Certified Open Source: OSI Certified.

    <b>Python</b> Documentation Index
    http://www.python.org/doc/
     <b>...</b> New-style classes (aka descrintro). Regular expressions. Database
    API. Email Us.<br> docs@<b>python</b>.org. (c) 2004. <b>Python</b>
    Software Foundation. <b>Python</b> Documentation. <b>...</b>

    Download <b>Python</b> Software
    http://www.python.org/download/
    Download Standard <b>Python</b> Software. <b>Python</b> 2.3.3 is the
    current production<br> version of <b>Python</b>. <b>...</b>
    <b>Python</b> is OSI Certified Open Source:

    Pythonline
    http://www.pythonline.com/


    Dive Into <b>Python</b>
    http://diveintopython.net/
    Dive Into <b>Python</b>. <b>Python</b> from novice to pro. Find:
    <b>...</b> It is also available in multiple<br> languages. Read
    Dive Into <b>Python</b>. This book is still being written. <b>...</b>

### Further Reading on SOAP

-   [http://www.xmethods.net/](http://www.xmethods.net/) is a repository
    of public access SOAP web services.
-   The [SOAP specification](http://www.w3.org/TR/soap/) is surprisingly
    readable, if you like that sort of thing.

  

