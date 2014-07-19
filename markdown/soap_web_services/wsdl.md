

12.5. Introducing WSDL
----------------------

The `SOAPProxy` class proxies local method calls and transparently turns
then into invocations of remote SOAP methods. As you've seen, this is a
lot of work, and `SOAPProxy` does it quickly and transparently. What it
doesn't do is provide any means of method introspection.

Consider this: the previous two sections showed an example of calling a
simple remote SOAP method with one argument and one return value, both
of simple data types. This required knowing, and keeping track of, the
service URL, the service namespace, the function name, the number of
arguments, and the datatype of each argument. If any of these is missing
or wrong, the whole thing falls apart.

That shouldn't come as a big surprise. If I wanted to call a local
function, I would need to know what package or module it was in (the
equivalent of service URL and namespace). I would need to know the
correct function name and the correct number of arguments. Python deftly
handles datatyping without explicit types, but I would still need to
know how many argument to pass, and how many return values to expect.

The big difference is introspection. As you saw in [Chapter
4](../power_of_introspection/index.html), Python excels at letting you
discover things about modules and functions at runtime. You can list the
available functions within a module, and with a little work, drill down
to individual function declarations and arguments.

WSDL lets you do that with SOAP web services. WSDL stands for “Web
Services Description Language”. Although designed to be flexible enough
to describe many types of web services, it is most often used to
describe SOAP web services.

A WSDL file is just that: a file. More specifically, it's an XML file.
It usually lives on the same server you use to access the SOAP web
services it describes, although there's nothing special about it. Later
in this chapter, we'll download the WSDL file for the Google API and use
it locally. That doesn't mean we're calling Google locally; the WSDL
file still describes the remote functions sitting on Google's server.

A WSDL file contains a description of everything involved in calling a
SOAP web service:

-   The service URL and namespace
-   The type of web service (probably function calls using SOAP,
    although as I mentioned, WSDL is flexible enough to describe a wide
    variety of web services)
-   The list of available functions
-   The arguments for each function
-   The datatype of each argument
-   The return values of each function, and the datatype of each return
    value

In other words, a WSDL file tells you everything you need to know to be
able to call a SOAP web service.

  

