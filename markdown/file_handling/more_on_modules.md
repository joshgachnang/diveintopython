

6.4. Using `sys`.modules
------------------------

Modules, like everything else in Python, are objects. Once imported, you
can always get a reference to a module through the global dictionary
`sys`.modules.

### Example 6.12. Introducing `sys`.modules

    >>> import sys                          
    >>> print '\n'.join(sys.modules.keys()) 
    win32api
    os.path
    os
    exceptions
    __main__
    ntpath
    nt
    sys
    __builtin__
    site
    signal
    UserDict
    stat



[![1](../images/callouts/1.png)](#fileinfo.modules.1.1) The `sys` module contains system-level information, such as the version of Python you're running (`sys`.version or `sys`.version\_info), and system-level options such as the maximum allowed recursion depth (`sys`.getrecursionlimit() and `sys`.setrecursionlimit()). 

[![2](../images/callouts/2.png)](#fileinfo.modules.1.2) `sys`.modules is a dictionary containing all the modules that have ever been imported since Python was started; the key is the module name, the value is the module object. Note that this is more than just the modules *your* program has imported. Python preloads some modules on startup, and if you're using a Python IDE, `sys`.modules contains all the modules imported by all the programs you've run within the IDE. 

This example demonstrates how to use `sys`.modules.

### Example 6.13. Using `sys`.modules

    >>> import fileinfo         
    >>> print '\n'.join(sys.modules.keys())
    win32api
    os.path
    os
    fileinfo
    exceptions
    __main__
    ntpath
    nt
    sys
    __builtin__
    site
    signal
    UserDict
    stat
    >>> fileinfo
    <module 'fileinfo' from 'fileinfo.pyc'>
    >>> sys.modules["fileinfo"] 
    <module 'fileinfo' from 'fileinfo.pyc'>



[![1](../images/callouts/1.png)](#fileinfo.modules.1.3) As new modules are imported, they are added to `sys`.modules. This explains why importing the same module twice is very fast: Python has already loaded and cached the module in `sys`.modules, so importing the second time is simply a dictionary lookup. 

[![2](../images/callouts/2.png)](#fileinfo.modules.1.4) Given the name (as a string) of any previously-imported module, you can get a reference to the module itself through the `sys`.modules dictionary. 

The next example shows how to use the `__module__` class attribute with
the `sys`.modules dictionary to get a reference to the module in which a
class is defined.

### Example 6.14. The `__module__` Class Attribute

    >>> from fileinfo import MP3FileInfo
    >>> MP3FileInfo.__module__              
    'fileinfo'
    >>> sys.modules[MP3FileInfo.__module__] 
    <module 'fileinfo' from 'fileinfo.pyc'>



[![1](../images/callouts/1.png)](#fileinfo.modules.2.1) Every Python class has a built-in [class attribute](../object_oriented_framework/class_attributes.html "5.8. Introducing Class Attributes") `__module__`, which is the name of the module in which the class is defined. 

[![2](../images/callouts/2.png)](#fileinfo.modules.2.2) Combining this with the `sys`.modules dictionary, you can get a reference to the module in which a class is defined. 

Now you're ready to see how `sys`.modules is used in `fileinfo.py`, the
sample program introduced in [Chapter
5](../object_oriented_framework/index.html). This example shows that
portion of the code.

### Example 6.15. `sys`.modules in `fileinfo.py`

        def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):       
            "get file info class from filename extension"                             
            subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]        
            return hasattr(module, subclass) and getattr(module, subclass) or FileInfo 



[![1](../images/callouts/1.png)](#fileinfo.modules.3.1) This is a function with two arguments; `filename` is required, but `module` is [optional](../power_of_introspection/optional_arguments.html "4.2. Using Optional and Named Arguments") and defaults to the module that contains the `FileInfo` class. This looks inefficient, because you might expect Python to evaluate the `sys`.modules expression every time the function is called. In fact, Python evaluates default expressions only once, the first time the module is imported. As you'll see later, you never call this function with a `module` argument, so `module` serves as a function-level constant. 

[![2](../images/callouts/2.png)](#fileinfo.modules.3.2) You'll plow through this line later, after you dive into the `os` module. For now, take it on faith that `subclass` ends up as the name of a class, like `MP3FileInfo`. 

[![3](../images/callouts/3.png)](#fileinfo.modules.3.3) You already know about [`getattr`](../power_of_introspection/getattr.html "4.4. Getting Object References With getattr"), which gets a reference to an object by name. `hasattr` is a complementary function that checks whether an object has a particular attribute; in this case, whether a module has a particular class (although it works for any object and any attribute, just like `getattr`). In English, this line of code says, “If this module has the class named by `subclass` then return it, otherwise return the base class `FileInfo`.” 

### Further Reading on Modules

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses exactly [when and how default arguments are
    evaluated](http://www.python.org/doc/current/tut/node6.html#SECTION006710000000000000000).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the
    [`sys`](http://www.python.org/doc/current/lib/module-sys.html)
    module.

  

