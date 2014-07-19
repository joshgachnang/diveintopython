

11.8. Handling compressed data
------------------------------

The last important HTTP feature you want to support is compression. Many
web services have the ability to send data compressed, which can cut
down the amount of data sent over the wire by 60% or more. This is
especially true of XML web services, since XML data compresses very
well.

Servers won't give you compressed data unless you tell them you can
handle it.

### Example 11.14. Telling the server you would like compressed data

    >>> import urllib2, httplib
    >>> httplib.HTTPConnection.debuglevel = 1
    >>> request = urllib2.Request('http://diveintomark.org/xml/atom.xml')
    >>> request.add_header('Accept-encoding', 'gzip')        
    >>> opener = urllib2.build_opener()
    >>> f = opener.open(request)
    connect: (diveintomark.org, 80)
    send: '
    GET /xml/atom.xml HTTP/1.0
    Host: diveintomark.org
    User-agent: Python-urllib/2.1
    Accept-encoding: gzip                                    
    '
    reply: 'HTTP/1.1 200 OK\r\n'
    header: Date: Thu, 15 Apr 2004 22:24:39 GMT
    header: Server: Apache/2.0.49 (Debian GNU/Linux)
    header: Last-Modified: Thu, 15 Apr 2004 19:45:21 GMT
    header: ETag: "e842a-3e53-55d97640"
    header: Accept-Ranges: bytes
    header: Vary: Accept-Encoding
    header: Content-Encoding: gzip                           
    header: Content-Length: 6289                             
    header: Connection: close
    header: Content-Type: application/atom+xml



[![1](../images/callouts/1.png)](#oa.gzip.1.1) This is the key: once you've created your `Request` object, add an `Accept-encoding` header to tell the server you can accept gzip-encoded data. `gzip` is the name of the compression algorithm you're using. In theory there could be other compression algorithms, but `gzip` is the compression algorithm used by 99% of web servers. 

[![2](../images/callouts/2.png)](#oa.gzip.1.2) There's your header going across the wire. 

[![3](../images/callouts/3.png)](#oa.gzip.1.3) And here's what the server sends back: the `Content-Encoding: gzip` header means that the data you're about to receive has been gzip-compressed. 

[![4](../images/callouts/4.png)](#oa.gzip.1.4) The `Content-Length` header is the length of the compressed data, not the uncompressed data. As you'll see in a minute, the actual length of the uncompressed data was 15955, so gzip compression cut your bandwidth by over 60%! 

### Example 11.15. Decompressing the data

    >>> compresseddata = f.read()                              
    >>> len(compresseddata)
    6289
    >>> import StringIO
    >>> compressedstream = StringIO.StringIO(compresseddata)   
    >>> import gzip
    >>> gzipper = gzip.GzipFile(fileobj=compressedstream)      
    >>> data = gzipper.read()                                  
    >>> print data                                             
    <?xml version="1.0" encoding="iso-8859-1"?>
    <feed version="0.3"
      xmlns="http://purl.org/atom/ns#"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xml:lang="en">
      <title mode="escaped">dive into mark</title>
      <link rel="alternate" type="text/html" href="http://diveintomark.org/"/>
      <-- rest of feed omitted for brevity -->
    >>> len(data)
    15955



[![1](../images/callouts/1.png)](#oa.gzip.2.1) Continuing from the previous example, `f` is the file-like object returned from the URL opener. Using its `read()` method would ordinarily get you the uncompressed data, but since this data has been gzip-compressed, this is just the first step towards getting the data you really want. 

[![2](../images/callouts/2.png)](#oa.gzip.2.2) OK, this step is a little bit of messy workaround. Python has a `gzip` module, which reads (and actually writes) gzip-compressed files on disk. But you don't have a file on disk, you have a gzip-compressed buffer in memory, and you don't want to write out a temporary file just so you can uncompress it. So what you're going to do is create a file-like object out of the in-memory data (`compresseddata`), using the `StringIO` module. You first saw the `StringIO` module in [the previous chapter](../scripts_and_streams/index.html#kgp.openanything.stringio.example "Example 10.4. Introducing StringIO"), but now you've found another use for it. 

[![3](../images/callouts/3.png)](#oa.gzip.2.3) Now you can create an instance of `GzipFile`, and tell it that its “file” is the file-like object `compressedstream`. 

[![4](../images/callouts/4.png)](#oa.gzip.2.4) This is the line that does all the actual work: “reading” from `GzipFile` will decompress the data. Strange? Yes, but it makes sense in a twisted kind of way. `gzipper` is a file-like object which represents a gzip-compressed file. That “file” is not a real file on disk, though; `gzipper` is really just “reading” from the file-like object you created with `StringIO` to wrap the compressed data, which is only in memory in the variable `compresseddata`. And where did that compressed data come from? You originally downloaded it from a remote HTTP server by “reading” from the file-like object you built with `urllib2.build_opener`. And amazingly, this all just works. Every step in the chain has no idea that the previous step is faking it. 

[![5](../images/callouts/5.png)](#oa.gzip.2.5) Look ma, real data. (15955 bytes of it, in fact.) 

“But wait!” I hear you cry. “This could be even easier!” I know what
you're thinking. You're thinking that `opener.open` returns a file-like
object, so why not cut out the `StringIO` middleman and just pass `f`
directly to `GzipFile`? OK, maybe you weren't thinking that, but don't
worry about it, because it doesn't work.

### Example 11.16. Decompressing the data directly from the server

    >>> f = opener.open(request)                  
    >>> f.headers.get('Content-Encoding')         
    'gzip'
    >>> data = gzip.GzipFile(fileobj=f).read()    
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "c:\python23\lib\gzip.py", line 217, in read
        self._read(readsize)
      File "c:\python23\lib\gzip.py", line 252, in _read
        pos = self.fileobj.tell()   # Save current position
    AttributeError: addinfourl instance has no attribute 'tell'



[![1](../images/callouts/1.png)](#oa.gzip.3.1) Continuing from the previous example, you already have a `Request` object set up with an `Accept-encoding: gzip` header. 

[![2](../images/callouts/2.png)](#oa.gzip.3.2) Simply opening the request will get you the headers (though not download any data yet). As you can see from the returned `Content-Encoding` header, this data has been sent gzip-compressed. 

[![3](../images/callouts/3.png)](#oa.gzip.3.3) Since `opener.open` returns a file-like object, and you know from the headers that when you read it, you're going to get gzip-compressed data, why not simply pass that file-like object directly to `GzipFile`? As you “read” from the `GzipFile` instance, it will “read” compressed data from the remote HTTP server and decompress it on the fly. It's a good idea, but unfortunately it doesn't work. Because of the way gzip compression works, `GzipFile` needs to save its position and move forwards and backwards through the compressed file. This doesn't work when the “file” is a stream of bytes coming from a remote server; all you can do with it is retrieve bytes one at a time, not move back and forth through the data stream. So the inelegant hack of using `StringIO` is the best solution: download the compressed data, create a file-like object out of it with `StringIO`, and then decompress the data from that. 

  

