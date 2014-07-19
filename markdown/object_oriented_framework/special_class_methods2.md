

5.7. Advanced Special Class Methods
-----------------------------------

Python has more special methods than just `__getitem__` and
`__setitem__`. Some of them let you emulate functionality that you may
not even know about.

This example shows some of the other special methods in `UserDict`.

### Example 5.16. More Special Methods in `UserDict`

        def __repr__(self): return repr(self.data)     
        def __cmp__(self, dict):                       
            if isinstance(dict, UserDict):            
                return cmp(self.data, dict.data)      
            else:                                     
                return cmp(self.data, dict)           
        def __len__(self): return len(self.data)       
        def __delitem__(self, key): del self.data[key] 



[![1](../images/callouts/1.png)](#fileinfo.morespecial.1.1) `__repr__` is a special method that is called when you call `repr(instance)`. The `repr` function is a built-in function that returns a string representation of an object. It works on any object, not just class instances. You're already intimately familiar with `repr` and you don't even know it. In the interactive window, when you type just a variable name and press the **ENTER** key, Python uses `repr` to display the variable's value. Go create a dictionary `d` with some data and then `print repr(d)` to see for yourself. 

[![2](../images/callouts/2.png)](#fileinfo.morespecial.1.2) `__cmp__` is called when you compare class instances. In general, you can compare any two Python objects, not just class instances, by using `==`. There are rules that define when built-in datatypes are considered equal; for instance, dictionaries are equal when they have all the same keys and values, and strings are equal when they are the same length and contain the same sequence of characters. For class instances, you can define the `__cmp__` method and code the comparison logic yourself, and then you can use `==` to compare instances of your class and Python will call your `__cmp__` special method for you. 

[![3](../images/callouts/3.png)](#fileinfo.morespecial.1.3) `__len__` is called when you call `len(instance)`. The `len` function is a built-in function that returns the length of an object. It works on any object that could reasonably be thought of as having a length. The `len` of a string is its number of characters; the `len` of a dictionary is its number of keys; the `len` of a list or tuple is its number of elements. For class instances, define the `__len__` method and code the length calculation yourself, and then call `len(instance)` and Python will call your `__len__` special method for you. 

[![4](../images/callouts/4.png)](#fileinfo.morespecial.1.4) `__delitem__` is called when you call `del instance[key]`, which you may remember as the way to [delete individual items from a dictionary](../native_data_types/index.html#odbchelper.dict.del "Example 3.5. Deleting Items from a Dictionary"). When you use `del` on a class instance, Python calls the `__delitem__` special method for you. 


![Note](../images/note.png) 
In Java, you determine whether two string variables reference the same physical memory location by using `str1 == str2`. This is called *object identity*, and it is written in Python as `str1 is str2`. To compare string values in Java, you would use `str1.equals(str2)`; in Python, you would use `str1 == str2`. Java programmers who have been taught to believe that the world is a better place because `==` in Java compares by identity instead of by value may have a difficult time adjusting to Python's lack of such “gotchas”. 

At this point, you may be thinking, “All this work just to do something
in a class that I can do with a built-in datatype.” And it's true that
life would be easier (and the entire `UserDict` class would be
unnecessary) if you could inherit from built-in datatypes like a
dictionary. But even if you could, special methods would still be
useful, because they can be used in any class, not just wrapper classes
like `UserDict`.

Special methods mean that *any class* can store key/value pairs like a
dictionary, just by defining the `__setitem__` method. *Any class* can
act like a sequence, just by defining the `__getitem__` method. Any
class that defines the `__cmp__` method can be compared with `==`. And
if your class represents something that has a length, don't define a
`GetLength` method; define the `__len__` method and use `len(instance)`.


![Note](../images/note.png) 
While other object-oriented languages only let you define the physical model of an object (“this object has a `GetLength` method”), Python's special class methods like `__len__` allow you to define the logical model of an object (“this object has a length”). 

Python has a lot of other special methods. There's a whole set of them
that let classes act like numbers, allowing you to add, subtract, and do
other arithmetic operations on class instances. (The canonical example
of this is a class that represents complex numbers, numbers with both
real and imaginary components.) The `__call__` method lets a class act
like a function, allowing you to call a class instance directly. And
there are other special methods that allow classes to have read-only and
write-only data attributes; you'll talk more about those in later
chapters.

### Further Reading on Special Class Methods

-   [*Python Reference Manual*](http://www.python.org/doc/current/ref/)
    documents [all the special class
    methods](http://www.python.org/doc/current/ref/specialnames.html).

  

