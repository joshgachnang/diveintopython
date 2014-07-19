

12.7. Searching Google
----------------------

Let's finally turn to the sample code that you saw that the beginning of
this chapter, which does something more useful and exciting than get the
current temperature.

Google provides a SOAP API for programmatically accessing Google search
results. To use it, you will need to sign up for Google Web Services.

### Procedure 12.4. Signing Up for Google Web Services

1.  Go to [http://www.google.com/apis/](http://www.google.com/apis/) and
    create a Google account. This requires only an email address. After
    you sign up you will receive your Google API license key by email.
    You will need this key to pass as a parameter whenever you call
    Google's search functions.

2.  Also on [http://www.google.com/apis/](http://www.google.com/apis/),
    download the Google Web APIs developer kit. This includes some
    sample code in several programming languages (but not Python), and
    more importantly, it includes the WSDL file.

3.  Decompress the developer kit file and find `GoogleSearch.wsdl`. Copy
    this file to some permanent location on your local drive. You will
    need it later in this chapter.

Once you have your developer key and your Google WSDL file in a known
place, you can start poking around with Google Web Services.

### Example 12.12. Introspecting Google Web Services

    >>> from SOAPpy import WSDL
    >>> server = WSDL.Proxy('/path/to/your/GoogleSearch.wsdl') 
    >>> server.methods.keys()                                  
    [u'doGoogleSearch', u'doGetCachedPage', u'doSpellingSuggestion']
    >>> callInfo = server.methods['doGoogleSearch']
    >>> for arg in callInfo.inparams:                          
    ...     print arg.name.ljust(15), arg.type
    key             (u'http://www.w3.org/2001/XMLSchema', u'string')
    q               (u'http://www.w3.org/2001/XMLSchema', u'string')
    start           (u'http://www.w3.org/2001/XMLSchema', u'int')
    maxResults      (u'http://www.w3.org/2001/XMLSchema', u'int')
    filter          (u'http://www.w3.org/2001/XMLSchema', u'boolean')
    restrict        (u'http://www.w3.org/2001/XMLSchema', u'string')
    safeSearch      (u'http://www.w3.org/2001/XMLSchema', u'boolean')
    lr              (u'http://www.w3.org/2001/XMLSchema', u'string')
    ie              (u'http://www.w3.org/2001/XMLSchema', u'string')
    oe              (u'http://www.w3.org/2001/XMLSchema', u'string')



[![1](../images/callouts/1.png)](#soap.google.1.1) Getting started with Google web services is easy: just create a `WSDL.Proxy` object and point it at your local copy of Google's WSDL file. 

[![2](../images/callouts/2.png)](#soap.google.1.2) According to the WSDL file, Google offers three functions: `doGoogleSearch`, `doGetCachedPage`, and `doSpellingSuggestion`. These do exactly what they sound like: perform a Google search and return the results programmatically, get access to the cached version of a page from the last time Google saw it, and offer spelling suggestions for commonly misspelled search words. 

[![3](../images/callouts/3.png)](#soap.google.1.3) The `doGoogleSearch` function takes a number of parameters of various types. Note that while the WSDL file can tell you what the arguments are called and what datatype they are, it can't tell you what they mean or how to use them. It could theoretically tell you the acceptable range of values for each parameter, if only specific values were allowed, but Google's WSDL file is not that detailed. `WSDL.Proxy` can't work magic; it can only give you the information provided in the WSDL file. 

Here is a brief synopsis of all the parameters to the `doGoogleSearch`
function:

-   `key` - Your Google API key, which you received when you signed up
    for Google web services.
-   `q` - The search word or phrase you're looking for. The syntax is
    exactly the same as Google's web form, so if you know any advanced
    search syntax or tricks, they all work here as well.
-   `start` - The index of the result to start on. Like the interactive
    web version of Google, this function returns 10 results at a time.
    If you wanted to get the second “page” of results, you would set
    `start` to 10.
-   `maxResults` - The number of results to return. Currently capped at
    10, although you can specify fewer if you are only interested in a
    few results and want to save a little bandwidth.
-   `filter` - If `True`, Google will filter out duplicate pages from
    the results.
-   `restrict` - Set this to `country` plus a country code to get
    results only from a particular country. Example: `countryUK` to
    search pages in the United Kingdom. You can also specify `linux`,
    `mac`, or `bsd` to search a Google-defined set of technical sites,
    or `unclesam` to search sites about the United States government.
-   `safeSearch` - If `True`, Google will filter out porn sites.
-   `lr` (“language restrict”) - Set this to a language code to get
    results only in a particular language.
-   `ie` and `oe` (“input encoding” and “output encoding”) - Deprecated,
    both must be `utf-8`.

### Example 12.13. Searching Google

    >>> from SOAPpy import WSDL
    >>> server = WSDL.Proxy('/path/to/your/GoogleSearch.wsdl')
    >>> key = 'YOUR_GOOGLE_API_KEY'
    >>> results = server.doGoogleSearch(key, 'mark', 0, 10, False, "",
    ...     False, "", "utf-8", "utf-8")             
    >>> len(results.resultElements)                  
    10
    >>> results.resultElements[0].URL                
    'http://diveintomark.org/'
    >>> results.resultElements[0].title
    'dive into <b>mark</b>'



[![1](../images/callouts/1.png)](#soap.google.2.1) After setting up the `WSDL.Proxy` object, you can call `server.doGoogleSearch` with all ten parameters. Remember to use your own Google API key that you received when you signed up for Google web services. 

[![2](../images/callouts/2.png)](#soap.google.2.2) There's a lot of information returned, but let's look at the actual search results first. They're stored in `results.resultElements`, and you can access them just like a normal Python list. 

[![3](../images/callouts/3.png)](#soap.google.2.3) Each element in the `resultElements` is an object that has a `URL`, `title`, `snippet`, and other useful attributes. At this point you can use normal Python introspection techniques like **`dir(results.resultElements[0])`** to see the available attributes. Or you can introspect through the WSDL proxy object and look through the function's `outparams`. Each technique will give you the same information. 

The `results` object contains more than the actual search results. It
also contains information about the search itself, such as how long it
took and how many results were found (even though only 10 were
returned). The Google web interface shows this information, and you can
access it programmatically too.

### Example 12.14. Accessing Secondary Information From Google

    >>> results.searchTime                     
    0.224919
    >>> results.estimatedTotalResultsCount     
    29800000
    >>> results.directoryCategories            
    [<SOAPpy.Types.structType item at 14367400>:
     {'fullViewableName':
      'Top/Arts/Literature/World_Literature/American/19th_Century/Twain,_Mark',
      'specialEncoding': ''}]
    >>> results.directoryCategories[0].fullViewableName
    'Top/Arts/Literature/World_Literature/American/19th_Century/Twain,_Mark'



[![1](../images/callouts/1.png)](#soap.google.3.1) This search took 0.224919 seconds. That does not include the time spent sending and receiving the actual SOAP XML documents. It's just the time that Google spent processing your request once it received it. 

[![2](../images/callouts/2.png)](#soap.google.3.2) In total, there were approximately 30 million results. You can access them 10 at a time by changing the `start` parameter and calling `server.doGoogleSearch` again. 

[![3](../images/callouts/3.png)](#soap.google.3.3) For some queries, Google also returns a list of related categories in the [Google Directory](http://directory.google.com/). You can append these URLs to [http://directory.google.com/](http://directory.google.com/) to construct the link to the directory category page. 

  

