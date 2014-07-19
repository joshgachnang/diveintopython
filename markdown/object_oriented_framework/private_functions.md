

5.9. Private Functions
----------------------

Like most languages, Python has the concept of private elements:

-   Private functions, which can't be called from outside their module
-   Private class methods, which can't be called from outside their
    class
-   Private attributes, which can't be accessed from outside their
    class.

Unlike in most languages, whether a Python function, method, or
attribute is private or public is determined entirely by its name.

If the name of a Python function, class method, or attribute starts with
(but doesn't end with) two underscores, it's private; everything else is
public. Python has no concept of *protected* class methods (accessible
only in their own class and descendant classes). Class methods are
either private (accessible only in their own class) or public
(accessible from anywhere).

In `MP3FileInfo`, there are two methods: `__parse` and `__setitem__`. As
you have already discussed, `__setitem__` is a [special
method](special_class_methods.html#fileinfo.specialmethods.setitem.example "Example 5.13. The __setitem__ Special Method");
normally, you would call it indirectly by using the dictionary syntax on
a class instance, but it is public, and you could call it directly (even
from outside the `fileinfo` module) if you had a really good reason.
However, `__parse` is private, because it has two underscores at the
beginning of its name.


![Note](../images/note.png) 
In Python, all special methods (like [`__setitem__`](special_class_methods.html#fileinfo.specialmethods.setitem.example "Example 5.13. The __setitem__ Special Method")) and built-in attributes (like [`__doc__`](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string")) follow a standard naming convention: they both start with and end with two underscores. Don't name your own methods and attributes this way, because it will only confuse you (and others) later. 

### Example 5.19. Trying to Call a Private Method

    >>> import fileinfo
    >>> m = fileinfo.MP3FileInfo()
    >>> m.__parse("/music/_singles/kairo.mp3") 
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    AttributeError: 'MP3FileInfo' instance has no attribute '__parse'



[![1](../images/callouts/1.png)](#fileinfo.private.1.1) If you try to call a private method, Python will raise a slightly misleading exception, saying that the method does not exist. Of course it does exist, but it's private, so it's not accessible outside the class.Strictly speaking, private methods are accessible outside their class, just not *easily* accessible. Nothing in Python is truly private; internally, the names of private methods and attributes are mangled and unmangled on the fly to make them seem inaccessible by their given names. You can access the `__parse` method of the `MP3FileInfo` class by the name `_MP3FileInfo__parse`. Acknowledge that this is interesting, but promise to never, ever do it in real code. Private methods are private for a reason, but like many other things in Python, their privateness is ultimately a matter of convention, not force. 

### Further Reading on Private Functions

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses the inner workings of [private
    variables](http://www.python.org/doc/current/tut/node11.html#SECTION0011600000000000000000).

  

