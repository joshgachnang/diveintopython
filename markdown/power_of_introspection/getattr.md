


4.4. Getting Object References With `getattr`
---------------------------------------------

-   [4.4.1. getattr with Modules](getattr.html#d0e9194)
-   [4.4.2. getattr As a Dispatcher](getattr.html#d0e9362)

You already know that [Python functions are
objects](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object").
What you don't know is that you can get a reference to a function
without knowing its name until run-time, by using the `getattr`
function.

### Example 4.10. Introducing `getattr`

    >>> li = ["Larry", "Curly"]
    >>> li.pop                       
    <built-in method pop of list object at 010DF884>
    >>> getattr(li, "pop")           
    <built-in method pop of list object at 010DF884>
    >>> getattr(li, "append")("Moe") 
    >>> li
    ["Larry", "Curly", "Moe"]
    >>> getattr({}, "clear")         
    <built-in method clear of dictionary object at 00F113D4>
    >>> getattr((), "pop")           
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    AttributeError: 'tuple' object has no attribute 'pop'



[![1](../images/callouts/1.png)](#apihelper.getattr.1.1) This gets a reference to the `pop` method of the list. Note that this is not calling the `pop` method; that would be `li.pop()`. This is the method itself. 

[![2](../images/callouts/2.png)](#apihelper.getattr.1.2) This also returns a reference to the `pop` method, but this time, the method name is specified as a string argument to the `getattr` function. `getattr` is an incredibly useful built-in function that returns any attribute of any object. In this case, the object is a list, and the attribute is the `pop` method. 

[![3](../images/callouts/3.png)](#apihelper.getattr.1.3) In case it hasn't sunk in just how incredibly useful this is, try this: the return value of `getattr` *is* the method, which you can then call just as if you had said `li.append("Moe")` directly. But you didn't call the function directly; you specified the function name as a string instead. 

[![4](../images/callouts/4.png)](#apihelper.getattr.1.4) `getattr` also works on dictionaries. 

[![5](../images/callouts/5.png)](#apihelper.getattr.1.5) In theory, `getattr` would work on tuples, except that [tuples have no methods](../native_data_types/tuples.html#odbchelper.tuplemethods "Example 3.16. Tuples Have No Methods"), so `getattr` will raise an exception no matter what attribute name you give. 

### 4.4.1. `getattr` with Modules

`getattr` isn't just for built-in datatypes. It also works on modules.

### Example 4.11. The `getattr` Function in `apihelper.py`

    >>> import odbchelper
    >>> odbchelper.buildConnectionString             
    <function buildConnectionString at 00D18DD4>
    >>> getattr(odbchelper, "buildConnectionString") 
    <function buildConnectionString at 00D18DD4>
    >>> object = odbchelper
    >>> method = "buildConnectionString"
    >>> getattr(object, method)                      
    <function buildConnectionString at 00D18DD4>
    >>> type(getattr(object, method))                
    <type 'function'>
    >>> import types
    >>> type(getattr(object, method)) == types.FunctionType
    True
    >>> callable(getattr(object, method))            
    True



[![1](../images/callouts/1.png)](#apihelper.getattr.2.1) This returns a reference to the `buildConnectionString` function in the `odbchelper` module, which you studied in [Chapter 2, *Your First Python Program*](../getting_to_know_python/index.html "Chapter 2. Your First Python Program"). (The hex address you see is specific to my machine; your output will be different.) 

[![2](../images/callouts/2.png)](#apihelper.getattr.2.2) Using `getattr`, you can get the same reference to the same function. In general, `getattr`(*object*, "*attribute*") is equivalent to `object.attribute`. If *`object`* is a module, then *`attribute`* can be anything defined in the module: a function, class, or global variable. 

[![3](../images/callouts/3.png)](#apihelper.getattr.2.3) And this is what you actually use in the `info` function. `object` is passed into the function as an argument; `method` is a string which is the name of a method or function. 

[![4](../images/callouts/4.png)](#apihelper.getattr.2.4) In this case, `method` is the name of a function, which you can prove by getting its [`type`](built_in_functions.html#apihelper.type.intro "Example 4.5. Introducing type"). 

[![5](../images/callouts/5.png)](#apihelper.getattr.2.5) Since `method` is a function, it is [callable](built_in_functions.html#apihelper.builtin.callable "Example 4.8. Introducing callable"). 

### 4.4.2. `getattr` As a Dispatcher

A common usage pattern of `getattr` is as a dispatcher. For example, if
you had a program that could output data in a variety of different
formats, you could define separate functions for each output format and
use a single dispatch function to call the right one.

For example, let's imagine a program that prints site statistics in
HTML, XML, and plain text formats. The choice of output format could be
specified on the command line, or stored in a configuration file. A
`statsout` module defines three functions, `output_html`, `output_xml`,
and `output_text`. Then the main program defines a single output
function, like this:

### Example 4.12. Creating a Dispatcher with `getattr`

    import statsout

    def output(data, format="text"):                              
        output_function = getattr(statsout, "output_%s" % format) 
        return output_function(data)                              



[![1](../images/callouts/1.png)](#apihelper.getattr.3.1) The `output` function takes one required argument, `data`, and one optional argument, `format`. If `format` is not specified, it defaults to `text`, and you will end up calling the plain text output function. 

[![2](../images/callouts/2.png)](#apihelper.getattr.3.2) You concatenate the `format` argument with "output\_" to produce a function name, and then go get that function from the `statsout` module. This allows you to easily extend the program later to support other output formats, without changing this dispatch function. Just add another function to `statsout` named, for instance, `output_pdf`, and pass "pdf" as the `format` into the `output` function. 

[![3](../images/callouts/3.png)](#apihelper.getattr.3.3) Now you can simply call the output function in the same way as any other function. The `output_function` variable is a reference to the appropriate function from the `statsout` module. 

Did you see the bug in the previous example? This is a very loose
coupling of strings and functions, and there is no error checking. What
happens if the user passes in a format that doesn't have a corresponding
function defined in `statsout`? Well, `getattr` will return `None`,
which will be assigned to `output_function` instead of a valid function,
and the next line that attempts to call that function will crash and
raise an exception. That's bad.

Luckily, `getattr` takes an optional third argument, a default value.

### Example 4.13. `getattr` Default Values

    import statsout

    def output(data, format="text"):
        output_function = getattr(statsout, "output_%s" % format, statsout.output_text)
        return output_function(data) 



[![1](../images/callouts/1.png)](#apihelper.getattr.4.1) This function call is guaranteed to work, because you added a third argument to the call to `getattr`. The third argument is a default value that is returned if the attribute or method specified by the second argument wasn't found. 

As you can see, `getattr` is quite powerful. It is the heart of
introspection, and you'll see even more powerful examples of it in later
chapters.

  

