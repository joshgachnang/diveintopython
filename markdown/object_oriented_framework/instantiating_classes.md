

5.4. Instantiating Classes
--------------------------

-   [5.4.1. Garbage Collection](instantiating_classes.html#d0e12165)

Instantiating classes in Python is straightforward. To instantiate a
class, simply call the class as if it were a function, passing the
arguments that the `__init__` method defines. The return value will be
the newly created object.

### Example 5.7. Creating a `FileInfo` Instance

    >>> import fileinfo
    >>> f = fileinfo.FileInfo("/music/_singles/kairo.mp3") 
    >>> f.__class__                                        
    <class fileinfo.FileInfo at 010EC204>
    >>> f.__doc__                                          
    'store file metadata'
    >>> f                                                  
    {'name': '/music/_singles/kairo.mp3'}



[![1](../images/callouts/1.png)](#fileinfo.create.1.1) You are creating an instance of the `FileInfo` class (defined in the `fileinfo` module) and assigning the newly created instance to the variable `f`. You are passing one parameter, `/music/_singles/kairo.mp3`, which will end up as the `filename` argument in `FileInfo`'s `__init__` method. 

[![2](../images/callouts/2.png)](#fileinfo.create.1.2) Every class instance has a built-in attribute, `__class__`, which is the object's class. (Note that the representation of this includes the physical address of the instance on my machine; your representation will be different.) Java programmers may be familiar with the `Class` class, which contains methods like `getName` and `getSuperclass` to get metadata information about an object. In Python, this kind of metadata is available directly on the object itself through attributes like `__class__`, `__name__`, and `__bases__`. 

[![3](../images/callouts/3.png)](#fileinfo.create.1.3) You can access the instance's `doc string` just as with a function or a module. All instances of a class share the same `doc string`. 

[![4](../images/callouts/4.png)](#fileinfo.create.1.4) Remember when the `__init__` method [assigned its `filename` argument to `self["name"]`](defining_classes.html#fileinfo.class.example "Example 5.4. Defining the FileInfo Class")? Well, here's the result. The arguments you pass when you create the class instance get sent right along to the `__init__` method (along with the object reference, `self`, which Python adds for free). 


![Note](../images/note.png) 
In Python, simply call a class as if it were a function to create a new instance of the class. There is no explicit `new` operator like C++ or Java. 

### 5.4.1. Garbage Collection

If creating new instances is easy, destroying them is even easier. In
general, there is no need to explicitly free instances, because they are
freed automatically when the variables assigned to them go out of scope.
Memory leaks are rare in Python.

### Example 5.8. Trying to Implement a Memory Leak

    >>> def leakmem():
    ...     f = fileinfo.FileInfo('/music/_singles/kairo.mp3') 
    ...     
    >>> for i in range(100):
    ...     leakmem()                                          



[![1](../images/callouts/1.png)](#fileinfo.create.2.1) Every time the `leakmem` function is called, you are creating an instance of `FileInfo` and assigning it to the variable `f`, which is a local variable within the function. Then the function ends without ever freeing `f`, so you would expect a memory leak, but you would be wrong. When the function ends, the local variable `f` goes out of scope. At this point, there are no longer any references to the newly created instance of `FileInfo` (since you never assigned it to anything other than `f`), so Python destroys the instance for us. 

[![2](../images/callouts/2.png)](#fileinfo.create.2.3) No matter how many times you call the `leakmem` function, it will never leak memory, because every time, Python will destroy the newly created `FileInfo` class before returning from `leakmem`. 

The technical term for this form of garbage collection is “reference
counting”. Python keeps a list of references to every instance created.
In the above example, there was only one reference to the `FileInfo`
instance: the local variable `f`. When the function ends, the variable
`f` goes out of scope, so the reference count drops to `0`, and Python
destroys the instance automatically.

In previous versions of Python, there were situations where reference
counting failed, and Python couldn't clean up after you. If you created
two instances that referenced each other (for instance, a doubly-linked
list, where each node has a pointer to the previous and next node in the
list), neither instance would ever be destroyed automatically because
Python (correctly) believed that there is always a reference to each
instance. Python 2.0 has an additional form of garbage collection called
“mark-and-sweep” which is smart enough to notice this virtual gridlock
and clean up circular references correctly.

As a former philosophy major, it disturbs me to think that things
disappear when no one is looking at them, but that's exactly what
happens in Python. In general, you can simply forget about memory
management and let Python clean up after you.

### Further Reading on Garbage Collection

-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [built-in attributes like
    `__class__`](http://www.python.org/doc/current/lib/specialattrs.html).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the [`gc`
    module](http://www.python.org/doc/current/lib/module-gc.html), which
    gives you low-level control over Python's garbage collection.

  

