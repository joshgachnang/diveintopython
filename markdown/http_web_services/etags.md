

11.6. Handling `Last-Modified` and `ETag`
-----------------------------------------

Now that you know how to add custom HTTP headers to your web service
requests, let's look at adding support for `Last-Modified` and `ETag`
headers.

These examples show the output with debugging turned off. If you still
have it turned on from the previous section, you can turn it off by
setting `httplib.HTTPConnection.debuglevel = 0`. Or you can just leave
debugging on, if that helps you.

### Example 11.6. Testing `Last-Modified`

    >>> import urllib2
    >>> request = urllib2.Request('http://diveintomark.org/xml/atom.xml')
    >>> opener = urllib2.build_opener()
    >>> firstdatastream = opener.open(request)
    >>> firstdatastream.headers.dict                       
    {'date': 'Thu, 15 Apr 2004 20:42:41 GMT', 
     'server': 'Apache/2.0.49 (Debian GNU/Linux)', 
     'content-type': 'application/atom+xml',
     'last-modified': 'Thu, 15 Apr 2004 19:45:21 GMT', 
     'etag': '"e842a-3e53-55d97640"',
     'content-length': '15955', 
     'accept-ranges': 'bytes', 
     'connection': 'close'}
    >>> request.add_header('If-Modified-Since',
    ...     firstdatastream.headers.get('Last-Modified'))  
    >>> seconddatastream = opener.open(request)            
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "c:\python23\lib\urllib2.py", line 326, in open
        '_open', req)
      File "c:\python23\lib\urllib2.py", line 306, in _call_chain
        result = func(*args)
      File "c:\python23\lib\urllib2.py", line 901, in http_open
        return self.do_open(httplib.HTTP, req)
      File "c:\python23\lib\urllib2.py", line 895, in do_open
        return self.parent.error('http', req, fp, code, msg, hdrs)
      File "c:\python23\lib\urllib2.py", line 352, in error
        return self._call_chain(*args)
      File "c:\python23\lib\urllib2.py", line 306, in _call_chain
        result = func(*args)
      File "c:\python23\lib\urllib2.py", line 412, in http_error_default
        raise HTTPError(req.get_full_url(), code, msg, hdrs, fp)
    urllib2.HTTPError: HTTP Error 304: Not Modified



[![1](../images/callouts/1.png)](#oa.etags.1.1) Remember all those HTTP headers you saw printed out when you turned on debugging? This is how you can get access to them programmatically: `firstdatastream.headers` is [an object that acts like a dictionary](../object_oriented_framework/userdict.html "5.5. Exploring UserDict: A Wrapper Class") and allows you to get any of the individual headers returned from the HTTP server. 

[![2](../images/callouts/2.png)](#oa.etags.1.2) On the second request, you add the `If-Modified-Since` header with the last-modified date from the first request. If the data hasn't changed, the server should return a `304` status code. 

[![3](../images/callouts/3.png)](#oa.etags.1.3) Sure enough, the data hasn't changed. You can see from the traceback that `urllib2` throws a special exception, `HTTPError`, in response to the `304` status code. This is a little unusual, and not entirely helpful. After all, it's not an error; you specifically asked the server not to send you any data if it hadn't changed, and the data didn't change, so the server told you it wasn't sending you any data. That's not an error; that's exactly what you were hoping for. 

`urllib2` also raises an `HTTPError` exception for conditions that you
would think of as errors, such as `404` (page not found). In fact, it
will raise `HTTPError` for *any* status code other than `200` (OK),
`301` (permanent redirect), or `302` (temporary redirect). It would be
more helpful for your purposes to capture the status code and simply
return it, without throwing an exception. To do that, you'll need to
define a custom URL handler.

### Example 11.7. Defining URL handlers

This custom URL handler is part of `openanything.py`.

    class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):    
        def http_error_default(self, req, fp, code, msg, headers): 
            result = urllib2.HTTPError(                           
                req.get_full_url(), code, msg, headers, fp)       
            result.status = code                                   
            return result                                         



[![1](../images/callouts/1.png)](#oa.etags.2.1) `urllib2` is designed around URL handlers. Each handler is just a class that can define any number of methods. When something happens -- like an HTTP error, or even a `304` code -- `urllib2` introspects into the list of defined handlers for a method that can handle it. You used a similar introspection in [Chapter 9, *XML Processing*](../xml_processing/index.html "Chapter 9. XML Processing") to define handlers for different node types, but `urllib2` is more flexible, and introspects over as many handlers as are defined for the current request. 

[![2](../images/callouts/2.png)](#oa.etags.2.2) `urllib2` searches through the defined handlers and calls the `http_error_default` method when it encounters a `304` status code from the server. By defining a custom error handler, you can prevent `urllib2` from raising an exception. Instead, you create the `HTTPError` object, but return it instead of raising it. 

[![3](../images/callouts/3.png)](#oa.etags.2.3) This is the key part: before returning, you save the status code returned by the HTTP server. This will allow you easy access to it from the calling program. 

### Example 11.8. Using custom URL handlers

    >>> request.headers                           
    {'If-modified-since': 'Thu, 15 Apr 2004 19:45:21 GMT'}
    >>> import openanything
    >>> opener = urllib2.build_opener(
    ...     openanything.DefaultErrorHandler())   
    >>> seconddatastream = opener.open(request)
    >>> seconddatastream.status                   
    304
    >>> seconddatastream.read()                   
    ''



[![1](../images/callouts/1.png)](#oa.etags.3.1) You're continuing the previous example, so the `Request` object is already set up, and you've already added the `If-Modified-Since` header. 

[![2](../images/callouts/2.png)](#oa.etags.3.2) This is the key: now that you've defined your custom URL handler, you need to tell `urllib2` to use it. Remember how I said that `urllib2` broke up the process of accessing an HTTP resource into three steps, and for good reason? This is why building the URL opener is its own step, because you can build it with your own custom URL handlers that override `urllib2`'s default behavior. 

[![3](../images/callouts/3.png)](#oa.etags.3.3) Now you can quietly open the resource, and what you get back is an object that, along with the usual headers (use `seconddatastream.headers.dict` to acess them), also contains the HTTP status code. In this case, as you expected, the status is `304`, meaning this data hasn't changed since the last time you asked for it. 

[![4](../images/callouts/4.png)](#oa.etags.3.4) Note that when the server sends back a `304` status code, it doesn't re-send the data. That's the whole point: to save bandwidth by not re-downloading data that hasn't changed. So if you actually want that data, you'll need to cache it locally the first time you get it. 

Handling `ETag` works much the same way, but instead of checking for
`Last-Modified` and sending `If-Modified-Since`, you check for `ETag`
and send `If-None-Match`. Let's start with a fresh IDE session.

### Example 11.9. Supporting `ETag`/`If-None-Match`

    >>> import urllib2, openanything
    >>> request = urllib2.Request('http://diveintomark.org/xml/atom.xml')
    >>> opener = urllib2.build_opener(
    ...     openanything.DefaultErrorHandler())
    >>> firstdatastream = opener.open(request)
    >>> firstdatastream.headers.get('ETag')        
    '"e842a-3e53-55d97640"'
    >>> firstdata = firstdatastream.read()
    >>> print firstdata                            
    <?xml version="1.0" encoding="iso-8859-1"?>
    <feed version="0.3"
      xmlns="http://purl.org/atom/ns#"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xml:lang="en">
      <title mode="escaped">dive into mark</title>
      <link rel="alternate" type="text/html" href="http://diveintomark.org/"/>
      <-- rest of feed omitted for brevity -->
    >>> request.add_header('If-None-Match',
    ...     firstdatastream.headers.get('ETag'))   
    >>> seconddatastream = opener.open(request)
    >>> seconddatastream.status                    
    304
    >>> seconddatastream.read()                    
    ''



[![1](../images/callouts/1.png)](#oa.etags.4.1) Using the `firstdatastream.headers` pseudo-dictionary, you can get the `ETag` returned from the server. (What happens if the server didn't send back an `ETag`? Then this line would return `None`.) 

[![2](../images/callouts/2.png)](#oa.etags.4.2) OK, you got the data. 

[![3](../images/callouts/3.png)](#oa.etags.4.3) Now set up the second call by setting the `If-None-Match` header to the `ETag` you got from the first call. 

[![4](../images/callouts/4.png)](#oa.etags.4.4) The second call succeeds quietly (without throwing an exception), and once again you see that the server has sent back a `304` status code. Based on the `ETag` you sent the second time, it knows that the data hasn't changed. 

[![5](../images/callouts/5.png)](#oa.etags.4.5) Regardless of whether the `304` is triggered by `Last-Modified` date checking or `ETag` hash matching, you'll never get the data along with the `304`. That's the whole point. 


![Note](../images/note.png) 
In these examples, the HTTP server has supported both `Last-Modified` and `ETag` headers, but not all servers do. As a web services client, you should be prepared to support both, but you must code defensively in case a server only supports one or the other, or neither. 

  

