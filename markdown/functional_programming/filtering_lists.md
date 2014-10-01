

16.3. Filtering lists revisited
-------------------------------

You're already familiar with [using list comprehensions to filter
lists](../power_of_introspection/filtering_lists.html "4.5. Filtering Lists").
There is another way to accomplish this same thing, which some people
feel is more expressive.

Python has a built-in `filter` function which takes two arguments, a
function and a list, and returns a list.<sup>[[7](#ftn.d0e35697)]</sup>
The function passed as the first argument to `filter` must itself take
one argument, and the list that `filter` returns will contain all the
elements from the list passed to `filter` for which the function passed
to `filter` returns true.

Got all that? It's not as difficult as it sounds.

### Example 16.7. Introducing `filter`

    >>> [def odd(n):](http://test.com)              
    ...     return n % 2
    ...     
    >>> li = [1, 2, 3, 5, 9, 10, 256, -3]
    >>> filter(odd, li)             
    [1, 3, 5, 9, -3]
    >>> [e for e in li if odd(e)]   
    >>> filteredList =
    >>> for n in li:                
    ...     if odd(n):
    ...         filteredList.append(n)
    ...     
    >>> filteredList
    [1, 3, 5, 9, -3]



[![1](../images/callouts/1.png)](#regression.filter.1.1) `odd` uses the built-in mod function “`%`” to return `True` if `n` is odd and `False` if `n` is even. 

[![2](../images/callouts/2.png)](#regression.filter.1.2) `filter` takes two arguments, a function (`odd`) and a list (`li`). It loops through the list and calls `odd` with each element. If `odd` returns a true value (remember, any non-zero value is true in Python), then the element is included in the returned list, otherwise it is filtered out. The result is a list of only the odd numbers from the original list, in the same order as they appeared in the original. 

[![3](../images/callouts/3.png)](#regression.filter.1.3) You could accomplish the same thing using list comprehensions, as you saw in [Section 4.5, “Filtering Lists”](../power_of_introspection/filtering_lists.html "4.5. Filtering Lists"). 

[![4](../images/callouts/4.png)](#regression.filter.1.4) You could also accomplish the same thing with a `for` loop. Depending on your programming background, this may seem more “straightforward”, but functions like `filter` are much more expressive. Not only is it easier to write, it's easier to read, too. Reading the `for` loop is like standing too close to a painting; you see all the details, but it may take a few seconds to be able to step back and see the bigger picture: “Oh, you're just filtering the list!” 

### Example 16.8. `filter` in `regression.py`

        files = os.listdir(path)                                
        test = re.compile("test\.py$", re.IGNORECASE)           
        files = filter(test.search, files)                      



[![1](../images/callouts/1.png)](#regression.filter.2.1) As you saw in [Section 16.2, “Finding the path”](finding_the_path.html "16.2. Finding the path"), `path` may contain the full or partial pathname of the directory of the currently running script, or it may contain an empty string if the script is being run from the current directory. Either way, `files` will end up with the names of the files in the same directory as this script you're running. 

[![2](../images/callouts/2.png)](#regression.filter.2.2) This is a compiled regular expression. As you saw in [Section 15.3, “Refactoring”](../refactoring/refactoring.html "15.3. Refactoring"), if you're going to use the same regular expression over and over, you should compile it for faster performance. The compiled object has a `search` method which takes a single argument, the string to search. If the regular expression matches the string, the `search` method returns a `Match` object containing information about the regular expression match; otherwise it returns `None`, the Python null value. 

[![3](../images/callouts/3.png)](#regression.filter.2.3) For each element in the `files` list, you're going to call the `search` method of the compiled regular expression object, `test`. If the regular expression matches, the method will return a `Match` object, which Python considers to be true, so the element will be included in the list returned by `filter`. If the regular expression does not match, the `search` method will return `None`, which Python considers to be false, so the element will not be included. 

**Historical note. **Versions of Python prior to 2.0 did not have [list
comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists"),
so you couldn't [filter using list
comprehensions](../power_of_introspection/filtering_lists.html "4.5. Filtering Lists");
the `filter` function was the only game in town. Even with the
introduction of list comprehensions in 2.0, some people still prefer the
old-style `filter` (and its companion function, `map`, which you'll see
later in this chapter). Both techniques work at the moment, so which one
you use is a matter of style. There is discussion that `map` and
`filter` might be deprecated in a future version of Python, but no
decision has been made.

### Example 16.9. Filtering using list comprehensions instead

        files = os.listdir(path)                               
        test = re.compile("test\.py$", re.IGNORECASE)          
        files = [f for f in files if test.search(f)] 



[![1](../images/callouts/1.png)](#regression.filter.3.1) This will accomplish exactly the same result as using the `filter` function. Which way is more expressive? That's up to you. 

### Footnotes

<sup>[[7](#d0e35697)]</sup>Technically, the second argument to `filter`
can be any sequence, including lists, tuples, and custom classes that
act like lists by defining the `__getitem__` special method. If
possible, `filter` will return the same datatype as you give it, so
filtering a list returns a list, but filtering a tuple returns a tuple.

  

