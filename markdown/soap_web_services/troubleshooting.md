

12.8. Troubleshooting SOAP Web Services
---------------------------------------

Of course, the world of SOAP web services is not all happiness and
light. Sometimes things go wrong.

As you've seen throughout this chapter, SOAP involves several layers.
There's the HTTP layer, since SOAP is sending XML documents to, and
receiving XML documents from, an HTTP server. So all the debugging
techniques you learned in [Chapter 11, *HTTP Web
Services*](../http_web_services/index.html "Chapter 11. HTTP Web Services")
come into play here. You can **`import httplib`** and then set
**`httplib.HTTPConnection.debuglevel = 1`** to see the underlying HTTP
traffic.

Beyond the underlying HTTP layer, there are a number of things that can
go wrong. SOAPpy does an admirable job hiding the SOAP syntax from you,
but that also means it can be difficult to determine where the problem
is when things don't work.

Here are a few examples of common mistakes that I've made in using SOAP
web services, and the errors they generated.

### Example 12.15. Calling a Method With an Incorrectly Configured Proxy

    >>> from SOAPpy import SOAPProxy
    >>> url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
    >>> server = SOAPProxy(url)                                        
    >>> server.getTemp('27502')                                        
    <Fault SOAP-ENV:Server.BadTargetObjectURI:
    Unable to determine object id from call: is the method element namespaced?>
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 453, in __call__
        return self.__r_call(*args, **kw)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 475, in __r_call
        self.__hd, self.__ma)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 389, in __call
        raise p
    SOAPpy.Types.faultType: <Fault SOAP-ENV:Server.BadTargetObjectURI:
    Unable to determine object id from call: is the method element namespaced?>



[![1](../images/callouts/1.png)](#soap.troubleshooting.1.1) Did you spot the mistake? You're creating a `SOAPProxy` manually, and you've correctly specified the service URL, but you haven't specified the namespace. Since multiple services may be routed through the same service URL, the namespace is essential to determine which service you're trying to talk to, and therefore which method you're really calling. 

[![2](../images/callouts/2.png)](#soap.troubleshooting.1.2) The server responds by sending a SOAP Fault, which SOAPpy turns into a Python exception of type `SOAPpy.Types.faultType`. All errors returned from any SOAP server will always be SOAP Faults, so you can easily catch this exception. In this case, the human-readable part of the SOAP Fault gives a clue to the problem: the method element is not namespaced, because the original `SOAPProxy` object was not configured with a service namespace. 

Misconfiguring the basic elements of the SOAP service is one of the
problems that WSDL aims to solve. The WSDL file contains the service URL
and namespace, so you can't get it wrong. Of course, there are still
other things you can get wrong.

### Example 12.16. Calling a Method With the Wrong Arguments

    >>> wsdlFile = 'http://www.xmethods.net/sd/2001/TemperatureService.wsdl'
    >>> server = WSDL.Proxy(wsdlFile)
    >>> temperature = server.getTemp(27502)                                
    <Fault SOAP-ENV:Server: Exception while handling service request:
    services.temperature.TempService.getTemp(int) -- no signature match>   
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 453, in __call__
        return self.__r_call(*args, **kw)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 475, in __r_call
        self.__hd, self.__ma)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 389, in __call
        raise p
    SOAPpy.Types.faultType: <Fault SOAP-ENV:Server: Exception while handling service request:
    services.temperature.TempService.getTemp(int) -- no signature match>



[![1](../images/callouts/1.png)](#soap.troubleshooting.2.1) Did you spot the mistake? It's a subtle one: you're calling `server.getTemp` with an integer instead of a string. As you saw from introspecting the WSDL file, the `getTemp()` SOAP function takes a single argument, `zipcode`, which must be a string. `WSDL.Proxy` will *not* coerce datatypes for you; you need to pass the exact datatypes that the server expects. 

[![2](../images/callouts/2.png)](#soap.troubleshooting.2.2) Again, the server returns a SOAP Fault, and the human-readable part of the error gives a clue as to the problem: you're calling a `getTemp` function with an integer value, but there is no function defined with that name that takes an integer. In theory, SOAP allows you to *overload* functions, so you could have two functions in the same SOAP service with the same name and the same number of arguments, but the arguments were of different datatypes. This is why it's important to match the datatypes exactly, and why `WSDL.Proxy` doesn't coerce datatypes for you. If it did, you could end up calling a completely different function! Good luck debugging that one. It's much easier to be picky about datatypes and fail as quickly as possible if you get them wrong. 

It's also possible to write Python code that expects a different number
of return values than the remote function actually returns.

### Example 12.17. Calling a Method and Expecting the Wrong Number of Return Values

    >>> wsdlFile = 'http://www.xmethods.net/sd/2001/TemperatureService.wsdl'
    >>> server = WSDL.Proxy(wsdlFile)
    >>> (city, temperature) = server.getTemp(27502)  
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    TypeError: unpack non-sequence



[![1](../images/callouts/1.png)](#soap.troubleshooting.3.1) Did you spot the mistake? `server.getTemp` only returns one value, a float, but you've written code that assumes you're getting two values and trying to assign them to two different variables. Note that this does not fail with a SOAP fault. As far as the remote server is concerned, nothing went wrong at all. The error only occurred *after* the SOAP transaction was complete, `WSDL.Proxy` returned a float, and your local Python interpreter tried to accomodate your request to split it into two different variables. Since the function only returned one value, you get a Python exception trying to split it, not a SOAP Fault. 

What about Google's web service? The most common problem I've had with
it is that I forget to set the application key properly.

### Example 12.18. Calling a Method With An Application-Specific Error

    >>> from SOAPpy import WSDL
    >>> server = WSDL.Proxy(r'/path/to/local/GoogleSearch.wsdl')
    >>> results = server.doGoogleSearch('foo', 'mark', 0, 10, False, "", 
    ...     False, "", "utf-8", "utf-8")
    <Fault SOAP-ENV:Server:                                              
     Exception from service object: Invalid authorization key: foo:
     <SOAPpy.Types.structType detail at 14164616>:
     {'stackTrace':
      'com.google.soap.search.GoogleSearchFault: Invalid authorization key: foo
       at com.google.soap.search.QueryLimits.lookUpAndLoadFromINSIfNeedBe(
         QueryLimits.java:220)
       at com.google.soap.search.QueryLimits.validateKey(QueryLimits.java:127)
       at com.google.soap.search.GoogleSearchService.doPublicMethodChecks(
         GoogleSearchService.java:825)
       at com.google.soap.search.GoogleSearchService.doGoogleSearch(
         GoogleSearchService.java:121)
       at sun.reflect.GeneratedMethodAccessor13.invoke(Unknown Source)
       at sun.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)
       at java.lang.reflect.Method.invoke(Unknown Source)
       at org.apache.soap.server.RPCRouter.invoke(RPCRouter.java:146)
       at org.apache.soap.providers.RPCJavaProvider.invoke(
         RPCJavaProvider.java:129)
       at org.apache.soap.server.http.RPCRouterServlet.doPost(
         RPCRouterServlet.java:288)
       at javax.servlet.http.HttpServlet.service(HttpServlet.java:760)
       at javax.servlet.http.HttpServlet.service(HttpServlet.java:853)
       at com.google.gse.HttpConnection.runServlet(HttpConnection.java:237)
       at com.google.gse.HttpConnection.run(HttpConnection.java:195)
       at com.google.gse.DispatchQueue$WorkerThread.run(DispatchQueue.java:201)
    Caused by: com.google.soap.search.UserKeyInvalidException: Key was of wrong size.
       at com.google.soap.search.UserKey.<init>(UserKey.java:59)
       at com.google.soap.search.QueryLimits.lookUpAndLoadFromINSIfNeedBe(
         QueryLimits.java:217)
       ... 14 more
    '}>
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 453, in __call__
        return self.__r_call(*args, **kw)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 475, in __r_call
        self.__hd, self.__ma)
      File "c:\python23\Lib\site-packages\SOAPpy\Client.py", line 389, in __call
        raise p
    SOAPpy.Types.faultType: <Fault SOAP-ENV:Server: Exception from service object:
    Invalid authorization key: foo:
    <SOAPpy.Types.structType detail at 14164616>:
    {'stackTrace':
      'com.google.soap.search.GoogleSearchFault: Invalid authorization key: foo
       at com.google.soap.search.QueryLimits.lookUpAndLoadFromINSIfNeedBe(
         QueryLimits.java:220)
       at com.google.soap.search.QueryLimits.validateKey(QueryLimits.java:127)
       at com.google.soap.search.GoogleSearchService.doPublicMethodChecks(
         GoogleSearchService.java:825)
       at com.google.soap.search.GoogleSearchService.doGoogleSearch(
         GoogleSearchService.java:121)
       at sun.reflect.GeneratedMethodAccessor13.invoke(Unknown Source)
       at sun.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)
       at java.lang.reflect.Method.invoke(Unknown Source)
       at org.apache.soap.server.RPCRouter.invoke(RPCRouter.java:146)
       at org.apache.soap.providers.RPCJavaProvider.invoke(
         RPCJavaProvider.java:129)
       at org.apache.soap.server.http.RPCRouterServlet.doPost(
         RPCRouterServlet.java:288)
       at javax.servlet.http.HttpServlet.service(HttpServlet.java:760)
       at javax.servlet.http.HttpServlet.service(HttpServlet.java:853)
       at com.google.gse.HttpConnection.runServlet(HttpConnection.java:237)
       at com.google.gse.HttpConnection.run(HttpConnection.java:195)
       at com.google.gse.DispatchQueue$WorkerThread.run(DispatchQueue.java:201)
    Caused by: com.google.soap.search.UserKeyInvalidException: Key was of wrong size.
       at com.google.soap.search.UserKey.<init>(UserKey.java:59)
       at com.google.soap.search.QueryLimits.lookUpAndLoadFromINSIfNeedBe(
         QueryLimits.java:217)
       ... 14 more
    '}>



[![1](../images/callouts/1.png)](#soap.troubleshooting.4.1) Can you spot the mistake? There's nothing wrong with the calling syntax, or the number of arguments, or the datatypes. The problem is application-specific: the first argument is supposed to be my application key, but `foo` is not a valid Google key. 

[![2](../images/callouts/2.png)](#soap.troubleshooting.4.2) The Google server responds with a SOAP Fault and an incredibly long error message, which includes a complete Java stack trace. Remember that *all* SOAP errors are signified by SOAP Faults: errors in configuration, errors in function arguments, and application-specific errors like this. Buried in there somewhere is the crucial piece of information: `Invalid authorization key: foo`. 

### Further Reading on Troubleshooting SOAP

-   [New developments for
    SOAPpy](http://www-106.ibm.com/developerworks/webservices/library/ws-pyth17.html)
    steps through trying to connect to another SOAP service that doesn't
    quite work as advertised.

  

