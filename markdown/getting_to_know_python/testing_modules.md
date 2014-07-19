

2.6. Testing Modules
--------------------

Python modules are objects and have several useful attributes. You can
use this to easily test your modules as you write them. Here's an
example that uses the `if` `__name__` trick.

    if __name__ == "__main__":

Some quick observations before you get to the good stuff. First,
parentheses are not required around the `if` expression. Second, the
`if` statement ends with a colon, and is followed by [indented
code](indenting_code.html "2.5. Indenting Code").


![Note](../images/note.png) 
Like C, Python uses `==` for comparison and `=` for assignment. Unlike C, Python does not support in-line assignment, so there's no chance of accidentally assigning the value you thought you were comparing. 

So why is this particular `if` statement a trick? Modules are objects,
and all modules have a built-in attribute `__name__`. A module's
`__name__` depends on how you're using the module. If you `import` the
module, then `__name__` is the module's filename, without a directory
path or file extension. But you can also run the module directly as a
standalone program, in which case `__name__` will be a special default
value, `__main__`.

    >>> import odbchelper
    >>> odbchelper.__name__
    'odbchelper'

Knowing this, you can design a test suite for your module within the
module itself by putting it in this `if` statement. When you run the
module directly, `__name__` is `__main__`, so the test suite executes.
When you import the module, `__name__` is something else, so the test
suite is ignored. This makes it easier to develop and debug new modules
before integrating them into a larger program.


![Tip](../images/tip.png) 
On MacPython, there is an additional step to make the `if` `__name__` trick work. Pop up the module's options menu by clicking the black triangle in the upper-right corner of the window, and make sure Run as \_\_main\_\_ is checked. 

### Further Reading on Importing Modules

-   [*Python Reference Manual*](http://www.python.org/doc/current/ref/)
    discusses the low-level details of [importing
    modules](http://www.python.org/doc/current/ref/import.html).

  

