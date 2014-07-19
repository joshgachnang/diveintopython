

5.5. Exploring `UserDict`: A Wrapper Class
------------------------------------------

As you've seen, `FileInfo` is a class that acts like a dictionary. To
explore this further, let's look at the `UserDict` class in the
`UserDict` module, which is the ancestor of the `FileInfo` class. This
is nothing special; the class is written in Python and stored in a `.py`
file, just like any other Python code. In particular, it's stored in the
`lib` directory in your Python installation.


![Tip](../images/tip.png) 
In the ActivePython IDE on Windows, you can quickly open any module in your library path by selecting File-\>Locate... (****Ctrl**-L**). 

### Example 5.9. Defining the `UserDict` Class

    class UserDict:                                
        def __init__(self, dict=None):             
            self.data = {}                         
            if dict is not None: self.update(dict)  



[![1](../images/callouts/1.png)](#fileinfo.userdict.1.1) Note that `UserDict` is a base class, not inherited from any other class. 

[![2](../images/callouts/2.png)](#fileinfo.userdict.1.2) This is the `__init__` method that you [overrode in the `FileInfo` class](defining_classes.html#fileinfo.class.example "Example 5.4. Defining the FileInfo Class"). Note that the argument list in this ancestor class is different than the descendant. That's okay; each subclass can have its own set of arguments, as long as it calls the ancestor with the correct arguments. Here the ancestor class has a way to define initial values (by passing a dictionary in the `dict` argument) which the `FileInfo` does not use. 

[![3](../images/callouts/3.png)](#fileinfo.userdict.1.3) Python supports data attributes (called “instance variables” in Java and Powerbuilder, and “member variables” in C++). Data attributes are pieces of data held by a specific instance of a class. In this case, each instance of `UserDict` will have a data attribute `data`. To reference this attribute from code outside the class, you qualify it with the instance name, `instance.data`, in the same way that you qualify a function with its module name. To reference a data attribute from within the class, you use `self` as the qualifier. By convention, all data attributes are initialized to reasonable values in the `__init__` method. However, this is not required, since data attributes, like local variables, [spring into existence](../native_data_types/declaring_variables.html "3.4. Declaring variables") when they are first assigned a value. 

[![4](../images/callouts/4.png)](#fileinfo.userdict.1.4) The `update` method is a dictionary duplicator: it copies all the keys and values from one dictionary to another. This does *not* clear the target dictionary first; if the target dictionary already has some keys, the ones from the source dictionary will be overwritten, but others will be left untouched. Think of `update` as a merge function, not a copy function. 

[![5](../images/callouts/5.png)](#fileinfo.userdict.1.5) This is a syntax you may not have seen before (I haven't used it in the examples in this book). It's an `if` statement, but instead of having an indented block starting on the next line, there is just a single statement on the same line, after the colon. This is perfectly legal syntax, which is just a shortcut you can use when you have only one statement in a block. (It's like specifying a single statement without braces in C++.) You can use this syntax, or you can have indented code on subsequent lines, but you can't do both for the same block. 


![Note](../images/note.png) 
Java and Powerbuilder support function overloading by argument list, *i.e.* one class can have multiple methods with the same name but a different number of arguments, or arguments of different types. Other languages (most notably PL/SQL) even support function overloading by argument name; *i.e.* one class can have multiple methods with the same name and the same number of arguments of the same type but different argument names. Python supports neither of these; it has no form of function overloading whatsoever. Methods are defined solely by their name, and there can be only one method per class with a given name. So if a descendant class has an `__init__` method, it *always* overrides the ancestor `__init__` method, even if the descendant defines it with a different argument list. And the same rule applies to any other method. 


![Note](../images/note.png) 
Guido, the original author of Python, explains method overriding this way: "Derived classes may override methods of their base classes. Because methods have no special privileges when calling other methods of the same object, a method of a base class that calls another method defined in the same base class, may in fact end up calling a method of a derived class that overrides it. (For C++ programmers: all methods in Python are effectively virtual.)" If that doesn't make sense to you (it confuses the hell out of me), feel free to ignore it. I just thought I'd pass it along. 


![Caution](../images/caution.png) 
Always assign an initial value to all of an instance's data attributes in the `__init__` method. It will save you hours of debugging later, tracking down `AttributeError` exceptions because you're referencing uninitialized (and therefore non-existent) attributes. 

### Example 5.10. `UserDict` Normal Methods

        def clear(self): self.data.clear()          
        def copy(self):                             
            if self.__class__ is UserDict:          
                return UserDict(self.data)         
            import copy                             
            return copy.copy(self)                 
        def keys(self): return self.data.keys()     
        def items(self): return self.data.items()  
        def values(self): return self.data.values()



[![1](../images/callouts/1.png)](#fileinfo.userdict.2.1) `clear` is a normal class method; it is publicly available to be called by anyone at any time. Notice that `clear`, like all class methods, has `self` as its first argument. (Remember that you don't include `self` when you call the method; it's something that Python adds for you.) Also note the basic technique of this wrapper class: store a real dictionary (`data`) as a data attribute, define all the methods that a real dictionary has, and have each class method redirect to the corresponding method on the real dictionary. (In case you'd forgotten, a dictionary's `clear` method [deletes all of its keys](../native_data_types/index.html#odbchelper.dict.del "Example 3.5. Deleting Items from a Dictionary") and their associated values.) 

[![2](../images/callouts/2.png)](#fileinfo.userdict.2.2) The `copy` method of a real dictionary returns a new dictionary that is an exact duplicate of the original (all the same key-value pairs). But `UserDict` can't simply redirect to `self.data.copy`, because that method returns a real dictionary, and what you want is to return a new instance that is the same class as `self`. 

[![3](../images/callouts/3.png)](#fileinfo.userdict.2.3) You use the `__class__` attribute to see if `self` is a `UserDict`; if so, you're golden, because you know how to copy a `UserDict`: just create a new `UserDict` and give it the real dictionary that you've squirreled away in `self.data`. Then you immediately return the new `UserDict` you don't even get to the `import copy` on the next line. 

[![4](../images/callouts/4.png)](#fileinfo.userdict.2.4) If `self.__class__` is not `UserDict`, then `self` must be some subclass of `UserDict` (like maybe `FileInfo`), in which case life gets trickier. `UserDict` doesn't know how to make an exact copy of one of its descendants; there could, for instance, be other data attributes defined in the subclass, so you would need to iterate through them and make sure to copy all of them. Luckily, Python comes with a module to do exactly this, and it's called `copy`. I won't go into the details here (though it's a wicked cool module, if you're ever inclined to dive into it on your own). Suffice it to say that `copy` can copy arbitrary Python objects, and that's how you're using it here. 

[![5](../images/callouts/5.png)](#fileinfo.userdict.2.5) The rest of the methods are straightforward, redirecting the calls to the built-in methods on `self.data`. 


![Note](../images/note.png) 
In versions of Python prior to 2.2, you could not directly subclass built-in datatypes like strings, lists, and dictionaries. To compensate for this, Python comes with wrapper classes that mimic the behavior of these built-in datatypes: `UserString`, `UserList`, and `UserDict`. Using a combination of normal and special methods, the `UserDict` class does an excellent imitation of a dictionary. In Python 2.2 and later, you can inherit classes directly from built-in datatypes like `dict`. An example of this is given in the examples that come with this book, in `fileinfo_fromdict.py`. 

In Python, you can inherit directly from the `dict` built-in datatype,
as shown in this example. There are three differences here compared to
the `UserDict` version.

### Example 5.11. Inheriting Directly from Built-In Datatype `dict`

    class FileInfo(dict):                  
        "store file metadata"
        def __init__(self, filename=None): 
            self["name"] = filename



[![1](../images/callouts/1.png)](#fileinfo.userdict.3.1) The first difference is that you don't need to import the `UserDict` module, since `dict` is a built-in datatype and is always available. The second is that you are inheriting from `dict` directly, instead of from `UserDict.UserDict`. 

[![2](../images/callouts/2.png)](#fileinfo.userdict.3.2) The third difference is subtle but important. Because of the way `UserDict` works internally, it requires you to manually call its `__init__` method to properly initialize its internal data structures. `dict` does not work like this; it is not a wrapper, and it requires no explicit initialization. 

### Further Reading on `UserDict`

-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the [`UserDict`
    module](http://www.python.org/doc/current/lib/module-UserDict.html)
    and the [`copy`
    module](http://www.python.org/doc/current/lib/module-copy.html).

  

