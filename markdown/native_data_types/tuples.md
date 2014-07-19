

3.3. Introducing Tuples
-----------------------

A tuple is an immutable list. A tuple can not be changed in any way once
it is created.

### Example 3.15. Defining a tuple

    >>> t = ("a", "b", "mpilgrim", "z", "example") 
    >>> t
    ('a', 'b', 'mpilgrim', 'z', 'example')
    >>> t[0]                                       
    'a'
    >>> t[-1]                                      
    'example'
    >>> t[1:3]                                     
    ('b', 'mpilgrim')



[![1](../images/callouts/1.png)](#odbchelper.tuple.1.1) A tuple is defined in the same way as a list, except that the whole set of elements is enclosed in parentheses instead of square brackets. 

[![2](../images/callouts/2.png)](#odbchelper.tuple.1.2) The elements of a tuple have a defined order, just like a list. Tuples indices are zero-based, just like a list, so the first element of a non-empty tuple is always `t[0]`. 

[![3](../images/callouts/3.png)](#odbchelper.tuple.1.3) Negative indices count from the end of the tuple, just as with a list. 

[![4](../images/callouts/4.png)](#odbchelper.tuple.1.4) Slicing works too, just like a list. Note that when you slice a list, you get a new list; when you slice a tuple, you get a new tuple. 

### Example 3.16. Tuples Have No Methods

    >>> t
    ('a', 'b', 'mpilgrim', 'z', 'example')
    >>> t.append("new")    
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    AttributeError: 'tuple' object has no attribute 'append'
    >>> t.remove("z")      
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    AttributeError: 'tuple' object has no attribute 'remove'
    >>> t.index("example") 
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    AttributeError: 'tuple' object has no attribute 'index'
    >>> "z" in t           
    True



[![1](../images/callouts/1.png)](#odbchelper.tuple.2.1) You can't add elements to a tuple. Tuples have no `append` or `extend` method. 

[![2](../images/callouts/2.png)](#odbchelper.tuple.2.2) You can't remove elements from a tuple. Tuples have no `remove` or `pop` method. 

[![3](../images/callouts/3.png)](#odbchelper.tuple.2.3) You can't find elements in a tuple. Tuples have no `index` method. 

[![4](../images/callouts/4.png)](#odbchelper.tuple.2.4) You can, however, use `in` to see if an element exists in the tuple. 

So what are tuples good for?

-   Tuples are faster than lists. If you're defining a constant set of
    values and all you're ever going to do with it is iterate through
    it, use a tuple instead of a list.
-   It makes your code safer if you “write-protect” data that does not
    need to be changed. Using a tuple instead of a list is like having
    an implied `assert` statement that shows this data is constant, and
    that special thought (and a specific function) is required to
    override that.
-   Remember that I said that [dictionary
    keys](index.html#odbchelper.dictionarytypes "Example 3.4. Mixing Datatypes in a Dictionary")
    can be integers, strings, and “a few other types”? Tuples are one of
    those types. Tuples can be used as keys in a dictionary, but lists
    can't be used this way.Actually, it's more complicated than that.
    Dictionary keys must be immutable. Tuples themselves are immutable,
    but if you have a tuple of lists, that counts as mutable and isn't
    safe to use as a dictionary key. Only tuples of strings, numbers, or
    other dictionary-safe tuples can be used as dictionary keys.
-   Tuples are used in string formatting, as you'll see shortly.


![Note](../images/note.png) 
Tuples can be converted into lists, and vice-versa. The built-in `tuple` function takes a list and returns a tuple with the same elements, and the `list` function takes a tuple and returns a list. In effect, `tuple` freezes a list, and `list` thaws a tuple. 

### Further Reading on Tuples

-   [*How to Think Like a Computer
    Scientist*](http://www.ibiblio.org/obp/thinkCSpy/ "Python book for computer science majors")
    teaches about tuples and shows how to [concatenate
    tuples](http://www.ibiblio.org/obp/thinkCSpy/chap10.htm).
-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    shows how to [sort a
    tuple](http://www.faqts.com/knowledge-base/view.phtml/aid/4553/fid/587).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    shows how to [define a tuple with one
    element](http://www.python.org/doc/current/tut/node7.html#SECTION007300000000000000000).

  

