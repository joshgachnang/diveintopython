

-   [4.3.1. The type Function](built_in_functions.html#d0e8510)
-   [4.3.2. The str Function](built_in_functions.html#d0e8609)
-   [4.3.3. Built-In Functions](built_in_functions.html#d0e8958)

4.3. Using `type`, `str`, `dir`, and Other Built-In Functions
-------------------------------------------------------------

-   [4.3.1. The type Function](built_in_functions.html#d0e8510)
-   [4.3.2. The str Function](built_in_functions.html#d0e8609)
-   [4.3.3. Built-In Functions](built_in_functions.html#d0e8958)

Python has a small set of extremely useful built-in functions. All other
functions are partitioned off into modules. This was actually a
conscious design decision, to keep the core language from getting
bloated like other scripting languages (cough cough, Visual Basic).

### 4.3.1. The `type` Function

The `type` function returns the datatype of any arbitrary object. The
possible types are listed in the `types` module. This is useful for
helper functions that can handle several types of data.

### Example 4.5. Introducing `type`

    >>> type(1)           
    <type 'int'>
    >>> li =
    >>> type(li)          
    <type 'list'>
    >>> import odbchelper
    >>> type(odbchelper)  
    <type 'module'>
    >>> import types      
    >>> type(odbchelper) == types.ModuleType
    True



[![1](../images/callouts/1.png)](#apihelper.builtin.1.1) `type` takes anything -- and I mean anything -- and returns its datatype. Integers, strings, lists, dictionaries, tuples, functions, classes, modules, even types are acceptable. 

[![2](../images/callouts/2.png)](#apihelper.builtin.1.2) `type` can take a variable and return its datatype. 

[![3](../images/callouts/3.png)](#apihelper.builtin.1.3) `type` also works on modules. 

[![4](../images/callouts/4.png)](#apihelper.builtin.1.4) You can use the constants in the `types` module to compare types of objects. This is what the `info` function does, as you'll see shortly. 

### 4.3.2. The `str` Function

The `str` coerces data into a string. Every datatype can be coerced into
a string.

### Example 4.6. Introducing `str`

    >>> str(1)          
    '1'
    >>> horsemen = ['war', 'pestilence', 'famine']
    >>> horsemen
    ['war', 'pestilence', 'famine']
    >>> horsemen.append('Powerbuilder')
    >>> str(horsemen)   
    "['war', 'pestilence', 'famine', 'Powerbuilder']"
    >>> str(odbchelper) 
    "<module 'odbchelper' from 'c:\\docbook\\dip\\py\\odbchelper.py'>"
    >>> str(None)       
    'None'



[![1](../images/callouts/1.png)](#apihelper.builtin.2.1) For simple datatypes like integers, you would expect `str` to work, because almost every language has a function to convert an integer to a string. 

[![2](../images/callouts/2.png)](#apihelper.builtin.2.2) However, `str` works on any object of any type. Here it works on a list which you've constructed in bits and pieces. 

[![3](../images/callouts/3.png)](#apihelper.builtin.2.3) `str` also works on modules. Note that the string representation of the module includes the pathname of the module on disk, so yours will be different. 

[![4](../images/callouts/4.png)](#apihelper.builtin.2.4) A subtle but important behavior of `str` is that it works on `None`, the Python null value. It returns the string `'None'`. You'll use this to your advantage in the `info` function, as you'll see shortly. 

At the heart of the `info` function is the powerful `dir` function.
`dir` returns a list of the attributes and methods of any object:
modules, functions, strings, lists, dictionaries... pretty much
anything.

### Example 4.7. Introducing `dir`

    >>> li =
    >>> dir(li)           
    ['append', 'count', 'extend', 'index', 'insert',
    'pop', 'remove', 'reverse', 'sort']
    >>> d = {}
    >>> dir(d)            
    ['clear', 'copy', 'get', 'has_key', 'items', 'keys', 'setdefault', 'update', 'values']
    >>> import odbchelper
    >>> dir(odbchelper)   
    ['__builtins__', '__doc__', '__file__', '__name__', 'buildConnectionString']



[![1](../images/callouts/1.png)](#apihelper.builtin.3.1) `li` is a list, so `dir`(`li`) returns a list of all the methods of a list. Note that the returned list contains the names of the methods as strings, not the methods themselves. 

[![2](../images/callouts/2.png)](#apihelper.builtin.3.2) `d` is a dictionary, so `dir`(`d`) returns a list of the names of dictionary methods. At least one of these, [`keys`](../native_data_types/mapping_lists.html#odbchelper.items "Example 3.25. The keys, values, and items Functions"), should look familiar. 

[![3](../images/callouts/3.png)](#apihelper.builtin.3.3) This is where it really gets interesting. `odbchelper` is a module, so `dir`(`odbchelper`) returns a list of all kinds of stuff defined in the module, including built-in attributes, like [`__name__`](../getting_to_know_python/testing_modules.html#odbchelper.ifnametrick), [`__doc__`](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string"), and whatever other attributes and methods you define. In this case, `odbchelper` has only one user-defined method, the `buildConnectionString` function described in [Chapter 2](../getting_to_know_python/index.html). 

Finally, the `callable` function takes any object and returns `True` if
the object can be called, or `False` otherwise. Callable objects include
functions, class methods, even classes themselves. (More on classes in
the next chapter.)

### Example 4.8. Introducing `callable`

    >>> import string
    >>> string.punctuation           
    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{ }~'
    >>> string.join                  
    <function join at 00C55A7C>
    >>> callable(string.punctuation) 
    False
    >>> callable(string.join)        
    True
    >>> print string.join.__doc__    
    join(list [,sep]) -> string

        Return a string composed of the words in list, with
        intervening occurrences of sep.  The default separator is a
        single space.

        (joinfields and join are synonymous)



[![1](../images/callouts/1.png)](#apihelper.builtin.4.1) The functions in the `string` module are deprecated (although many people still use the `join` function), but the module contains a lot of useful constants like this `string.punctuation`, which contains all the standard punctuation characters. 

[![2](../images/callouts/2.png)](#apihelper.builtin.4.2) [`string.join`](../native_data_types/joining_lists.html "3.7. Joining Lists and Splitting Strings") is a function that joins a list of strings. 

[![3](../images/callouts/3.png)](#apihelper.builtin.4.3) `string.punctuation` is not callable; it is a string. (A string does have callable methods, but the string itself is not callable.) 

[![4](../images/callouts/4.png)](#apihelper.builtin.4.4) `string.join` is callable; it's a function that takes two arguments. 

[![5](../images/callouts/5.png)](#apihelper.builtin.4.5) Any callable object may have a `doc string`. By using the `callable` function on each of an object's attributes, you can determine which attributes you care about (methods, functions, classes) and which you want to ignore (constants and so on) without knowing anything about the object ahead of time. 

### 4.3.3. Built-In Functions

`type`, `str`, `dir`, and all the rest of Python's built-in functions
are grouped into a special module called `__builtin__`. (That's two
underscores before and after.) If it helps, you can think of Python
automatically executing `from __builtin__ import *` on startup, which
imports all the “built-in” functions into the namespace so you can use
them directly.

The advantage of thinking like this is that you can access all the
built-in functions and attributes as a group by getting information
about the `__builtin__` module. And guess what, Python has a function
called `info`. Try it yourself and skim through the list now. We'll dive
into some of the more important functions later. (Some of the built-in
error classes, like
[`AttributeError`](../native_data_types/tuples.html#odbchelper.tuplemethods "Example 3.16. Tuples Have No Methods"),
should already look familiar.)

### Example 4.9. Built-in Attributes and Functions

    >>> from apihelper import info
    >>> import __builtin__
    >>> info(__builtin__, 20)
    ArithmeticError      Base class for arithmetic errors.
    AssertionError       Assertion failed.
    AttributeError       Attribute not found.
    EOFError             Read beyond end of file.
    EnvironmentError     Base class for I/O related errors.
    Exception            Common base class for all exceptions.
    FloatingPointError   Floating point operation failed.
    IOError              I/O operation failed.

    [...snip...]


![Note](../images/note.png) 
Python comes with excellent reference manuals, which you should peruse thoroughly to learn all the modules Python has to offer. But unlike most languages, where you would find yourself referring back to the manuals or man pages to remind yourself how to use these modules, Python is largely self-documenting. 

### Further Reading on Built-In Functions

-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents [all the built-in
    functions](http://www.python.org/doc/current/lib/built-in-funcs.html)
    and [all the built-in
    exceptions](http://www.python.org/doc/current/lib/module-exceptions.html).

  

