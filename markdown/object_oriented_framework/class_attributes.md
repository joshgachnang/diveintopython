

5.8. Introducing Class Attributes
---------------------------------

You already know about [data
attributes](userdict.html#fileinfo.userdict.init.example "Example 5.9. Defining the UserDict Class"),
which are variables owned by a specific instance of a class. Python also
supports class attributes, which are variables owned by the class
itself.

### Example 5.17. Introducing Class Attributes

    class MP3FileInfo(FileInfo):
        "store ID3v1.0 MP3 tags"
        tagDataMap = {"title"   : (  3,  33, stripnulls),
                      "artist"  : ( 33,  63, stripnulls),
                      "album"   : ( 63,  93, stripnulls),
                      "year"    : ( 93,  97, stripnulls),
                      "comment" : ( 97, 126, stripnulls),
                      "genre"   : (127, 128, ord)}

    >>> import fileinfo
    >>> fileinfo.MP3FileInfo            
    <class fileinfo.MP3FileInfo at 01257FDC>
    >>> fileinfo.MP3FileInfo.tagDataMap 
    {'title': (3, 33, <function stripnulls at 0260C8D4>), 
    'genre': (127, 128, <built-in function ord>), 
    'artist': (33, 63, <function stripnulls at 0260C8D4>), 
    'year': (93, 97, <function stripnulls at 0260C8D4>), 
    'comment': (97, 126, <function stripnulls at 0260C8D4>), 
    'album': (63, 93, <function stripnulls at 0260C8D4>)}
    >>> m = fileinfo.MP3FileInfo()      
    >>> m.tagDataMap
    {'title': (3, 33, <function stripnulls at 0260C8D4>), 
    'genre': (127, 128, <built-in function ord>), 
    'artist': (33, 63, <function stripnulls at 0260C8D4>), 
    'year': (93, 97, <function stripnulls at 0260C8D4>), 
    'comment': (97, 126, <function stripnulls at 0260C8D4>), 
    'album': (63, 93, <function stripnulls at 0260C8D4>)}



[![1](../images/callouts/1.png)](#fileinfo.classattributes.1.1) `MP3FileInfo` is the class itself, not any particular instance of the class. 

[![2](../images/callouts/2.png)](#fileinfo.classattributes.1.2) `tagDataMap` is a class attribute: literally, an attribute of the class. It is available before creating any instances of the class. 

[![3](../images/callouts/3.png)](#fileinfo.classattributes.1.3) Class attributes are available both through direct reference to the class and through any instance of the class. 


![Note](../images/note.png) 
In Java, both static variables (called class attributes in Python) and instance variables (called data attributes in Python) are defined immediately after the class definition (one with the `static` keyword, one without). In Python, only class attributes can be defined here; data attributes are defined in the `__init__` method. 

Class attributes can be used as class-level constants (which is how you
use them in `MP3FileInfo`), but they are not really constants. You can
also change them.


![Note](../images/note.png) 
There are no constants in Python. Everything can be changed if you try hard enough. This fits with one of the core principles of Python: bad behavior should be discouraged but not banned. If you really want to change the value of `None`, you can do it, but don't come running to me when your code is impossible to debug. 

### Example 5.18. Modifying Class Attributes

    >>> class counter:
    ...     count = 0                     
    ...     def __init__(self):
    ...         self.__class__.count += 1 
    ...     
    >>> counter
    <class __main__.counter at 010EAECC>
    >>> counter.count                     
    0
    >>> c = counter()
    >>> c.count                           
    1
    >>> counter.count
    1
    >>> d = counter()                     
    >>> d.count
    2
    >>> c.count
    2
    >>> counter.count
    2



[![1](../images/callouts/1.png)](#fileinfo.classattributes.2.1) `count` is a class attribute of the `counter` class. 

[![2](../images/callouts/2.png)](#fileinfo.classattributes.2.2) `__class__` is a built-in attribute of every class instance (of every class). It is a reference to the class that `self` is an instance of (in this case, the `counter` class). 

[![3](../images/callouts/3.png)](#fileinfo.classattributes.2.3) Because `count` is a class attribute, it is available through direct reference to the class, before you have created any instances of the class. 

[![4](../images/callouts/4.png)](#fileinfo.classattributes.2.4) Creating an instance of the class calls the `__init__` method, which increments the class attribute `count` by `1`. This affects the class itself, not just the newly created instance. 

[![5](../images/callouts/5.png)](#fileinfo.classattributes.2.5) Creating a second instance will increment the class attribute `count` again. Notice how the class attribute is shared by the class and all instances of the class. 

  

