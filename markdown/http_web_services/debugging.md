

11.4. Debugging HTTP web services
---------------------------------

First, let's turn on the debugging features of Python's HTTP library and
see what's being sent over the wire. This will be useful throughout the
chapter, as you add more and more features.

### Example 11.3. Debugging HTTP

    >>> import httplib
    >>> httplib.HTTPConnection.debuglevel = 1             
    >>> import urllib
    >>> feeddata = urllib.urlopen('http://diveintomark.org/xml/atom.xml').read()
    connect: (diveintomark.org, 80)                       
    send: '
    GET /xml/atom.xml HTTP/1.0                            
    Host: diveintomark.org                                
    User-agent: Python-urllib/1.15                        
    '
    reply: 'HTTP/1.1 200 OK\r\n'                          
    header: Date: Wed, 14 Apr 2004 22:27:30 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Content-Type: application/atom+xml
    header: Last-Modified: Wed, 14 Apr 2004 22:14:38 GMT  
    header: ETag: "e8284-68e0-4de30f80"                   
    header: Accept-Ranges: bytes
    header: Content-Length: 26848
    header: Connection: close



[![1](../images/callouts/1.png)](#oa.debug.1.1) `urllib` relies on another standard Python library, `httplib`. Normally you don't need to `import httplib` directly (`urllib` does that automatically), but you will here so you can set the debugging flag on the `HTTPConnection` class that `urllib` uses internally to connect to the HTTP server. This is an incredibly useful technique. Some other Python libraries have similar debug flags, but there's no particular standard for naming them or turning them on; you need to read the documentation of each library to see if such a feature is available. 

[![2](../images/callouts/2.png)](#oa.debug.1.2) Now that the debugging flag is set, information on the the HTTP request and response is printed out in real time. The first thing it tells you is that you're connecting to the server `diveintomark.org` on port 80, which is the standard port for HTTP. 

[![3](../images/callouts/3.png)](#oa.debug.1.3) When you request the Atom feed, `urllib` sends three lines to the server. The first line specifies the HTTP verb you're using, and the path of the resource (minus the domain name). All the requests in this chapter will use `GET`, but in the next chapter on SOAP, you'll see that it uses `POST` for everything. The basic syntax is the same, regardless of the verb. 

[![4](../images/callouts/4.png)](#oa.debug.1.4) The second line is the `Host` header, which specifies the domain name of the service you're accessing. This is important, because a single HTTP server can host multiple separate domains. My server currently hosts 12 domains; other servers can host hundreds or even thousands. 

[![5](../images/callouts/5.png)](#oa.debug.1.5) The third line is the `User-Agent` header. What you see here is the generic `User-Agent` that the `urllib` library adds by default. In the next section, you'll see how to customize this to be more specific. 

[![6](../images/callouts/6.png)](#oa.debug.1.6) The server replies with a status code and a bunch of headers (and possibly some data, which got stored in the `feeddata` variable). The status code here is `200`, meaning “everything's normal, here's the data you requested”. The server also tells you the date it responded to your request, some information about the server itself, and the content type of the data it's giving you. Depending on your application, this might be useful, or not. It's certainly reassuring that you thought you were asking for an Atom feed, and lo and behold, you're getting an Atom feed (`application/atom+xml`, which is the registered content type for Atom feeds). 

[![7](../images/callouts/7.png)](#oa.debug.1.7) The server tells you when this Atom feed was last modified (in this case, about 13 minutes ago). You can send this date back to the server the next time you request the same feed, and the server can do last-modified checking. 

[![8](../images/callouts/8.png)](#oa.debug.1.8) The server also tells you that this Atom feed has an ETag hash of `"e8284-68e0-4de30f80"`. The hash doesn't mean anything by itself; there's nothing you can do with it, except send it back to the server the next time you request this same feed. Then the server can use it to tell you if the data has changed or not. 

  

