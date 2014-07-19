

3.6. Mapping Lists
------------------

One of the most powerful features of Python is the list comprehension,
which provides a compact way of mapping a list into another list by
applying a function to each of the elements of the list.

### Example 3.24. Introducing List Comprehensions

    >>> li = [1, 9, 8, 4]
    >>> [elem*2 for elem in li]      
    [2, 18, 16, 8]
    >>> li                           
    [1, 9, 8, 4]
    >>> li = [elem*2 for elem in li] 
    >>> li
    [2, 18, 16, 8]



[![1](../images/callouts/1.png)](#odbchelper.map.1.1) To make sense of this, look at it from right to left. `li` is the list you're mapping. Python loops through `li` one element at a time, temporarily assigning the value of each element to the variable `elem`. Python then applies the function `elem`\*2 and appends that result to the returned list. 

[![2](../images/callouts/2.png)](#odbchelper.map.1.2) Note that list comprehensions do not change the original list. 

[![3](../images/callouts/3.png)](#odbchelper.map.1.3) It is safe to assign the result of a list comprehension to the variable that you're mapping. Python constructs the new list in memory, and when the list comprehension is complete, it assigns the result to the variable. 

Here are the list comprehensions in the `buildConnectionString` function
that you declared in [Chapter 2](../getting_to_know_python/index.html):

    ["%s=%s" % (k, v) for k, v in params.items()]

First, notice that you're calling the `items` function of the `params`
dictionary. This function returns a list of tuples of all the data in
the dictionary.

### Example 3.25. The `keys`, `values`, and `items` Functions

    >>> params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
    >>> params.keys()   
    ['server', 'uid', 'database', 'pwd']
    >>> params.values() 
    ['mpilgrim', 'sa', 'master', 'secret']
    >>> params.items()  
    [('server', 'mpilgrim'), ('uid', 'sa'), ('database', 'master'), ('pwd', 'secret')]



[![1](../images/callouts/1.png)](#odbchelper.map.2.1) The `keys` method of a dictionary returns a list of all the keys. The list is not in the order in which the dictionary was defined (remember that elements in a dictionary are unordered), but it is a list. 

[![2](../images/callouts/2.png)](#odbchelper.map.2.2) The `values` method returns a list of all the values. The list is in the same order as the list returned by `keys`, so `params.values()[n] == params[params.keys()[n]]` for all values of `n`. 

[![3](../images/callouts/3.png)](#odbchelper.map.2.3) The `items` method returns a list of tuples of the form `(key, value)`. The list contains all the data in the dictionary. 

Now let's see what `buildConnectionString` does. It takes a list,
`params`.`items`(), and maps it to a new list by applying string
formatting to each element. The new list will have the same number of
elements as `params`.`items`(), but each element in the new list will be
a string that contains both a key and its associated value from the
`params` dictionary.

### Example 3.26. List Comprehensions in `buildConnectionString`, Step by Step

    >>> params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
    >>> params.items()
    [('server', 'mpilgrim'), ('uid', 'sa'), ('database', 'master'), ('pwd', 'secret')]
    >>> [k for k, v in params.items()]                
    ['server', 'uid', 'database', 'pwd']
    >>> [v for k, v in params.items()]                
    ['mpilgrim', 'sa', 'master', 'secret']
    >>> ["%s=%s" % (k, v) for k, v in params.items()] 
    ['server=mpilgrim', 'uid=sa', 'database=master', 'pwd=secret']



[![1](../images/callouts/1.png)](#odbchelper.map.3.1) Note that you're using two variables to iterate through the `params.items()` list. This is another use of [multi-variable assignment](declaring_variables.html#odbchelper.multiassign "3.4.2. Assigning Multiple Values at Once"). The first element of `params.items()` is `('server', 'mpilgrim')`, so in the first iteration of the list comprehension, `k` will get `'server'` and `v` will get `'mpilgrim'`. In this case, you're ignoring the value of `v` and only including the value of `k` in the returned list, so this list comprehension ends up being equivalent to `params`.`keys`(). 

[![2](../images/callouts/2.png)](#odbchelper.map.3.2) Here you're doing the same thing, but ignoring the value of `k`, so this list comprehension ends up being equivalent to `params`.`values`(). 

[![3](../images/callouts/3.png)](#odbchelper.map.3.3) Combining the previous two examples with some simple [string formatting](formatting_strings.html "3.5. Formatting Strings"), you get a list of strings that include both the key and value of each element of the dictionary. This looks suspiciously like the [output](../getting_to_know_python/index.html#odbchelper.output) of the program. All that remains is to join the elements in this list into a single string. 

### Further Reading on List Comprehensions

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses another way to map lists [using the built-in `map`
    function](http://www.python.org/doc/current/tut/node7.html#SECTION007130000000000000000).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    shows how to [do nested list
    comprehensions](http://www.python.org/doc/current/tut/node7.html#SECTION007140000000000000000).

  

