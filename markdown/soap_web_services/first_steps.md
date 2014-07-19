

12.3. First Steps with SOAP
---------------------------

The heart of SOAP is the ability to call remote functions. There are a
number of public access SOAP servers that provide simple functions for
demonstration purposes.

The most popular public access SOAP server is
[http://www.xmethods.net/](http://www.xmethods.net/). This example uses
a demonstration function that takes a United States zip code and returns
the current temperature in that region.

### Example 12.6. Getting the Current Temperature

    >>> from SOAPpy import SOAPProxy            
    >>> url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
    >>> namespace = 'urn:xmethods-Temperature'  
    >>> server = SOAPProxy(url, namespace)      
    >>> server.getTemp('27502')                 
    80.0



[![1](../images/callouts/1.png)](#soap.firststeps.1.1) You access the remote SOAP server through a proxy class, `SOAPProxy`. The proxy handles all the internals of SOAP for you, including creating the XML request document out of the function name and argument list, sending the request over HTTP to the remote SOAP server, parsing the XML response document, and creating native Python values to return. You'll see what these XML documents look like in the next section. 

[![2](../images/callouts/2.png)](#soap.firststeps.1.2) Every SOAP service has a URL which handles all the requests. The same URL is used for all function calls. This particular service only has a single function, but later in this chapter you'll see examples of the Google API, which has several functions. The service URL is shared by all functions.Each SOAP service also has a namespace, which is defined by the server and is completely arbitrary. It's simply part of the configuration required to call SOAP methods. It allows the server to share a single service URL and route requests between several unrelated services. It's like dividing Python modules into [packages](../xml_processing/packages.html "9.2. Packages"). 

[![3](../images/callouts/3.png)](#soap.firststeps.1.3) You're creating the `SOAPProxy` with the service URL and the service namespace. This doesn't make any connection to the SOAP server; it simply creates a local Python object. 

[![4](../images/callouts/4.png)](#soap.firststeps.1.4) Now with everything configured properly, you can actually call remote SOAP methods as if they were local functions. You pass arguments just like a normal function, and you get a return value just like a normal function. But under the covers, there's a heck of a lot going on. 

Let's peek under those covers.

  

