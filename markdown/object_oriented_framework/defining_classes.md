

5.3. Defining Classes
---------------------

-   [5.3.1. Initializing and Coding
    Classes](defining_classes.html#d0e11720)
-   [5.3.2. Knowing When to Use self and
    \_\_init\_\_](defining_classes.html#d0e11896)

Python is fully object-oriented: you can define your own classes,
inherit from your own or built-in classes, and instantiate the classes
you've defined.

Defining a class in Python is simple. As with functions, there is no
separate interface definition. Just define the class and start coding. A
Python class starts with the reserved word `class`, followed by the
class name. Technically, that's all that's required, since a class
doesn't need to inherit from any other class.

### Example 5.3. The Simplest Python Class

    class Loaf: 
        pass     



[![1](../images/callouts/1.png)](#fileinfo.class.1.1) The name of this class is `Loaf`, and it doesn't inherit from any other class. Class names are usually capitalized, `EachWordLikeThis`, but this is only a convention, not a requirement. 

[![2](../images/callouts/2.png)](#fileinfo.class.1.2) This class doesn't define any methods or attributes, but syntactically, there needs to be something in the definition, so you use `pass`. This is a Python reserved word that just means “move along, nothing to see here”. It's a statement that does nothing, and it's a good placeholder when you're stubbing out functions or classes. 

[![3](../images/callouts/3.png)](#fileinfo.class.1.3) You probably guessed this, but everything in a class is indented, just like the code within a function, `if` statement, `for` loop, and so forth. The first thing not indented is not in the class. 


![Note](../images/note.png) 
The `pass` statement in Python is like an empty set of braces (`{}`) in Java or C. 

Of course, realistically, most classes will be inherited from other
classes, and they will define their own class methods and attributes.
But as you've just seen, there is nothing that a class absolutely must
have, other than a name. In particular, C++ programmers may find it odd
that Python classes don't have explicit constructors and destructors.
Python classes do have something similar to a constructor: the
`__init__` method.

### Example 5.4. Defining the `FileInfo` Class

    from UserDict import UserDict

    class FileInfo(UserDict): 



[![1](../images/callouts/1.png)](#fileinfo.class.2.1) In Python, the ancestor of a class is simply listed in parentheses immediately after the class name. So the `FileInfo` class is inherited from the `UserDict` class (which was [imported from the `UserDict` module](importing_modules.html "5.2. Importing Modules Using from module import")). `UserDict` is a class that acts like a dictionary, allowing you to essentially subclass the dictionary datatype and add your own behavior. (There are similar classes `UserList` and `UserString` which allow you to subclass lists and strings.) There is a bit of black magic behind this, which you will demystify later in this chapter when you explore the `UserDict` class in more depth. 


![Note](../images/note.png) 
In Python, the ancestor of a class is simply listed in parentheses immediately after the class name. There is no special keyword like `extends` in Java. 

Python supports multiple inheritance. In the parentheses following the
class name, you can list as many ancestor classes as you like, separated
by commas.

### 5.3.1. Initializing and Coding Classes

This example shows the initialization of the `FileInfo` class using the
`__init__` method.

### Example 5.5. Initializing the `FileInfo` Class

    class FileInfo(UserDict):
        "store file metadata"              
        def __init__(self, filename=None):   



[![1](../images/callouts/1.png)](#fileinfo.class.2.2) Classes can (and [should](../getting_to_know_python/documenting_functions.html#tip.docstring)) have `doc string`s too, just like modules and functions. 

[![2](../images/callouts/2.png)](#fileinfo.class.2.3) `__init__` is called immediately after an instance of the class is created. It would be tempting but incorrect to call this the constructor of the class. It's tempting, because it looks like a constructor (by convention, `__init__` is the first method defined for the class), acts like one (it's the first piece of code executed in a newly created instance of the class), and even sounds like one (“init” certainly suggests a constructor-ish nature). Incorrect, because the object has already been constructed by the time `__init__` is called, and you already have a valid reference to the new instance of the class. But `__init__` is the closest thing you're going to get to a constructor in Python, and it fills much the same role. 

[![3](../images/callouts/3.png)](#fileinfo.class.2.4) The first argument of every class method, including `__init__`, is always a reference to the current instance of the class. By convention, this argument is always named `self`. In the `__init__` method, `self` refers to the newly created object; in other class methods, it refers to the instance whose method was called. Although you need to specify `self` explicitly when defining the method, you do *not* specify it when calling the method; Python will add it for you automatically. 

[![4](../images/callouts/4.png)](#fileinfo.class.2.5) `__init__` methods can take any number of arguments, and just like functions, the arguments can be defined with default values, making them optional to the caller. In this case, `filename` has a default value of `None`, which is the Python null value. 


![Note](../images/note.png) 
By convention, the first argument of any Python class method (the reference to the current instance) is called `self`. This argument fills the role of the reserved word `this` in C++ or Java, but `self` is not a reserved word in Python, merely a naming convention. Nonetheless, please don't call it anything but `self`; this is a very strong convention. 

### Example 5.6. Coding the `FileInfo` Class

    class FileInfo(UserDict):
        "store file metadata"
        def __init__(self, filename=None):
            UserDict.__init__(self)        
            self["name"] = filename        
                                           



[![1](../images/callouts/1.png)](#fileinfo.class.2.6) Some pseudo-object-oriented languages like Powerbuilder have a concept of “extending” constructors and other events, where the ancestor's method is called automatically before the descendant's method is executed. Python does not do this; you must always explicitly call the appropriate method in the ancestor class. 

[![2](../images/callouts/2.png)](#fileinfo.class.2.7) I told you that this class acts like a dictionary, and here is the first sign of it. You're assigning the argument `filename` as the value of this object's `name` key. 

[![3](../images/callouts/3.png)](#fileinfo.class.2.8) Note that the `__init__` method never returns a value. 

### 5.3.2. Knowing When to Use `self` and `__init__`

When defining your class methods, you *must* explicitly list `self` as
the first argument for each method, including `__init__`. When you call
a method of an ancestor class from within your class, you *must* include
the `self` argument. But when you call your class method from outside,
you do not specify anything for the `self` argument; you skip it
entirely, and Python automatically adds the instance reference for you.
I am aware that this is confusing at first; it's not really
inconsistent, but it may appear inconsistent because it relies on a
distinction (between bound and unbound methods) that you don't know
about yet.

Whew. I realize that's a lot to absorb, but you'll get the hang of it.
All Python classes work the same way, so once you learn one, you've
learned them all. If you forget everything else, remember this one
thing, because I promise it will trip you up:


![Note](../images/note.png) 
`__init__` methods are optional, but when you define one, you must remember to explicitly call the ancestor's `__init__` method (if it defines one). This is more generally true: whenever a descendant wants to extend the behavior of the ancestor, the descendant method must explicitly call the ancestor method at the proper time, with the proper arguments. 

### Further Reading on Python Classes

-   [*Learning to
    Program*](http://www.freenetpages.co.uk/hp/alan.gauld/ "Python book for first-time programmers")
    has a gentler [introduction to
    classes](http://www.freenetpages.co.uk/hp/alan.gauld/tutclass.htm).
-   [*How to Think Like a Computer
    Scientist*](http://www.ibiblio.org/obp/thinkCSpy/ "Python book for computer science majors")
    shows how to [use classes to model compound
    datatypes](http://www.ibiblio.org/obp/thinkCSpy/chap12.htm).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    has an in-depth look at [classes, namespaces, and
    inheritance](http://www.python.org/doc/current/tut/node11.html).
-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    answers [common questions about
    classes](http://www.faqts.com/knowledge-base/index.phtml/fid/242).

  

