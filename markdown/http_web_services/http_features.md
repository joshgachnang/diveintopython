

11.3. Features of HTTP
----------------------

-   [11.3.1. User-Agent](http_features.html#d0e27596)
-   [11.3.2. Redirects](http_features.html#d0e27616)
-   [11.3.3.
    Last-Modified/If-Modified-Since](http_features.html#d0e27689)
-   [11.3.4. ETag/If-None-Match](http_features.html#d0e27724)
-   [11.3.5. Compression](http_features.html#d0e27752)

There are five important features of HTTP which you should support.

### 11.3.1. `User-Agent`

The `User-Agent` is simply a way for a client to tell a server who it is
when it requests a web page, a syndicated feed, or any sort of web
service over HTTP. When the client requests a resource, it should always
announce who it is, as specifically as possible. This allows the
server-side administrator to get in touch with the client-side developer
if anything is going fantastically wrong.

By default, Python sends a generic `User-Agent`: `Python-urllib/1.15`.
In the next section, you'll see how to change this to something more
specific.

### 11.3.2. Redirects

Sometimes resources move around. Web sites get reorganized, pages move
to new addresses. Even web services can reorganize. A syndicated feed at
`http://example.com/index.xml` might be moved to
`http://example.com/xml/atom.xml`. Or an entire domain might move, as an
organization expands and reorganizes; for instance,
`http://www.example.com/index.xml` might be redirected to
`http://server-farm-1.example.com/index.xml`.

Every time you request any kind of resource from an HTTP server, the
server includes a status code in its response. Status code `200` means
“everything's normal, here's the page you asked for”. Status code `404`
means “page not found”. (You've probably seen 404 errors while browsing
the web.)

HTTP has two different ways of signifying that a resource has moved.
Status code `302` is a *temporary redirect*; it means “oops, that got
moved over here temporarily” (and then gives the temporary address in a
`Location:` header). Status code `301` is a *permanent redirect*; it
means “oops, that got moved permanently” (and then gives the new address
in a `Location:` header). If you get a `302` status code and a new
address, the HTTP specification says you should use the new address to
get what you asked for, but the next time you want to access the same
resource, you should retry the old address. But if you get a `301`
status code and a new address, you're supposed to use the new address
from then on.

`urllib.urlopen` will automatically “follow” redirects when it receives
the appropriate status code from the HTTP server, but unfortunately, it
doesn't tell you when it does so. You'll end up getting data you asked
for, but you'll never know that the underlying library “helpfully”
followed a redirect for you. So you'll continue pounding away at the old
address, and each time you'll get redirected to the new address. That's
two round trips instead of one: not very efficient! Later in this
chapter, you'll see how to work around this so you can deal with
permanent redirects properly and efficiently.

### 11.3.3. `Last-Modified`/`If-Modified-Since`

Some data changes all the time. The home page of CNN.com is constantly
updating every few minutes. On the other hand, the home page of
Google.com only changes once every few weeks (when they put up a special
holiday logo, or advertise a new service). Web services are no
different; usually the server knows when the data you requested last
changed, and HTTP provides a way for the server to include this
last-modified date along with the data you requested.

If you ask for the same data a second time (or third, or fourth), you
can tell the server the last-modified date that you got last time: you
send an `If-Modified-Since` header with your request, with the date you
got back from the server last time. If the data hasn't changed since
then, the server sends back a special HTTP status code `304`, which
means “this data hasn't changed since the last time you asked for it”.
Why is this an improvement? Because when the server sends a `304`, *it
doesn't re-send the data*. All you get is the status code. So you don't
need to download the same data over and over again if it hasn't changed;
the server assumes you have the data cached locally.

All modern web browsers support last-modified date checking. If you've
ever visited a page, re-visited the same page a day later and found that
it hadn't changed, and wondered why it loaded so quickly the second time
-- this could be why. Your web browser cached the contents of the page
locally the first time, and when you visited the second time, your
browser automatically sent the last-modified date it got from the server
the first time. The server simply says `304: Not Modified`, so your
browser knows to load the page from its cache. Web services can be this
smart too.

Python's URL library has no built-in support for last-modified date
checking, but since you can add arbitrary headers to each request and
read arbitrary headers in each response, you can add support for it
yourself.

### 11.3.4. `ETag`/`If-None-Match`

ETags are an alternate way to accomplish the same thing as the
last-modified date checking: don't re-download data that hasn't changed.
The way it works is, the server sends some sort of hash of the data (in
an `ETag` header) along with the data you requested. Exactly how this
hash is determined is entirely up to the server. The second time you
request the same data, you include the ETag hash in an `If-None-Match:`
header, and if the data hasn't changed, the server will send you back a
`304` status code. As with the last-modified date checking, the server
*just* sends the `304`; it doesn't send you the same data a second time.
By including the ETag hash in your second request, you're telling the
server that there's no need to re-send the same data if it still matches
this hash, since you still have the data from the last time.

Python's URL library has no built-in support for ETags, but you'll see
how to add it later in this chapter.

### 11.3.5. Compression

The last important HTTP feature is gzip compression. When you talk about
HTTP web services, you're almost always talking about moving XML back
and forth over the wire. XML is text, and quite verbose text at that,
and text generally compresses well. When you request a resource over
HTTP, you can ask the server that, if it has any new data to send you,
to please send it in compressed format. You include the
`Accept-encoding: gzip` header in your request, and if the server
supports compression, it will send you back gzip-compressed data and
mark it with a `Content-encoding: gzip` header.

Python's URL library has no built-in support for gzip compression per
se, but you can add arbitrary headers to the request. And Python comes
with a separate `gzip` module, which has functions you can use to
decompress the data yourself.

Note that [our little one-line
script](review.html "11.2. How not to fetch data over HTTP") to download
a syndicated feed did not support any of these HTTP features. Let's see
how you can improve it.

  

