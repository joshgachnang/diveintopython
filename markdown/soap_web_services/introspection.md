

12.6. Introspecting SOAP Web Services with WSDL
-----------------------------------------------

Like many things in the web services arena, WSDL has a long and
checkered history, full of political strife and intrigue. I will skip
over this history entirely, since it bores me to tears. There were other
standards that tried to do similar things, but WSDL won, so let's learn
how to use it.

The most fundamental thing that WSDL allows you to do is discover the
available methods offered by a SOAP server.

### Example 12.8. Discovering The Available Methods

    >>> from SOAPpy import WSDL          
    >>> wsdlFile = 'http://www.xmethods.net/sd/2001/TemperatureService.wsdl')
    >>> server = WSDL.Proxy(wsdlFile)    
    >>> server.methods.keys()            
    [u'getTemp']



[![1](../images/callouts/1.png)](#soap.introspection.1.1) SOAPpy includes a WSDL parser. At the time of this writing, it was labeled as being in the early stages of development, but I had no problem parsing any of the WSDL files I tried. 

[![2](../images/callouts/2.png)](#soap.introspection.1.2) To use a WSDL file, you again use a proxy class, `WSDL.Proxy`, which takes a single argument: the WSDL file. Note that in this case you are passing in the URL of a WSDL file stored on the remote server, but the proxy class works just as well with a local copy of the WSDL file. The act of creating the WSDL proxy will download the WSDL file and parse it, so it there are any errors in the WSDL file (or it can't be fetched due to networking problems), you'll know about it immediately. 

[![3](../images/callouts/3.png)](#soap.introspection.1.3) The WSDL proxy class exposes the available functions as a Python dictionary, `server.methods`. So getting the list of available methods is as simple as calling the dictionary method `keys()`. 

Okay, so you know that this SOAP server offers a single method:
`getTemp`. But how do you call it? The WSDL proxy object can tell you
that too.

### Example 12.9. Discovering A Method's Arguments

    >>> callInfo = server.methods['getTemp']  
    >>> callInfo.inparams                     
    [<SOAPpy.wstools.WSDLTools.ParameterInfo instance at 0x00CF3AD0>]
    >>> callInfo.inparams[0].name             
    u'zipcode'
    >>> callInfo.inparams[0].type             
    (u'http://www.w3.org/2001/XMLSchema', u'string')



[![1](../images/callouts/1.png)](#soap.introspection.2.1) The `server.methods` dictionary is filled with a SOAPpy-specific structure called `CallInfo`. A `CallInfo` object contains information about one specific function, including the function arguments. 

[![2](../images/callouts/2.png)](#soap.introspection.2.2) The function arguments are stored in `callInfo.inparams`, which is a Python list of `ParameterInfo` objects that hold information about each parameter. 

[![3](../images/callouts/3.png)](#soap.introspection.2.3) Each `ParameterInfo` object contains a `name` attribute, which is the argument name. You are not required to know the argument name to call the function through SOAP, but SOAP does support calling functions with named arguments (just like Python), and `WSDL.Proxy` will correctly handle mapping named arguments to the remote function if you choose to use them. 

[![4](../images/callouts/4.png)](#soap.introspection.2.4) Each parameter is also explicitly typed, using datatypes defined in XML Schema. You saw this in the wire trace in the previous section; the XML Schema namespace was part of the “boilerplate” I told you to ignore. For our purposes here, you may continue to ignore it. The `zipcode` parameter is a string, and if you pass in a Python string to the `WSDL.Proxy` object, it will map it correctly and send it to the server. 

WSDL also lets you introspect into a function's return values.

### Example 12.10. Discovering A Method's Return Values

    >>> callInfo.outparams            
    [<SOAPpy.wstools.WSDLTools.ParameterInfo instance at 0x00CF3AF8>]
    >>> callInfo.outparams[0].name    
    u'return'
    >>> callInfo.outparams[0].type
    (u'http://www.w3.org/2001/XMLSchema', u'float')



[![1](../images/callouts/1.png)](#soap.introspection.3.1) The adjunct to `callInfo.inparams` for function arguments is `callInfo.outparams` for return value. It is also a list, because functions called through SOAP can return multiple values, just like Python functions. 

[![2](../images/callouts/2.png)](#soap.introspection.3.2) Each `ParameterInfo` object contains `name` and `type`. This function returns a single value, named `return`, which is a float. 

Let's put it all together, and call a SOAP web service through a WSDL
proxy.

### Example 12.11. Calling A Web Service Through A WSDL Proxy

    >>> from SOAPpy import WSDL
    >>> wsdlFile = 'http://www.xmethods.net/sd/2001/TemperatureService.wsdl')
    >>> server = WSDL.Proxy(wsdlFile)               
    >>> server.getTemp('90210')                     
    66.0
    >>> server.soapproxy.config.dumpSOAPOut = 1     
    >>> server.soapproxy.config.dumpSOAPIn = 1
    >>> temperature = server.getTemp('90210')
    *** Outgoing SOAP ******************************************************
    <?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
      xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
      xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
      xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
      xmlns:xsd="http://www.w3.org/1999/XMLSchema">
    <SOAP-ENV:Body>
    <ns1:getTemp xmlns:ns1="urn:xmethods-Temperature" SOAP-ENC:root="1">
    <v1 xsi:type="xsd:string">90210</v1>
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
    <return xsi:type="xsd:float">66.0</return>
    </ns1:getTempResponse>

    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    ************************************************************************

    >>> temperature
    66.0



[![1](../images/callouts/1.png)](#soap.introspection.4.1) The configuration is simpler than calling the SOAP service directly, since the WSDL file contains the both service URL and namespace you need to call the service. Creating the `WSDL.Proxy` object downloads the WSDL file, parses it, and configures a `SOAPProxy` object that it uses to call the actual SOAP web service. 

[![2](../images/callouts/2.png)](#soap.introspection.4.2) Once the `WSDL.Proxy` object is created, you can call a function as easily as you did with the `SOAPProxy` object. This is not surprising; the `WSDL.Proxy` is just a wrapper around the `SOAPProxy` with some introspection methods added, so the syntax for calling functions is the same. 

[![3](../images/callouts/3.png)](#soap.introspection.4.3) You can access the `WSDL.Proxy`'s `SOAPProxy` with `server.soapproxy`. This is useful to turning on debugging, so that when you can call functions through the WSDL proxy, its `SOAPProxy` will dump the outgoing and incoming XML documents that are going over the wire. 

  

