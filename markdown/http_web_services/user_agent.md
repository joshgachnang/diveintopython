

11.5. Setting the `User-Agent`
------------------------------

The first step to improving your HTTP web services client is to identify
yourself properly with a `User-Agent`. To do that, you need to move
beyond the basic `urllib` and dive into `urllib2`.

### Example 11.4. Introducing `urllib2`

    >>> import httplib
    >>> httplib.HTTPConnection.debuglevel = 1                             
    >>> import urllib2
    >>> request = urllib2.Request('http://diveintomark.org/xml/atom.xml') 
    >>> opener = urllib2.build_opener()                                   
    >>> feeddata = opener.open(request).read()                            
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Wed, 14 Apr 2004 23:23:12 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Content-Type: application/atom+xml
    header: Last-Modified: Wed, 14 Apr 2004 22:14:38 GMT
    header: ETag: "e8284-68e0-4de30f80"
    header: Accept-Ranges: bytes
    header: Content-Length: 26848
    header: Connection: close



[![1](../images/callouts/1.png)](#oa.useragent.1.1) If you still have your Python IDE open from the previous section's example, you can skip this, but this turns on [HTTP debugging](debugging.html "11.4. Debugging HTTP web services") so you can see what you're actually sending over the wire, and what gets sent back. 

[![2](../images/callouts/2.png)](#oa.useragent.1.2) Fetching an HTTP resource with `urllib2` is a three-step process, for good reasons that will become clear shortly. The first step is to create a `Request` object, which takes the URL of the resource you'll eventually get around to retrieving. Note that this step doesn't actually retrieve anything yet. 

[![3](../images/callouts/3.png)](#oa.useragent.1.3) The second step is to build a URL opener. This can take any number of handlers, which control how responses are handled. But you can also build an opener without any custom handlers, which is what you're doing here. You'll see how to define and use custom handlers later in this chapter when you explore redirects. 

[![4](../images/callouts/4.png)](#oa.useragent.1.4) The final step is to tell the opener to open the URL, using the `Request` object you created. As you can see from all the debugging information that gets printed, this step actually retrieves the resource and stores the returned data in `feeddata`. 

### Example 11.5. Adding headers with the `Request`

    >>> request                                                
    <urllib2.Request instance at 0x00250AA8>
    >>> request.get_full_url()
    http://diveintomark.org/xml/atom.xml
    >>> request.add_header('User-Agent',
    ...     'OpenAnything/1.0 +http://diveintopython.net/')
    >>> feeddata = opener.open(request).read()                 
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: OpenAnything/1.0 +http://diveintopython.net/
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Wed, 14 Apr 2004 23:45:17 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Content-Type: application/atom+xml
    header: Last-Modified: Wed, 14 Apr 2004 22:14:38 GMT
    header: ETag: "e8284-68e0-4de30f80"
    header: Accept-Ranges: bytes
    header: Content-Length: 26848
    header: Connection: close



[![1](../images/callouts/1.png)](#oa.useragent.2.1) You're continuing from the previous example; you've already created a `Request` object with the URL you want to access. 

[![2](../images/callouts/2.png)](#oa.useragent.2.2) Using the `add_header` method on the `Request` object, you can add arbitrary HTTP headers to the request. The first argument is the header, the second is the value you're providing for that header. Convention dictates that a `User-Agent` should be in this specific format: an application name, followed by a slash, followed by a version number. The rest is free-form, and you'll see a lot of variations in the wild, but somewhere it should include a URL of your application. The `User-Agent` is usually logged by the server along with other details of your request, and including a URL of your application allows server administrators looking through their access logs to contact you if something is wrong. 

[![3](../images/callouts/3.png)](#oa.useragent.2.3) The `opener` object you created before can be reused too, and it will retrieve the same feed again, but with your custom `User-Agent` header. 

[![4](../images/callouts/4.png)](#oa.useragent.2.4) And here's you sending your custom `User-Agent`, in place of the generic one that Python sends by default. If you look closely, you'll notice that you defined a `User-Agent` header, but you actually sent a `User-agent` header. See the difference? `urllib2` changed the case so that only the first letter was capitalized. It doesn't really matter; HTTP specifies that header field names are completely case-insensitive. 

  

