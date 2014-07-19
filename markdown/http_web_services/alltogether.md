

11.9. Putting it all together
-----------------------------

You've seen all the pieces for building an intelligent HTTP web services
client. Now let's see how they all fit together.

### Example 11.17. The `openanything` function

This function is defined in `openanything.py`.

    def openAnything(source, etag=None, lastmodified=None, agent=USER_AGENT):
        # non-HTTP code omitted for brevity
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



[![1](../images/callouts/1.png)](#oa.alltogether.1.1) `urlparse` is a handy utility module for, you guessed it, parsing URLs. It's primary function, also called `urlparse`, takes a URL and splits it into a tuple of (scheme, domain, path, params, query string parameters, and fragment identifier). Of these, the only thing you care about is the scheme, to make sure that you're dealing with an HTTP URL (which `urllib2` can handle). 

[![2](../images/callouts/2.png)](#oa.alltogether.1.2) You identify yourself to the HTTP server with the `User-Agent` passed in by the calling function. If no `User-Agent` was specified, you use a default one defined earlier in the `openanything.py` module. You never use the default one defined by `urllib2`. 

[![3](../images/callouts/3.png)](#oa.alltogether.1.3) If an `ETag` hash was given, send it in the `If-None-Match` header. 

[![4](../images/callouts/4.png)](#oa.alltogether.1.4) If a last-modified date was given, send it in the `If-Modified-Since` header. 

[![5](../images/callouts/5.png)](#oa.alltogether.1.5) Tell the server you would like compressed data if possible. 

[![6](../images/callouts/6.png)](#oa.alltogether.1.6) Build a URL opener that uses *both* of the custom URL handlers: `SmartRedirectHandler` for handling `301` and `302` redirects, and `DefaultErrorHandler` for handling `304`, `404`, and other error conditions gracefully. 

[![7](../images/callouts/7.png)](#oa.alltogether.1.7) That's it! Open the URL and return a file-like object to the caller. 

### Example 11.18. The `fetch` function

This function is defined in `openanything.py`.

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



[![1](../images/callouts/1.png)](#oa.alltogether.2.1) First, you call the `openAnything` function with a URL, `ETag` hash, `Last-Modified` date, and `User-Agent`. 

[![2](../images/callouts/2.png)](#oa.alltogether.2.2) Read the actual data returned from the server. This may be compressed; if so, you'll decompress it later. 

[![3](../images/callouts/3.png)](#oa.alltogether.2.3) Save the `ETag` hash returned from the server, so the calling application can pass it back to you next time, and you can pass it on to `openAnything`, which can stick it in the `If-None-Match` header and send it to the remote server. 

[![4](../images/callouts/4.png)](#oa.alltogether.2.4) Save the `Last-Modified` date too. 

[![5](../images/callouts/5.png)](#oa.alltogether.2.5) If the server says that it sent compressed data, decompress it. 

[![6](../images/callouts/6.png)](#oa.alltogether.2.6) If you got a URL back from the server, save it, and assume that the status code is `200` until you find out otherwise. 

[![7](../images/callouts/7.png)](#oa.alltogether.2.7) If one of the custom URL handlers captured a status code, then save that too. 

### Example 11.19. Using `openanything.py`

    >>> import openanything
    >>> useragent = 'MyHTTPWebServicesApp/1.0'
    >>> url = 'http://diveintopython.net/redir/example301.xml'
    >>> params = openanything.fetch(url, agent=useragent)              
    >>> params                                                         
    {'url': 'http://diveintomark.org/xml/atom.xml', 
    'lastmodified': 'Thu, 15 Apr 2004 19:45:21 GMT', 
    'etag': '"e842a-3e53-55d97640"', 
    'status': 301,
    'data': '<?xml version="1.0" encoding="iso-8859-1"?>
    <feed version="0.3"
    <-- rest of data omitted for brevity -->'}
    >>> if params['status'] == 301:                                    
    ...     url = params['url']
    >>> newparams = openanything.fetch(
    ...     url, params['etag'], params['lastmodified'], useragent)    
    >>> newparams
    {'url': 'http://diveintomark.org/xml/atom.xml', 
    'lastmodified': None, 
    'etag': '"e842a-3e53-55d97640"', 
    'status': 304,
    'data': ''}                                                        



[![1](../images/callouts/1.png)](#oa.alltogether.3.1) The very first time you fetch a resource, you don't have an `ETag` hash or `Last-Modified` date, so you'll leave those out. (They're [optional parameters](../power_of_introspection/optional_arguments.html "4.2. Using Optional and Named Arguments").) 

[![2](../images/callouts/2.png)](#oa.alltogether.3.2) What you get back is a dictionary of several useful headers, the HTTP status code, and the actual data returned from the server. `openanything` handles the gzip compression internally; you don't care about that at this level. 

[![3](../images/callouts/3.png)](#oa.alltogether.3.3) If you ever get a `301` status code, that's a permanent redirect, and you need to update your URL to the new address. 

[![4](../images/callouts/4.png)](#oa.alltogether.3.4) The second time you fetch the same resource, you have all sorts of information to pass back: a (possibly updated) URL, the `ETag` from the last time, the `Last-Modified` date from the last time, and of course your `User-Agent`. 

[![5](../images/callouts/5.png)](#oa.alltogether.3.5) What you get back is again a dictionary, but the data hasn't changed, so all you got was a `304` status code and no data. 

  

