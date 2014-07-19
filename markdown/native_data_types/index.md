

Chapter 3. Native Datatypes
---------------------------

-   [3.1. Introducing Dictionaries](index.html#odbchelper.dict)
    -   [3.1.1. Defining Dictionaries](index.html#d0e5174)
    -   [3.1.2. Modifying Dictionaries](index.html#d0e5269)
    -   [3.1.3. Deleting Items From Dictionaries](index.html#d0e5450)
-   [3.2. Introducing Lists](lists.html)
    -   [3.2.1. Defining Lists](lists.html#d0e5623)
    -   [3.2.2. Adding Elements to Lists](lists.html#d0e5887)
    -   [3.2.3. Searching Lists](lists.html#d0e6115)
    -   [3.2.4. Deleting List Elements](lists.html#d0e6277)
    -   [3.2.5. Using List Operators](lists.html#d0e6392)
-   [3.3. Introducing Tuples](tuples.html)
-   [3.4. Declaring variables](declaring_variables.html)
    -   [3.4.1. Referencing Variables](declaring_variables.html#d0e6873)
    -   [3.4.2. Assigning Multiple Values at
        Once](declaring_variables.html#odbchelper.multiassign)
-   [3.5. Formatting Strings](formatting_strings.html)
-   [3.6. Mapping Lists](mapping_lists.html)
-   [3.7. Joining Lists and Splitting Strings](joining_lists.html)
    -   [3.7.1. Historical Note on String
        Methods](joining_lists.html#d0e7982)
-   [3.8. Summary](summary.html)

3.1. Introducing Dictionaries
-----------------------------

-   [3.1.1. Defining Dictionaries](index.html#d0e5174)
-   [3.1.2. Modifying Dictionaries](index.html#d0e5269)
-   [3.1.3. Deleting Items From Dictionaries](index.html#d0e5450)

One of Python's built-in datatypes is the dictionary, which defines
one-to-one relationships between keys and values.


![Note](../images/note.png) 
A dictionary in Python is like a hash in Perl. In Perl, variables that store hashes always start with a `%` character. In Python, variables can be named anything, and Python keeps track of the datatype internally. 


![Note](../images/note.png) 
A dictionary in Python is like an instance of the `Hashtable` class in Java. 


![Note](../images/note.png) 
A dictionary in Python is like an instance of the `Scripting.Dictionary` object in Visual Basic. 

### 3.1.1. Defining Dictionaries

### Example 3.1. Defining a Dictionary

    >>> d = {"server":"mpilgrim", "database":"master"} 
    >>> d
    {'server': 'mpilgrim', 'database': 'master'}
    >>> d["server"]                                    
    'mpilgrim'
    >>> d["database"]                                  
    'master'
    >>> d["mpilgrim"]                                  
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    KeyError: mpilgrim



[![1](../images/callouts/1.png)](#odbchelper.dict.1.1) First, you create a new dictionary with two elements and assign it to the variable `d`. Each element is a key-value pair, and the whole set of elements is enclosed in curly braces. 

[![2](../images/callouts/2.png)](#odbchelper.dict.1.2) `'server'` is a key, and its associated value, referenced by `d["server"]`, is `'mpilgrim'`. 

[![3](../images/callouts/3.png)](#odbchelper.dict.1.3) `'database'` is a key, and its associated value, referenced by `d["database"]`, is `'master'`. 

[![4](../images/callouts/4.png)](#odbchelper.dict.1.4) You can get values by key, but you can't get keys by value. So `d["server"]` is `'mpilgrim'`, but `d["mpilgrim"]` raises an exception, because `'mpilgrim'` is not a key. 

### 3.1.2. Modifying Dictionaries

### Example 3.2. Modifying a Dictionary

    >>> d
    {'server': 'mpilgrim', 'database': 'master'}
    >>> d["database"] = "pubs" 
    >>> d
    {'server': 'mpilgrim', 'database': 'pubs'}
    >>> d["uid"] = "sa"        
    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'pubs'}



[![1](../images/callouts/1.png)](#odbchelper.dict.2.1) You can not have duplicate keys in a dictionary. Assigning a value to an existing key will wipe out the old value. 

[![2](../images/callouts/2.png)](#odbchelper.dict.2.2) You can add new key-value pairs at any time. This syntax is identical to modifying existing values. (Yes, this will annoy you someday when you think you are adding new values but are actually just modifying the same value over and over because your key isn't changing the way you think it is.) 

Note that the new element (key `'uid'`, value `'sa'`) appears to be in
the middle. In fact, it was just a coincidence that the elements
appeared to be in order in the first example; it is just as much a
coincidence that they appear to be out of order now.


![Note](../images/note.png) 
Dictionaries have no concept of order among elements. It is incorrect to say that the elements are “out of order”; they are simply unordered. This is an important distinction that will annoy you when you want to access the elements of a dictionary in a specific, repeatable order (like alphabetical order by key). There are ways of doing this, but they're not built into the dictionary. 

When working with dictionaries, you need to be aware that dictionary
keys are case-sensitive.

### Example 3.3. Dictionary Keys Are Case-Sensitive

    >>> d = {}
    >>> d["key"] = "value"
    >>> d["key"] = "other value" 
    >>> d
    {'key': 'other value'}
    >>> d["Key"] = "third value" 
    >>> d
    {'Key': 'third value', 'key': 'other value'}



[![1](../images/callouts/1.png)](#odbchelper.dict.5.1) Assigning a value to an existing dictionary key simply replaces the old value with a new one. 

[![2](../images/callouts/2.png)](#odbchelper.dict.5.2) This is not assigning a value to an existing dictionary key, because strings in Python are case-sensitive, so `'key'` is not the same as `'Key'`. This creates a new key/value pair in the dictionary; it may look similar to you, but as far as Python is concerned, it's completely different. 

### Example 3.4. Mixing Datatypes in a Dictionary

    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'pubs'}
    >>> d["retrycount"] = 3 
    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'master', 'retrycount': 3}
    >>> d[42] = "douglas"   
    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'master',
    42: 'douglas', 'retrycount': 3}



[![1](../images/callouts/1.png)](#odbchelper.dict.3.1) Dictionaries aren't just for strings. Dictionary values can be any datatype, including strings, integers, objects, or even other dictionaries. And within a single dictionary, the values don't all need to be the same type; you can mix and match as needed. 

[![2](../images/callouts/2.png)](#odbchelper.dict.3.2) Dictionary keys are more restricted, but they can be strings, integers, and a few other types. You can also mix and match key datatypes within a dictionary. 

### 3.1.3. Deleting Items From Dictionaries

### Example 3.5. Deleting Items from a Dictionary

    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'master',
    42: 'douglas', 'retrycount': 3}
    >>> del d[42] 
    >>> d
    {'server': 'mpilgrim', 'uid': 'sa', 'database': 'master', 'retrycount': 3}
    >>> d.clear() 
    >>> d
    {}



[![1](../images/callouts/1.png)](#odbchelper.dict.4.1) `del` lets you delete individual items from a dictionary by key. 

[![2](../images/callouts/2.png)](#odbchelper.dict.4.2) `clear` deletes all items from a dictionary. Note that the set of empty curly braces signifies a dictionary without any items. 

### Further Reading on Dictionaries

-   [*How to Think Like a Computer
    Scientist*](http://www.ibiblio.org/obp/thinkCSpy/ "Python book for computer science majors")
    teaches about dictionaries and shows how to [use dictionaries to
    model sparse
    matrices](http://www.ibiblio.org/obp/thinkCSpy/chap10.htm).
-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/) has
    a lot of [example code using
    dictionaries](http://www.faqts.com/knowledge-base/index.phtml/fid/541).
-   [Python
    Cookbook](http://www.activestate.com/ASPN/Python/Cookbook/ "growing archive of annotated code samples")
    discusses [how to sort the values of a dictionary by
    key](http://www.activestate.com/ASPN/Python/Cookbook/Recipe/52306).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the dictionary
    methods](http://www.python.org/doc/current/lib/typesmapping.html).

  

