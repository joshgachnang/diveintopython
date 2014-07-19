

Chapter 11. HTTP Web Services
-----------------------------

-   [11.1. Diving in](index.html#oa.divein)
-   [11.2. How not to fetch data over HTTP](review.html)
-   [11.3. Features of HTTP](http_features.html)
    -   [11.3.1. User-Agent](http_features.html#d0e27596)
    -   [11.3.2. Redirects](http_features.html#d0e27616)
    -   [11.3.3.
        Last-Modified/If-Modified-Since](http_features.html#d0e27689)
    -   [11.3.4. ETag/If-None-Match](http_features.html#d0e27724)
    -   [11.3.5. Compression](http_features.html#d0e27752)
-   [11.4. Debugging HTTP web services](debugging.html)
-   [11.5. Setting the User-Agent](user_agent.html)
-   [11.6. Handling Last-Modified and ETag](etags.html)
-   [11.7. Handling redirects](redirects.html)
-   [11.8. Handling compressed data](gzip_compression.html)
-   [11.9. Putting it all together](alltogether.html)
-   [11.10. Summary](summary.html)

11.1. Diving in
---------------

You've learned about [HTML
processing](../html_processing/index.html "Chapter 8. HTML Processing")
and [XML
processing](../xml_processing/index.html "Chapter 9. XML Processing"),
and along the way you saw [how to download a web
page](../html_processing/extracting_data.html#dialect.extract.urllib "Example 8.5. Introducing urllib")
and [how to parse XML from a
URL](../scripts_and_streams/index.html#kgp.openanything.urllib "Example 10.2. Parsing XML from a URL"),
but let's dive into the more general topic of HTTP web services.

Simply stated, HTTP web services are programmatic ways of sending and
receiving data from remote servers using the operations of HTTP
directly. If you want to get data from the server, use a straight HTTP
GET; if you want to send new data to the server, use HTTP POST. (Some
more advanced HTTP web service APIs also define ways of modifying
existing data and deleting data, using HTTP PUT and HTTP DELETE.) In
other words, the “verbs” built into the HTTP protocol (GET, POST, PUT,
and DELETE) map directly to application-level operations for receiving,
sending, modifying, and deleting data.

The main advantage of this approach is simplicity, and its simplicity
has proven popular with a lot of different sites. Data -- usually XML
data -- can be built and stored statically, or generated dynamically by
a server-side script, and all major languages include an HTTP library
for downloading it. Debugging is also easier, because you can load up
the web service in any web browser and see the raw data. Modern browsers
will even nicely format and pretty-print XML data for you, to allow you
to quickly navigate through it.

Examples of pure XML-over-HTTP web services:

-   [Amazon API](http://www.amazon.com/webservices) allows you to
    retrieve product information from the Amazon.com online store.
-   [National Weather Service](http://www.nws.noaa.gov/alerts/) (United
    States) and [Hong Kong Observatory](http://demo.xml.weather.gov.hk/)
    (Hong Kong) offer weather alerts as a web service.
-   [Atom API](http://atomenabled.org/) for managing web-based content.
-   [Syndicated feeds](http://syndic8.com/) from weblogs and news sites
    bring you up-to-the-minute news from a variety of sites.

In later chapters, you'll explore APIs which use HTTP as a transport for
sending and receiving data, but don't map application semantics to the
underlying HTTP semantics. (They tunnel everything over HTTP POST.) But
this chapter will concentrate on using HTTP GET to get data from a
remote server, and you'll explore several HTTP features you can use to
get the maximum benefit out of pure HTTP web services.

Here is a more advanced version of the `openanything` module that you
saw in [the previous
chapter](../scripts_and_streams/index.html "Chapter 10. Scripts and Streams"):

### Example 11.1. `openanything.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    import urllib2, urlparse, gzip
    from StringIO import StringIO

    USER_AGENT = 'OpenAnything/1.0 +http://diveintopython.net/http_web_services/'

    class SmartRedirectHandler(urllib2.HTTPRedirectHandler):    
        def http_error_301(self, req, fp, code, msg, headers):  
            result = urllib2.HTTPRedirectHandler.http_error_301(
                self, req, fp, code, msg, headers)              
            result.status = code                                
            return result                                       

        def http_error_302(self, req, fp, code, msg, headers):  
            result = urllib2.HTTPRedirectHandler.http_error_302(
                self, req, fp, code, msg, headers)              
            result.status = code                                
            return result                                       

    class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):   
        def http_error_default(self, req, fp, code, msg, headers):
            result = urllib2.HTTPError(                           
                req.get_full_url(), code, msg, headers, fp)       
            result.status = code                                  
            return result                                         

    def openAnything(source, etag=None, lastmodified=None, agent=USER_AGENT):
        '''URL, filename, or string --> stream

        This function lets you define parsers that take any input source
        (URL, pathname to local or network file, or actual data as a string)
        and deal with it in a uniform manner.  Returned object is guaranteed
        to have all the basic stdio read methods (read, readline, readlines).
        Just .close() the object when you're done with it.

        If the etag argument is supplied, it will be used as the value of an
        If-None-Match request header.

        If the lastmodified argument is supplied, it must be a formatted
        date/time string in GMT (as returned in the Last-Modified header of
        a previous request).  The formatted date/time will be used
        as the value of an If-Modified-Since request header.

        If the agent argument is supplied, it will be used as the value of a
        User-Agent request header.
        '''

        if hasattr(source, 'read'):
            return source

        if source == '-':
            return sys.stdin

        if urlparse.urlparse(source)[0] == 'http':                                      
            # open URL with urllib2                                                     
            request = urllib2.Request(source)                                           
            request.add_header('User-Agent', agent)                                     
            if etag:                                                                    
                request.add_header('If-None-Match', etag)                               
            if lastmodified:                                                            
                request.add_header('If-Modified-Since', lastmodified)                   
            request.add_header('Accept-encoding', 'gzip')                               
            opener = urllib2.build_opener(SmartRedirectHandler(), DefaultErrorHandler())
            return opener.open(request)                                                 
        
        # try to open with native open function (if source is a filename)
        try:
            return open(source)
        except (IOError, OSError):
            pass

        # treat source as string
        return StringIO(str(source))

    def fetch(source, etag=None, last_modified=None, agent=USER_AGENT):  
        '''Fetch data and metadata from a URL, file, stream, or string'''
        result = {}                                                      
        f = openAnything(source, etag, last_modified, agent)             
        result['data'] = f.read()                                        
        if hasattr(f, 'headers'):                                        
            # save ETag, if the server sent one                          
            result['etag'] = f.headers.get('ETag')                       
            # save Last-Modified header, if the server sent one          
            result['lastmodified'] = f.headers.get('Last-Modified')      
            if f.headers.get('content-encoding', '') == 'gzip':          
                # data came back gzip-compressed, decompress it          
                result['data'] = gzip.GzipFile(fileobj=StringIO(result['data']])).read()
        if hasattr(f, 'url'):                                            
            result['url'] = f.url                                        
            result['status'] = 200                                       
        if hasattr(f, 'status'):                                         
            result['status'] = f.status                                  
        f.close()                                                        
        return result                                                    

### Further reading

-   Paul Prescod believes that [pure HTTP web services are the future of
    the
    Internet](http://webservices.xml.com/pub/a/ws/2002/02/06/rest.html).

  

