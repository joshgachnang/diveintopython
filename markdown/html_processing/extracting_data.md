

8.3. Extracting data from HTML documents
----------------------------------------

To extract data from HTML documents, subclass the `SGMLParser` class and
define methods for each tag or entity you want to capture.

The first step to extracting data from an HTML document is getting some
HTML. If you have some HTML lying around on your hard drive, you can use
[file
functions](http://www.diveintopython.net/file_handling/file_objects.html "6.2. Working with File Objects")
to read it, but the real fun begins when you get HTML from live web
pages.

### Example 8.5. Introducing `urllib`

    >>> import urllib                                       
    >>> sock = urllib.urlopen("http://diveintopython.net/")
    >>> htmlSource = sock.read()                            
    >>> sock.close()                                        
    >>> print htmlSource                                    
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><html><head>
          <meta http-equiv='Content-Type' content='text/html; charset=ISO-8859-1'>
       <title>Dive Into Python</title>
    <link rel='stylesheet' href='diveintopython.css' type='text/css'>
    <link rev='made' href='mailto:mark@diveintopython.net'>
    <meta name='keywords' content='Python, Dive Into Python, tutorial, object-oriented, programming, documentation, book, free'>
    <meta name='description' content='a free Python tutorial for experienced programmers'>
    </head>
    <body bgcolor='white' text='black' link='#0000FF' vlink='#840084' alink='#0000FF'>
    <table cellpadding='0' cellspacing='0' border='0' width='100%'>
    <tr><td class='header' width='1%' valign='top'>diveintopython.net</td>
    <td width='99%' align='right'><hr size='1' noshade></td></tr>
    <tr><td class='tagline' colspan='2'>Python&nbsp;for&nbsp;experienced&nbsp;programmers</td></tr>

    [...snip...]



[![1](http://www.diveintopython.net/images/callouts/1.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.1.1) The `urllib` module is part of the standard Python library. It contains functions for getting information about and actually retrieving data from Internet-based URLs (mainly web pages). 

[![2](http://www.diveintopython.net/images/callouts/2.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.1.2) The simplest use of `urllib` is to retrieve the entire text of a web page using the `urlopen` function. Opening a URL is similar to [opening a file](http://www.diveintopython.net/file_handling/file_objects.html "6.2. Working with File Objects"). The return value of `urlopen` is a file-like object, which has some of the same methods as a file object. 

[![3](http://www.diveintopython.net/images/callouts/3.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.1.3) The simplest thing to do with the file-like object returned by `urlopen` is `read`, which reads the entire HTML of the web page into a single string. The object also supports `readlines`, which reads the text line by line into a list. 

[![4](http://www.diveintopython.net/images/callouts/4.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.1.4) When you're done with the object, make sure to `close` it, just like a normal file object. 

[![5](http://www.diveintopython.net/images/callouts/5.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.1.5) You now have the complete HTML of the home page of `http://diveintopython.net/` in a string, and you're ready to parse it.

### Example 8.6. Introducing `urllister.py`

If you have not already done so, you can [download this and other
examples](http://www.diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    from sgmllib import SGMLParser

    class URLLister(SGMLParser):
        def reset(self):                              
            SGMLParser.reset(self)
            self.urls =

        def start_a(self, attrs):                     
            href = [v for k, v in attrs if k=='href']  
            if href:
                self.urls.extend(href)



[![1](http://www.diveintopython.net/images/callouts/1.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.2.1) `reset` is called by the `__init__` method of `SGMLParser`, and it can also be called manually once an instance of the parser has been created. So if you need to do any initialization, do it in `reset`, not in `__init__`, so that it will be re-initialized properly when someone re-uses a parser instance. 

[![2](http://www.diveintopython.net/images/callouts/2.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.2.2) `start_a` is called by `SGMLParser` whenever it finds an `<a>` tag. The tag may contain an `href` attribute, and/or other attributes, like `name` or `title`. The `attrs` parameter is a list of tuples, `[(attribute, value), (attribute, value), ...]`. Or it may be just an `<a>`, a valid (if useless) HTML tag, in which case `attrs` would be an empty list. 

[![3](http://www.diveintopython.net/images/callouts/3.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.2.3) You can find out whether this `<a>` tag has an `href` attribute with a simple [multi-variable](http://www.diveintopython.net/native_data_types/declaring_variables.html#odbchelper.multiassign "3.4.2. Assigning Multiple Values at Once") [list comprehension](http://www.diveintopython.net/native_data_types/mapping_lists.html "3.6. Mapping Lists"). 

[![4](http://www.diveintopython.net/images/callouts/4.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.2.4) String comparisons like `k=='href'` are always case-sensitive, but that's safe in this case, because `SGMLParser` converts attribute names to lowercase while building `attrs`. 

### Example 8.7. Using `urllister.py`

    >>> import urllib, urllister
    >>> usock = urllib.urlopen("http://diveintopython.net/")
    >>> parser = urllister.URLLister()
    >>> parser.feed(usock.read())         
    >>> usock.close()                     
    >>> parser.close()                    
    >>> for url in parser.urls: print url 
    toc/index.html
    #download
    #languages
    toc/index.html
    appendix/history.html
    download/diveintopython-html-5.0.zip
    download/diveintopython-pdf-5.0.zip
    download/diveintopython-word-5.0.zip
    download/diveintopython-text-5.0.zip
    download/diveintopython-html-flat-5.0.zip
    download/diveintopython-xml-5.0.zip
    download/diveintopython-common-5.0.zip


    ... rest of output omitted for brevity ...



[![1](http://www.diveintopython.net/images/callouts/1.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.3.1) Call the `feed` method, defined in `SGMLParser`, to get HTML into the parser.<sup>[[1](http://www.diveintopython.net/html_processing/extracting_data.html#ftn.d0e20503)]</sup> It takes a string, which is what `usock.read()` returns. 

[![2](http://www.diveintopython.net/images/callouts/2.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.3.2) Like files, you should `close` your URL objects as soon as you're done with them. 

[![3](http://www.diveintopython.net/images/callouts/3.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.3.3) You should `close` your parser object, too, but for a different reason. You've read all the data and fed it to the parser, but the `feed` method isn't guaranteed to have actually processed all the HTML you give it; it may buffer it, waiting for more. Be sure to call `close` to flush the buffer and force everything to be fully parsed. 

[![4](http://www.diveintopython.net/images/callouts/4.png)](http://www.diveintopython.net/html_processing/extracting_data.html#dialect.extract.3.4) Once the parser is `close`d, the parsing is complete, and `parser.urls` contains a list of all the linked URLs in the HTML document. (Your output may look different, if the download links have been updated by the time you read this.) 

### Footnotes

<sup>[[1](http://www.diveintopython.net/html_processing/extracting_data.html#d0e20503)]</sup>The
technical term for a parser like `SGMLParser` is a *consumer*: it
consumes HTML and breaks it down. Presumably, the name `feed` was chosen
to fit into the whole “consumer” motif. Personally, it makes me think of
an exhibit in the zoo where there's just a dark cage with no trees or
plants or evidence of life of any kind, but if you stand perfectly still
and look really closely you can make out two beady eyes staring back at
you from the far left corner, but you convince yourself that that's just
your mind playing tricks on you, and the only way you can tell that the
whole thing isn't just an empty cage is a small innocuous sign on the
railing that reads, “Do not feed the parser.” But maybe that's just me.
In any event, it's an interesting mental image.

