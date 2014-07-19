

11.2. How not to fetch data over HTTP
-------------------------------------

Let's say you want to download a resource over HTTP, such as a
syndicated Atom feed. But you don't just want to download it once; you
want to download it over and over again, every hour, to get the latest
news from the site that's offering the news feed. Let's do it the
quick-and-dirty way first, and then see how you can do better.

### Example 11.2. Downloading a feed the quick-and-dirty way

    >>> import urllib
    >>> data = urllib.urlopen('http://diveintomark.org/xml/atom.xml').read()    
    >>> print data
    <?xml version="1.0" encoding="iso-8859-1"?>
    <feed version="0.3"
      xmlns="http://purl.org/atom/ns#"
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xml:lang="en">
      <title mode="escaped">dive into mark</title>
      <link rel="alternate" type="text/html" href="http://diveintomark.org/"/>
      <-- rest of feed omitted for brevity -->



[![1](../images/callouts/1.png)](#oa.review.1.1) Downloading anything over HTTP is incredibly easy in Python; in fact, it's a one-liner. The `urllib` module has a handy `urlopen` function that takes the address of the page you want, and returns a file-like object that you can just `read()` from to get the full contents of the page. It just can't get much easier. 

So what's wrong with this? Well, for a quick one-off during testing or
development, there's nothing wrong with it. I do it all the time. I
wanted the contents of the feed, and I got the contents of the feed. The
same technique works for any web page. But once you start thinking in
terms of a web service that you want to access on a regular basis -- and
remember, you said you were planning on retrieving this syndicated feed
once an hour -- then you're being inefficient, and you're being rude.

Let's talk about some of the basic features of HTTP.

  

