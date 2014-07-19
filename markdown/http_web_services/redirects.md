

11.7. Handling redirects
------------------------

You can support permanent and temporary redirects using a different kind
of custom URL handler.

First, let's see why a redirect handler is necessary in the first place.

### Example 11.10. Accessing web services without a redirect handler

    >>> import urllib2, httplib
    >>> httplib.HTTPConnection.debuglevel = 1           
    >>> request = urllib2.Request(
    ...     'http://diveintomark.org/redir/example301.xml') 
    >>> opener = urllib2.build_opener()
    >>> f = opener.open(request)
    connect: (diveintomark.org, 80)
    send: '
    GET /redir/example301.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 301 Moved Permanently\r\n'             
    header: Date: Thu, 15 Apr 2004 22:06:25 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Location: http://diveintomark.org/xml/atom.xml  
    header: Content-Length: 338
    header: Connection: close
    header: Content-Type: text/html; charset=iso-8859-1
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0                              
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Thu, 15 Apr 2004 22:06:25 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Last-Modified: Thu, 15 Apr 2004 19:45:21 GMT
    header: ETag: "e842a-3e53-55d97640"
    header: Accept-Ranges: bytes
    header: Content-Length: 15955
    header: Connection: close
    header: Content-Type: application/atom+xml
    >>> f.url                                               
    'http://diveintomark.org/xml/atom.xml'
    >>> f.headers.dict
    {'content-length': '15955', 
    'accept-ranges': 'bytes', 
    'server': 'Apache/2.0.49 (Debian GNU/Linux)', 
    'last-modified': 'Thu, 15 Apr 2004 19:45:21 GMT', 
    'connection': 'close', 
    'etag': '"e842a-3e53-55d97640"', 
    'date': 'Thu, 15 Apr 2004 22:06:25 GMT', 
    'content-type': 'application/atom+xml'}
    >>> f.status
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    AttributeError: addinfourl instance has no attribute 'status'



[![1](../images/callouts/1.png)](#oa.redirect.1.0) You'll be better able to see what's happening if you turn on debugging. 

[![2](../images/callouts/2.png)](#oa.redirect.1.1) This is a URL which I have set up to permanently redirect to my Atom feed at `http://diveintomark.org/xml/atom.xml`. 

[![3](../images/callouts/3.png)](#oa.redirect.1.2) Sure enough, when you try to download the data at that address, the server sends back a `301` status code, telling you that the resource has moved permanently. 

[![4](../images/callouts/4.png)](#oa.redirect.1.3) The server also sends back a `Location:` header that gives the new address of this data. 

[![5](../images/callouts/5.png)](#oa.redirect.1.4) `urllib2` notices the redirect status code and automatically tries to retrieve the data at the new location specified in the `Location:` header. 

[![6](../images/callouts/6.png)](#oa.redirect.1.5) The object you get back from the `opener` contains the new permanent address and all the headers returned from the second request (retrieved from the new permanent address). But the status code is missing, so you have no way of knowing programmatically whether this redirect was temporary or permanent. And that matters very much: if it was a temporary redirect, then you should continue to ask for the data at the old location. But if it was a permanent redirect (as this was), you should ask for the data at the new location from now on. 

This is suboptimal, but easy to fix. `urllib2` doesn't behave exactly as
you want it to when it encounters a `301` or `302`, so let's override
its behavior. How? With a custom URL handler, [just like you did to
handle `304` codes](etags.html "11.6. Handling Last-Modified and ETag").

### Example 11.11. Defining the redirect handler

This class is defined in `openanything.py`.

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



[![1](../images/callouts/1.png)](#oa.redirect.2.1) Redirect behavior is defined in `urllib2` in a class called `HTTPRedirectHandler`. You don't want to completely override the behavior, you just want to extend it a little, so you'll subclass `HTTPRedirectHandler` so you can call the ancestor class to do all the hard work. 

[![2](../images/callouts/2.png)](#oa.redirect.2.2) When it encounters a `301` status code from the server, `urllib2` will search through its handlers and call the `http_error_301` method. The first thing ours does is just call the `http_error_301` method in the ancestor, which handles the grunt work of looking for the `Location:` header and following the redirect to the new address. 

[![3](../images/callouts/3.png)](#oa.redirect.2.3) Here's the key: before you return, you store the status code (`301`), so that the calling program can access it later. 

[![4](../images/callouts/4.png)](#oa.redirect.2.4) Temporary redirects (status code `302`) work the same way: override the `http_error_302` method, call the ancestor, and save the status code before returning. 

So what has this bought us? You can now build a URL opener with the
custom redirect handler, and it will still automatically follow
redirects, but now it will also expose the redirect status code.

### Example 11.12. Using the redirect handler to detect permanent redirects

    >>> request = urllib2.Request('http://diveintomark.org/redir/example301.xml')
    >>> import openanything, httplib
    >>> httplib.HTTPConnection.debuglevel = 1
    >>> opener = urllib2.build_opener(
    ...     openanything.SmartRedirectHandler())           
    >>> f = opener.open(request)
    connect: (diveintomark.org, 80)
    send: 'GET /redir/example301.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 301 Moved Permanently\r\n'            
    header: Date: Thu, 15 Apr 2004 22:13:21 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Location: http://diveintomark.org/xml/atom.xml
    header: Content-Length: 338
    header: Connection: close
    header: Content-Type: text/html; charset=iso-8859-1
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Thu, 15 Apr 2004 22:13:21 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Last-Modified: Thu, 15 Apr 2004 19:45:21 GMT
    header: ETag: "e842a-3e53-55d97640"
    header: Accept-Ranges: bytes
    header: Content-Length: 15955
    header: Connection: close
    header: Content-Type: application/atom+xml

    >>> f.status                                           
    301
    >>> f.url
    'http://diveintomark.org/xml/atom.xml'



[![1](../images/callouts/1.png)](#oa.redirect.3.1) First, build a URL opener with the redirect handler you just defined. 

[![2](../images/callouts/2.png)](#oa.redirect.3.2) You sent off a request, and you got a `301` status code in response. At this point, the `http_error_301` method gets called. You call the ancestor method, which follows the redirect and sends a request at the new location (`http://diveintomark.org/xml/atom.xml`). 

[![3](../images/callouts/3.png)](#oa.redirect.3.3) This is the payoff: now, not only do you have access to the new URL, but you have access to the redirect status code, so you can tell that this was a permanent redirect. The next time you request this data, you should request it from the new location (`http://diveintomark.org/xml/atom.xml`, as specified in `f.url`). If you had stored the location in a configuration file or a database, you need to update that so you don't keep pounding the server with requests at the old address. It's time to update your address book. 

The same redirect handler can also tell you that you *shouldn't* update
your address book.

### Example 11.13. Using the redirect handler to detect temporary redirects

    >>> request = urllib2.Request(
    ...     'http://diveintomark.org/redir/example302.xml')   
    >>> f = opener.open(request)
    connect: (diveintomark.org, 80)
    send: '
    GET /redir/example302.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 302 Found\r\n'                           
    header: Date: Thu, 15 Apr 2004 22:18:21 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Location: http://diveintomark.org/xml/atom.xml
    header: Content-Length: 314
    header: Connection: close
    header: Content-Type: text/html; charset=iso-8859-1
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0                                
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Thu, 15 Apr 2004 22:18:21 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Last-Modified: Thu, 15 Apr 2004 19:45:21 GMT
    header: ETag: "e842a-3e53-55d97640"
    header: Accept-Ranges: bytes
    header: Content-Length: 15955
    header: Connection: close
    header: Content-Type: application/atom+xml
    >>> f.status                                              
    302
    >>> f.url
    http://diveintomark.org/xml/atom.xml



[![1](../images/callouts/1.png)](#oa.redirect.4.1) This is a sample URL I've set up that is configured to tell clients to *temporarily* redirect to `http://diveintomark.org/xml/atom.xml`. 

[![2](../images/callouts/2.png)](#oa.redirect.4.2) The server sends back a `302` status code, indicating a temporary redirect. The temporary new location of the data is given in the `Location:` header. 

[![3](../images/callouts/3.png)](#oa.redirect.4.3) `urllib2` calls your `http_error_302` method, which calls the ancestor method of the same name in `urllib2.HTTPRedirectHandler`, which follows the redirect to the new location. Then your `http_error_302` method stores the status code (`302`) so the calling application can get it later. 

[![4](../images/callouts/4.png)](#oa.redirect.4.4) And here you are, having successfully followed the redirect to `http://diveintomark.org/xml/atom.xml`. `f.status` tells you that this was a temporary redirect, which means that you should continue to request data from the original address (`http://diveintomark.org/redir/example302.xml`). Maybe it will redirect next time too, but maybe not. Maybe it will redirect to a different address. It's not for you to say. The server said this redirect was only temporary, so you should respect that. And now you're exposing enough information that the calling application can respect that. 

  

