
3.2. Introducing Lists
----------------------

-   [3.2.1. Defining Lists](lists.html#d0e5623)
-   [3.2.2. Adding Elements to Lists](lists.html#d0e5887)
-   [3.2.3. Searching Lists](lists.html#d0e6115)
-   [3.2.4. Deleting List Elements](lists.html#d0e6277)
-   [3.2.5. Using List Operators](lists.html#d0e6392)

Lists are Python's workhorse datatype. If your only experience with
lists is arrays in Visual Basic or (God forbid) the datastore in
Powerbuilder, brace yourself for Python lists.


![Note](../images/note.png) 
A list in Python is like an array in Perl. In Perl, variables that store arrays always start with the `@` character; in Python, variables can be named anything, and Python keeps track of the datatype internally. 


![Note](../images/note.png) 
A list in Python is much more than an array in Java (although it can be used as one if that's really all you want out of life). A better analogy would be to the `ArrayList` class, which can hold arbitrary objects and can expand dynamically as new items are added. 

### 3.2.1. Defining Lists

### Example 3.6. Defining a List

    >>> li = ["a", "b", "mpilgrim", "z", "example"] 
    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example']
    >>> li[0]                                       
    'a'
    >>> li[4]                                       
    'example'



[![1](../images/callouts/1.png)](#odbchelper.list.1.1) First, you define a list of five elements. Note that they retain their original order. This is not an accident. A list is an ordered set of elements enclosed in square brackets. 

[![2](../images/callouts/2.png)](#odbchelper.list.1.2) A list can be used like a zero-based array. The first element of any non-empty list is always `li[0]`. 

[![3](../images/callouts/3.png)](#odbchelper.list.1.3) The last element of this five-element list is `li[4]`, because lists are always zero-based. 

### Example 3.7. Negative List Indices

    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example']
    >>> li[-1] 
    'example'
    >>> li[-3] 
    'mpilgrim'



[![1](../images/callouts/1.png)](#odbchelper.list.2.1) A negative index accesses elements from the end of the list counting backwards. The last element of any non-empty list is always `li[-1]`. 

[![2](../images/callouts/2.png)](#odbchelper.list.2.2) If the negative index is confusing to you, think of it this way: `li[-n] == li[len(li) - n]`. So in this list, `li[-3] == li[5 - 3] == li[2]`. 

### Example 3.8. Slicing a List

    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example']
    >>> li[1:3]  
    ['b', 'mpilgrim']
    >>> li[1:-1] 
    ['b', 'mpilgrim', 'z']
    >>> li[0:3]  
    ['a', 'b', 'mpilgrim']



[![1](../images/callouts/1.png)](#odbchelper.list.3.1) You can get a subset of a list, called a “slice”, by specifying two indices. The return value is a new list containing all the elements of the list, in order, starting with the first slice index (in this case `li[1]`), up to but not including the second slice index (in this case `li[3]`). 

[![2](../images/callouts/2.png)](#odbchelper.list.3.2) Slicing works if one or both of the slice indices is negative. If it helps, you can think of it this way: reading the list from left to right, the first slice index specifies the first element you want, and the second slice index specifies the first element you don't want. The return value is everything in between. 

[![3](../images/callouts/3.png)](#odbchelper.list.3.3) Lists are zero-based, so `li[0:3]` returns the first three elements of the list, starting at `li[0]`, up to but not including `li[3]`. 

### Example 3.9. Slicing Shorthand

    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example']
    >>> li[:3] 
    ['a', 'b', 'mpilgrim']
    >>> li[3:]  
    ['z', 'example']
    >>> li[:]  
    ['a', 'b', 'mpilgrim', 'z', 'example']



[![1](../images/callouts/1.png)](#odbchelper.list.4.1) If the left slice index is 0, you can leave it out, and 0 is implied. So `li[:3]` is the same as `li[0:3]` from [Example 3.8, “Slicing a List”](lists.html#odbchelper.list.slice "Example 3.8. Slicing a List"). 

[![2](../images/callouts/2.png)](#odbchelper.list.4.2) Similarly, if the right slice index is the length of the list, you can leave it out. So `li[3:]` is the same as `li[3:5]`, because this list has five elements. 

[![3](../images/callouts/3.png)](#odbchelper.list.4.3) Note the symmetry here. In this five-element list, `li[:3]` returns the first 3 elements, and `li[3:]` returns the last two elements. In fact, `li[:n]` will always return the first `n` elements, and `li[n:]` will return the rest, regardless of the length of the list. 

[![4](../images/callouts/4.png)](#odbchelper.list.4.4) If both slice indices are left out, all elements of the list are included. But this is not the same as the original `li` list; it is a new list that happens to have all the same elements. `li[:]` is shorthand for making a complete copy of a list. 

### 3.2.2. Adding Elements to Lists

### Example 3.10. Adding Elements to a List

    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example']
    >>> li.append("new")               
    >>> li
    ['a', 'b', 'mpilgrim', 'z', 'example', 'new']
    >>> li.insert(2, "new")            
    >>> li
    ['a', 'b', 'new', 'mpilgrim', 'z', 'example', 'new']
    >>> li.extend(["two", "elements"]) 
    >>> li
    ['a', 'b', 'new', 'mpilgrim', 'z', 'example', 'new', 'two', 'elements']



[![1](../images/callouts/1.png)](#odbchelper.list.5.1) `append` adds a single element to the end of the list. 

[![2](../images/callouts/2.png)](#odbchelper.list.5.2) `insert` inserts a single element into a list. The numeric argument is the index of the first element that gets bumped out of position. Note that list elements do not need to be unique; there are now two separate elements with the value `'new'`, `li[2]` and `li[6]`. 

[![3](../images/callouts/3.png)](#odbchelper.list.5.3) `extend` concatenates lists. Note that you do not call `extend` with multiple arguments; you call it with one argument, a list. In this case, that list has two elements. 

### Example 3.11. The Difference between `extend` and `append`

    >>> li = ['a', 'b', 'c']
    >>> li.extend(['d', 'e', 'f']) 
    >>> li
    ['a', 'b', 'c', 'd', 'e', 'f']
    >>> len(li)                    
    6
    >>> li[-1]
    'f'
    >>> li = ['a', 'b', 'c']
    >>> li.append(['d', 'e', 'f']) 
    >>> li
    ['a', 'b', 'c', ['d', 'e', 'f']]
    >>> len(li)                    
    4
    >>> li[-1]
    ['d', 'e', 'f']



[![1](../images/callouts/1.png)](#odbchelper.list.5.4) Lists have two methods, `extend` and `append`, that look like they do the same thing, but are in fact completely different. `extend` takes a single argument, which is always a list, and adds each of the elements of that list to the original list. 

[![2](../images/callouts/2.png)](#odbchelper.list.5.5) Here you started with a list of three elements (`'a'`, `'b'`, and `'c'`), and you extended the list with a list of another three elements (`'d'`, `'e'`, and `'f'`), so you now have a list of six elements. 

[![3](../images/callouts/3.png)](#odbchelper.list.5.6) On the other hand, `append` takes one argument, which can be any data type, and simply adds it to the end of the list. Here, you're calling the `append` method with a single argument, which is a list of three elements. 

[![4](../images/callouts/4.png)](#odbchelper.list.5.7) Now the original list, which started as a list of three elements, contains four elements. Why four? Because the last element that you just appended *is itself a list*. Lists can contain any type of data, including other lists. That may be what you want, or maybe not. Don't use `append` if you mean `extend`. 

### 3.2.3. Searching Lists

### Example 3.12. Searching a List

    >>> li
    ['a', 'b', 'new', 'mpilgrim', 'z', 'example', 'new', 'two', 'elements']
    >>> li.index("example") 
    5
    >>> li.index("new")     
    2
    >>> li.index("c")       
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    ValueError: list.index(x): x not in list
    >>> "c" in li           
    False



[![1](../images/callouts/1.png)](#odbchelper.list.6.1) `index` finds the first occurrence of a value in the list and returns the index. 

[![2](../images/callouts/2.png)](#odbchelper.list.6.2) `index` finds the *first* occurrence of a value in the list. In this case, `'new'` occurs twice in the list, in `li[2]` and `li[6]`, but `index` will return only the first index, `2`. 

[![3](../images/callouts/3.png)](#odbchelper.list.6.3) If the value is not found in the list, Python raises an exception. This is notably different from most languages, which will return some invalid index. While this may seem annoying, it is a good thing, because it means your program will crash at the source of the problem, rather than later on when you try to use the invalid index. 

[![4](../images/callouts/4.png)](#odbchelper.list.6.4) To test whether a value is in the list, use `in`, which returns `True` if the value is found or `False` if it is not. 

<table>
<col width="100%" />
<tbody>
<tr class="odd">
<td align="left"><img src="../images/note.png" alt="Note" /></td>
</tr>
<tr class="even">
<td align="left">Before version 2.2.1, Python had no separate boolean datatype. To compensate for this, Python accepted almost anything in a boolean context (like an <code class="literal">if</code> statement), according to the following rules:
<ul>
<li><code class="constant">0</code> is false; all other numbers are true.</li>
<li>An empty string (<code class="literal">&quot;&quot;</code>) is false, all other strings are true.</li>
<li>An empty list (<code class="literal">[]</code>) is false; all other lists are true.</li>
<li>An empty tuple (<code class="literal">()</code>) is false; all other tuples are true.</li>
<li>An empty dictionary (<code class="literal">{}</code>) is false; all other dictionaries are true.</li>
</ul>
These rules still apply in Python 2.2.1 and beyond, but now you can also use an actual boolean, which has a value of <code class="literal">True</code> or <code class="literal">False</code>. Note the capitalization; these values, like everything else in Python, are case-sensitive.</td>
</tr>
</tbody>
</table>

### 3.2.4. Deleting List Elements

### Example 3.13. Removing Elements from a List

    >>> li
    ['a', 'b', 'new', 'mpilgrim', 'z', 'example', 'new', 'two', 'elements']
    >>> li.remove("z")   
    >>> li
    ['a', 'b', 'new', 'mpilgrim', 'example', 'new', 'two', 'elements']
    >>> li.remove("new") 
    >>> li
    ['a', 'b', 'mpilgrim', 'example', 'new', 'two', 'elements']
    >>> li.remove("c")   
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    ValueError: list.remove(x): x not in list
    >>> li.pop()         
    'elements'
    >>> li
    ['a', 'b', 'mpilgrim', 'example', 'new', 'two']



[![1](../images/callouts/1.png)](#odbchelper.list.7.1) `remove` removes the first occurrence of a value from a list. 

[![2](../images/callouts/2.png)](#odbchelper.list.7.2) `remove` removes *only* the first occurrence of a value. In this case, `'new'` appeared twice in the list, but `li.remove("new")` removed only the first occurrence. 

[![3](../images/callouts/3.png)](#odbchelper.list.7.3) If the value is not found in the list, Python raises an exception. This mirrors the behavior of the `index` method. 

[![4](../images/callouts/4.png)](#odbchelper.list.7.4) `pop` is an interesting beast. It does two things: it removes the last element of the list, and it returns the value that it removed. Note that this is different from `li[-1]`, which returns a value but does not change the list, and different from `li.remove(value)`, which changes the list but does not return a value. 

### 3.2.5. Using List Operators

### Example 3.14. List Operators

    >>> li = ['a', 'b', 'mpilgrim']
    >>> li = li + ['example', 'new'] 
    >>> li
    ['a', 'b', 'mpilgrim', 'example', 'new']
    >>> li += ['two']                
    >>> li
    ['a', 'b', 'mpilgrim', 'example', 'new', 'two']
    >>> li = [1, 2] * 3              
    >>> li
    [1, 2, 1, 2, 1, 2]



[![1](../images/callouts/1.png)](#odbchelper.list.8.1) Lists can also be concatenated with the `+` operator. `list = list + otherlist` has the same result as `list.extend(otherlist)`. But the `+` operator returns a new (concatenated) list as a value, whereas `extend` only alters an existing list. This means that `extend` is faster, especially for large lists. 

[![2](../images/callouts/2.png)](#odbchelper.list.8.2) Python supports the `+=` operator. `li += ['two']` is equivalent to `li.extend(['two'])`. The `+=` operator works for lists, strings, and integers, and it can be overloaded to work for user-defined classes as well. (More on classes in [Chapter 5](../object_oriented_framework/index.html).) 

[![3](../images/callouts/3.png)](#odbchelper.list.8.3) The `*` operator works on lists as a repeater. `li = [1, 2] * 3` is equivalent to `li = [1, 2] + [1, 2] + [1, 2]`, which concatenates the three lists into one. 

### Further Reading on Lists

-   [*How to Think Like a Computer
    Scientist*](http://www.ibiblio.org/obp/thinkCSpy/ "Python book for computer science majors")
    teaches about lists and makes an important point about [passing
    lists as function
    arguments](http://www.ibiblio.org/obp/thinkCSpy/chap08.htm).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    shows how to [use lists as stacks and
    queues](http://www.python.org/doc/current/tut/node7.html#SECTION007110000000000000000).
-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    answers [common questions about
    lists](http://www.faqts.com/knowledge-base/index.phtml/fid/534) and
    has a lot of [example code using
    lists](http://www.faqts.com/knowledge-base/index.phtml/fid/540).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the list
    methods](http://www.python.org/doc/current/lib/typesseq-mutable.html).

  

