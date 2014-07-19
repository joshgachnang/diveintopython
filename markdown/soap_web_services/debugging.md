

12.4. Debugging SOAP Web Services
---------------------------------

The SOAP libraries provide an easy way to see what's going on behind the
scenes.

Turning on debugging is a simple matter of setting two flags in the
`SOAPProxy`'s configuration.

### Example 12.7. Debugging SOAP Web Services

    >>> from SOAPpy import SOAPProxy
    >>> url = 'http://services.xmethods.net:80/soap/servlet/rpcrouter'
    >>> n = 'urn:xmethods-Temperature'
    >>> server = SOAPProxy(url, namespace=n)     
    >>> server.config.dumpSOAPOut = 1            
    >>> server.config.dumpSOAPIn = 1
    >>> temperature = server.getTemp('27502')    
    *** Outgoing SOAP ******************************************************
    <?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
      xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
      xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
      xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
      xmlns:xsd="http://www.w3.org/1999/XMLSchema">
    <SOAP-ENV:Body>
    <ns1:getTemp xmlns:ns1="urn:xmethods-Temperature" SOAP-ENC:root="1">
    <v1 xsi:type="xsd:string">27502</v1>
    </ns1:getTemp>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    ************************************************************************
    *** Incoming SOAP ******************************************************
    <?xml version='1.0' encoding='UTF-8'?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <SOAP-ENV:Body>
    <ns1:getTempResponse xmlns:ns1="urn:xmethods-Temperature"
      SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <return xsi:type="xsd:float">80.0</return>
    </ns1:getTempResponse>

    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    ************************************************************************

    >>> temperature
    80.0



[![1](../images/callouts/1.png)](#soap.debug.1.1) First, create the `SOAPProxy` like normal, with the service URL and the namespace. 

[![2](../images/callouts/2.png)](#soap.debug.1.2) Second, turn on debugging by setting `server.config.dumpSOAPIn` and `server.config.dumpSOAPOut`. 

[![3](../images/callouts/3.png)](#soap.debug.1.3) Third, call the remote SOAP method as usual. The SOAP library will print out both the outgoing XML request document, and the incoming XML response document. This is all the hard work that `SOAPProxy` is doing for you. Intimidating, isn't it? Let's break it down. 

Most of the XML request document that gets sent to the server is just
boilerplate. Ignore all the namespace declarations; they're going to be
the same (or similar) for all SOAP calls. The heart of the “function
call” is this fragment within the `<Body>` element:

    <ns1:getTemp                                 
      xmlns:ns1="urn:xmethods-Temperature"       
      SOAP-ENC:root="1">
    <v1 xsi:type="xsd:string">27502</v1>         
    </ns1:getTemp>



[![1](../images/callouts/1.png)](#soap.debug.2.1) The element name is the function name, `getTemp`. `SOAPProxy` uses [`getattr` as a dispatcher](../scripts_and_streams/handlers_by_node_type.html "10.5. Creating separate handlers by node type"). Instead of calling separate local methods based on the method name, it actually uses the method name to construct the XML request document. 

[![2](../images/callouts/2.png)](#soap.debug.2.2) The function's XML element is contained in a specific namespace, which is the namespace you specified when you created the `SOAPProxy` object. Don't worry about the `SOAP-ENC:root`; that's boilerplate too. 

[![3](../images/callouts/3.png)](#soap.debug.2.3) The arguments of the function also got translated into XML. `SOAPProxy` introspects each argument to determine its datatype (in this case it's a string). The argument datatype goes into the `xsi:type` attribute, followed by the actual string value. 

The XML return document is equally easy to understand, once you know
what to ignore. Focus on this fragment within the `<Body>`:

    <ns1:getTempResponse                             
      xmlns:ns1="urn:xmethods-Temperature"           
      SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
    <return xsi:type="xsd:float">80.0</return>       
    </ns1:getTempResponse>



[![1](../images/callouts/1.png)](#soap.debug.3.1) The server wraps the function return value within a `<getTempResponse>` element. By convention, this wrapper element is the name of the function, plus `Response`. But it could really be almost anything; the important thing that `SOAPProxy` notices is not the element name, but the namespace. 

[![2](../images/callouts/2.png)](#soap.debug.3.2) The server returns the response in the same namespace we used in the request, the same namespace we specified when we first create the `SOAPProxy`. Later in this chapter we'll see what happens if you forget to specify the namespace when creating the `SOAPProxy`. 

[![3](../images/callouts/3.png)](#soap.debug.3.3) The return value is specified, along with its datatype (it's a float). `SOAPProxy` uses this explicit datatype to create a Python object of the correct native datatype and return it. 

  

