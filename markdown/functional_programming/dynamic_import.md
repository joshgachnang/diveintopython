

16.6. Dynamically importing modules
-----------------------------------

OK, enough philosophizing. Let's talk about dynamically importing
modules.

First, let's look at how you normally import modules. The
`import module` syntax looks in the search path for the named module and
imports it by name. You can even import multiple modules at once this
way, with a comma-separated list. You did this on the very first line of
this chapter's script.

### Example 16.13. Importing multiple modules at once

    import sys, os, re, unittest 



[![1](../images/callouts/1.png)](#regression.import.1.1) This imports four modules at once: `sys` (for system functions and access to the command line parameters), `os` (for operating system functions like directory listings), `re` (for regular expressions), and `unittest` (for unit testing). 

Now let's do the same thing, but with dynamic imports.

### Example 16.14. Importing modules dynamically

    >>> sys = __import__('sys')           
    >>> os = __import__('os')
    >>> re = __import__('re')
    >>> unittest = __import__('unittest')
    >>> sys                               
    >>> <module 'sys' (built-in)>
    >>> os
    >>> <module 'os' from '/usr/local/lib/python2.2/os.pyc'>



[![1](../images/callouts/1.png)](#regression.import.2.1) The built-in `__import__` function accomplishes the same goal as using the `import` statement, but it's an actual function, and it takes a string as an argument. 

[![2](../images/callouts/2.png)](#regression.import.2.2) The variable `sys` is now the `sys` module, just as if you had said `import sys`. The variable `os` is now the `os` module, and so forth. 

So `__import__` imports a module, but takes a string argument to do it.
In this case the module you imported was just a hard-coded string, but
it could just as easily be a variable, or the result of a function call.
And the variable that you assign the module to doesn't need to match the
module name, either. You could import a series of modules and assign
them to a list.

### Example 16.15. Importing a list of modules dynamically

    >>> moduleNames = ['sys', 'os', 're', 'unittest'] 
    >>> moduleNames
    ['sys', 'os', 're', 'unittest']
    >>> modules = map(__import__, moduleNames)        
    >>> modules                                       
    [<module 'sys' (built-in)>,
    <module 'os' from 'c:\Python22\lib\os.pyc'>,
    <module 're' from 'c:\Python22\lib\re.pyc'>,
    <module 'unittest' from 'c:\Python22\lib\unittest.pyc'>]
    >>> modules[0].version                            
    '2.2.2 (#37, Nov 26 2002, 10:24:37) [MSC 32 bit (Intel)]'
    >>> import sys
    >>> sys.version
    '2.2.2 (#37, Nov 26 2002, 10:24:37) [MSC 32 bit (Intel)]'



[![1](../images/callouts/1.png)](#regression.import.3.1) `moduleNames` is just a list of strings. Nothing fancy, except that the strings happen to be names of modules that you could import, if you wanted to. 

[![2](../images/callouts/2.png)](#regression.import.3.2) Surprise, you wanted to import them, and you did, by mapping the `__import__` function onto the list. Remember, this takes each element of the list (`moduleNames`) and calls the function (`__import__`) over and over, once with each element of the list, builds a list of the return values, and returns the result. 

[![3](../images/callouts/3.png)](#regression.import.3.3) So now from a list of strings, you've created a list of actual modules. (Your paths may be different, depending on your operating system, where you installed Python, the phase of the moon, etc.) 

[![4](../images/callouts/4.png)](#regression.import.3.4) To drive home the point that these are real modules, let's look at some module attributes. Remember, `modules[0]` *is* the `sys` module, so `modules[0].version` *is* `sys.version`. All the other attributes and methods of these modules are also available. There's nothing magic about the `import` statement, and there's nothing magic about modules. Modules are objects. Everything is an object. 

Now you should be able to put this all together and figure out what most
of this chapter's code sample is doing.

  

