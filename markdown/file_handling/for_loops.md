

6.3. Iterating with `for` Loops
-------------------------------

Like most other languages, Python has `for` loops. The only reason you
haven't seen them until now is that Python is good at so many other
things that you don't need them as often.

Most other languages don't have a powerful list datatype like Python, so
you end up doing a lot of manual work, specifying a start, end, and step
to define a range of integers or characters or other iteratable
entities. But in Python, a `for` loop simply iterates over a list, the
same way [list
comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists")
work.

### Example 6.8. Introducing the `for` Loop

    >>> li = ['a', 'b', 'e']
    >>> for s in li:         
    ...     print s          
    a
    b
    e
    >>> print "\n".join(li)  
    a
    b
    e



[![1](../images/callouts/1.png)](#fileinfo.for.1.1) The syntax for a `for` loop is similar to [list comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists"). `li` is a list, and `s` will take the value of each element in turn, starting from the first element. 

[![2](../images/callouts/2.png)](#fileinfo.for.1.2) Like an `if` statement or any other [indented block](../getting_to_know_python/indenting_code.html "2.5. Indenting Code"), a `for` loop can have any number of lines of code in it. 

[![3](../images/callouts/3.png)](#fileinfo.for.1.3) This is the reason you haven't seen the `for` loop yet: you haven't needed it yet. It's amazing how often you use `for` loops in other languages when all you really want is a `join` or a list comprehension. 

Doing a “normal” (by Visual Basic standards) counter `for` loop is also
simple.

### Example 6.9. Simple Counters

    >>> for i in range(5):             
    ...     print i
    0
    1
    2
    3
    4
    >>> li = ['a', 'b', 'c', 'd', 'e']
    >>> for i in range(len(li)):       
    ...     print li[i]
    a
    b
    c
    d
    e



[![1](../images/callouts/1.png)](#fileinfo.for.3.1) As you saw in [Example 3.20, “Assigning Consecutive Values”](../native_data_types/declaring_variables.html#odbchelper.multiassign.range "Example 3.20. Assigning Consecutive Values"), `range` produces a list of integers, which you then loop through. I know it looks a bit odd, but it is occasionally (and I stress *occasionally*) useful to have a counter loop. 

[![2](../images/callouts/2.png)](#fileinfo.for.3.2) Don't ever do this. This is Visual Basic-style thinking. Break out of it. Just iterate through the list, as shown in the previous example. 

`for` loops are not just for simple counters. They can iterate through
all kinds of things. Here is an example of using a `for` loop to iterate
through a dictionary.

### Example 6.10. Iterating Through a Dictionary

    >>> import os
    >>> for k, v in os.environ.items():       
    ...     print "%s=%s" % (k, v)
    USERPROFILE=C:\Documents and Settings\mpilgrim
    OS=Windows_NT
    COMPUTERNAME=MPILGRIM
    USERNAME=mpilgrim

    [...snip...]
    >>> print "\n".join(["%s=%s" % (k, v)
    ...     for k, v in os.environ.items()]) 
    USERPROFILE=C:\Documents and Settings\mpilgrim
    OS=Windows_NT
    COMPUTERNAME=MPILGRIM
    USERNAME=mpilgrim

    [...snip...]



[![1](../images/callouts/1.png)](#fileinfo.for.2.1) `os.environ` is a dictionary of the environment variables defined on your system. In Windows, these are your user and system variables accessible from MS-DOS. In UNIX, they are the variables exported in your shell's startup scripts. In Mac OS, there is no concept of environment variables, so this dictionary is empty. 

[![2](../images/callouts/2.png)](#fileinfo.for.2.2) `os.environ.items()` returns a list of tuples: `[(key1, value1), (key2, value2), ...]`. The `for` loop iterates through this list. The first round, it assigns `key1` to `k` and `value1` to `v`, so `k` = `USERPROFILE` and `v` = `C:\Documents and Settings\mpilgrim`. In the second round, `k` gets the second key, `OS`, and `v` gets the corresponding value, `Windows_NT`. 

[![3](../images/callouts/3.png)](#fileinfo.for.2.3) With [multi-variable assignment](../native_data_types/declaring_variables.html#odbchelper.multiassign "3.4.2. Assigning Multiple Values at Once") and [list comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists"), you can replace the entire `for` loop with a single statement. Whether you actually do this in real code is a matter of personal coding style. I like it because it makes it clear that what I'm doing is mapping a dictionary into a list, then joining the list into a single string. Other programmers prefer to write this out as a `for` loop. The output is the same in either case, although this version is slightly faster, because there is only one `print` statement instead of many. 

Now we can look at the `for` loop in `MP3FileInfo`, from the sample
`fileinfo.py` program introduced in [Chapter
5](../object_oriented_framework/index.html).

### Example 6.11. `for` Loop in `MP3FileInfo`

        tagDataMap = {"title"   : (  3,  33, stripnulls),
                      "artist"  : ( 33,  63, stripnulls),
                      "album"   : ( 63,  93, stripnulls),
                      "year"    : ( 93,  97, stripnulls),
                      "comment" : ( 97, 126, stripnulls),
                      "genre"   : (127, 128, ord)}                               
        .
        .
        .
                if tagdata[:3] == "TAG":
                    for tag, (start, end, parseFunc) in self.tagDataMap.items(): 
                        self[tag] = parseFunc(tagdata[start:end])                



[![1](../images/callouts/1.png)](#fileinfo.multiassign.5.1) `tagDataMap` is a [class attribute](../object_oriented_framework/class_attributes.html "5.8. Introducing Class Attributes") that defines the tags you're looking for in an MP3 file. Tags are stored in fixed-length fields. Once you read the last 128 bytes of the file, bytes 3 through 32 of those are always the song title, 33 through 62 are always the artist name, 63 through 92 are the album name, and so forth. Note that `tagDataMap` is a dictionary of tuples, and each tuple contains two integers and a function reference. 

[![2](../images/callouts/2.png)](#fileinfo.multiassign.5.2) This looks complicated, but it's not. The structure of the `for` variables matches the structure of the elements of the list returned by `items`. Remember that `items` returns a list of tuples of the form `(key, value)`. The first element of that list is `("title", (3, 33, <function stripnulls>))`, so the first time around the loop, `tag` gets `"title"`, `start` gets `3`, `end` gets `33`, and `parseFunc` gets the function `stripnulls`. 

[![3](../images/callouts/3.png)](#fileinfo.multiassign.5.3) Now that you've extracted all the parameters for a single MP3 tag, saving the tag data is easy. You [slice](../native_data_types/lists.html#odbchelper.list.slice "Example 3.8. Slicing a List") `tagdata` from `start` to `end` to get the actual data for this tag, call `parseFunc` to post-process the data, and assign this as the value for the key `tag` in the pseudo-dictionary `self`. After iterating through all the elements in `tagDataMap`, `self` has the values for all the tags, and [you know what that looks like](../object_oriented_framework/special_class_methods.html#fileinfo.specialmethods.setname "Example 5.15. Setting an MP3FileInfo's name"). 

  

