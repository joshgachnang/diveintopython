

5.6. Special Class Methods
--------------------------

-   [5.6.1. Getting and Setting
    Items](special_class_methods.html#d0e12822)

In addition to normal class methods, there are a number of special
methods that Python classes can define. Instead of being called directly
by your code (like normal methods), special methods are called for you
by Python in particular circumstances or when specific syntax is used.

As you saw in the [previous
section](userdict.html "5.5. Exploring UserDict: A Wrapper Class"),
normal methods go a long way towards wrapping a dictionary in a class.
But normal methods alone are not enough, because there are a lot of
things you can do with dictionaries besides call methods on them. For
starters, you can
[get](../native_data_types/index.html#odbchelper.dict.define "Example 3.1. Defining a Dictionary")
and
[set](../native_data_types/index.html#odbchelper.dict.modify "Example 3.2. Modifying a Dictionary")
items with a syntax that doesn't include explicitly invoking methods.
This is where special class methods come in: they provide a way to map
non-method-calling syntax into method calls.

### 5.6.1. Getting and Setting Items

### Example 5.12. The `__getitem__` Special Method

        def __getitem__(self, key): return self.data[key]

    >>> f = fileinfo.FileInfo("/music/_singles/kairo.mp3")
    >>> f
    {'name':'/music/_singles/kairo.mp3'}
    >>> f.__getitem__("name") 
    '/music/_singles/kairo.mp3'
    >>> f["name"]             
    '/music/_singles/kairo.mp3'



[![1](../images/callouts/1.png)](#fileinfo.specialmethods.1.1) The `__getitem__` special method looks simple enough. Like the normal methods `clear`, `keys`, and `values`, it just redirects to the dictionary to return its value. But how does it get called? Well, you can call `__getitem__` directly, but in practice you wouldn't actually do that; I'm just doing it here to show you how it works. The right way to use `__getitem__` is to get Python to call it for you. 

[![2](../images/callouts/2.png)](#fileinfo.specialmethods.1.2) This looks just like the syntax you would use to [get a dictionary value](../native_data_types/index.html#odbchelper.dict.define "Example 3.1. Defining a Dictionary"), and in fact it returns the value you would expect. But here's the missing link: under the covers, Python has converted this syntax to the method call `f.__getitem__("name")`. That's why `__getitem__` is a special class method; not only can you call it yourself, you can get Python to call it for you by using the right syntax. 

Of course, Python has a `__setitem__` special method to go along with
`__getitem__`, as shown in the next example.

### Example 5.13. The `__setitem__` Special Method

        def __setitem__(self, key, item): self.data[key] = item

    >>> f
    {'name':'/music/_singles/kairo.mp3'}
    >>> f.__setitem__("genre", 31) 
    >>> f
    {'name':'/music/_singles/kairo.mp3', 'genre':31}
    >>> f["genre"] = 32            
    >>> f
    {'name':'/music/_singles/kairo.mp3', 'genre':32}



[![1](../images/callouts/1.png)](#fileinfo.specialmethods.2.1) Like the `__getitem__` method, `__setitem__` simply redirects to the real dictionary `self.data` to do its work. And like `__getitem__`, you wouldn't ordinarily call it directly like this; Python calls `__setitem__` for you when you use the right syntax. 

[![2](../images/callouts/2.png)](#fileinfo.specialmethods.2.2) This looks like regular dictionary syntax, except of course that `f` is really a class that's trying very hard to masquerade as a dictionary, and `__setitem__` is an essential part of that masquerade. This line of code actually calls `f.__setitem__("genre", 32)` under the covers. 

`__setitem__` is a special class method because it gets called for you,
but it's still a class method. Just as easily as the `__setitem__`
method was defined in `UserDict`, you can redefine it in the descendant
class to override the ancestor method. This allows you to define classes
that act like dictionaries in some ways but define their own behavior
above and beyond the built-in dictionary.

This concept is the basis of the entire framework you're studying in
this chapter. Each file type can have a handler class that knows how to
get metadata from a particular type of file. Once some attributes (like
the file's name and location) are known, the handler class knows how to
derive other attributes automatically. This is done by overriding the
`__setitem__` method, checking for particular keys, and adding
additional processing when they are found.

For example, `MP3FileInfo` is a descendant of `FileInfo`. When an
`MP3FileInfo`'s `name` is set, it doesn't just set the `name` key (like
the ancestor `FileInfo` does); it also looks in the file itself for MP3
tags and populates a whole set of keys. The next example shows how this
works.

### Example 5.14. Overriding `__setitem__` in `MP3FileInfo`

        def __setitem__(self, key, item):         
            if key == "name" and item:            
                self.__parse(item)                
            FileInfo.__setitem__(self, key, item) 



[![1](../images/callouts/1.png)](#fileinfo.specialmethods.3.1) Notice that this `__setitem__` method is defined exactly the same way as the ancestor method. This is important, since Python will be calling the method for you, and it expects it to be defined with a certain number of arguments. (Technically speaking, the names of the arguments don't matter; only the number of arguments is important.) 

[![2](../images/callouts/2.png)](#fileinfo.specialmethods.3.2) Here's the crux of the entire `MP3FileInfo` class: if you're assigning a value to the `name` key, you want to do something extra. 

[![3](../images/callouts/3.png)](#fileinfo.specialmethods.3.3) The extra processing you do for `name`s is encapsulated in the `__parse` method. This is another class method defined in `MP3FileInfo`, and when you call it, you qualify it with `self`. Just calling `__parse` would look for a normal function defined outside the class, which is not what you want. Calling `self.__parse` will look for a class method defined within the class. This isn't anything new; you reference [data attributes](userdict.html#fileinfo.userdict.normalmethods "Example 5.10. UserDict Normal Methods") the same way. 

[![4](../images/callouts/4.png)](#fileinfo.specialmethods.3.4) After doing this extra processing, you want to call the ancestor method. Remember that this is never done for you in Python; you must do it manually. Note that you're calling the immediate ancestor, `FileInfo`, even though it doesn't have a `__setitem__` method. That's okay, because Python will walk up the ancestor tree until it finds a class with the method you're calling, so this line of code will eventually find and call the `__setitem__` defined in `UserDict`. 


![Note](../images/note.png) 
When accessing data attributes within a class, you need to qualify the attribute name: `self.attribute`. When calling other methods within a class, you need to qualify the method name: `self.method`. 

### Example 5.15. Setting an `MP3FileInfo`'s `name`

    >>> import fileinfo
    >>> mp3file = fileinfo.MP3FileInfo()                   
    >>> mp3file
    {'name':None}
    >>> mp3file["name"] = "/music/_singles/kairo.mp3"      
    >>> mp3file
    {'album': 'Rave Mix', 'artist': '***DJ MARY-JANE***', 'genre': 31,
    'title': 'KAIRO****THE BEST GOA', 'name': '/music/_singles/kairo.mp3',
    'year': '2000', 'comment': 'http://mp3.com/DJMARYJANE'}
    >>> mp3file["name"] = "/music/_singles/sidewinder.mp3" 
    >>> mp3file
    {'album': '', 'artist': 'The Cynic Project', 'genre': 18, 'title': 'Sidewinder', 
    'name': '/music/_singles/sidewinder.mp3', 'year': '2000', 
    'comment': 'http://mp3.com/cynicproject'}



[![1](../images/callouts/1.png)](#fileinfo.specialmethods.4.1) First, you create an instance of `MP3FileInfo`, without passing it a filename. (You can get away with this because the `filename` argument of the `__init__` method is [optional](../power_of_introspection/optional_arguments.html "4.2. Using Optional and Named Arguments").) Since `MP3FileInfo` has no `__init__` method of its own, Python walks up the ancestor tree and finds the `__init__` method of `FileInfo`. This `__init__` method manually calls the `__init__` method of `UserDict` and then sets the `name` key to `filename`, which is `None`, since you didn't pass a filename. Thus, `mp3file` initially looks like a dictionary with one key, `name`, whose value is `None`. 

[![2](../images/callouts/2.png)](#fileinfo.specialmethods.4.2) Now the real fun begins. Setting the `name` key of `mp3file` triggers the `__setitem__` method on `MP3FileInfo` (not `UserDict`), which notices that you're setting the `name` key with a real value and calls `self.__parse`. Although you haven't traced through the `__parse` method yet, you can see from the output that it sets several other keys: `album`, `artist`, `genre`, `title`, `year`, and `comment`. 

[![3](../images/callouts/3.png)](#fileinfo.specialmethods.4.3) Modifying the `name` key will go through the same process again: Python calls `__setitem__`, which calls `self.__parse`, which sets all the other keys. 

  

