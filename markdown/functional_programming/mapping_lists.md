

16.4. Mapping lists revisited
-----------------------------

You're already familiar with using [list
comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists")
to map one list into another. There is another way to accomplish the
same thing, using the built-in `map` function. It works much the same
way as the
[`filter`](filtering_lists.html "16.3. Filtering lists revisited")
function.

### Example 16.10. Introducing `map`

    >>> def double(n):
    ...     return n*2
    ...     
    >>> li = [1, 2, 3, 5, 9, 10, 256, -3]
    >>> map(double, li)                       
    [2, 4, 6, 10, 18, 20, 512, -6]
    >>> [double(n) for n in li]               
    [2, 4, 6, 10, 18, 20, 512, -6]
    >>> newlist =
    >>> for n in li:                          
    ...     newlist.append(double(n))
    ...     
    >>> newlist
    [2, 4, 6, 10, 18, 20, 512, -6]



[![1](../images/callouts/1.png)](#regression.map.1.1) `map` takes a function and a list<sup>[[8](#ftn.d0e36079)]</sup> and returns a new list by calling the function with each element of the list in order. In this case, the function simply multiplies each element by 2. 

[![2](../images/callouts/2.png)](#regression.map.1.2) You could accomplish the same thing with a list comprehension. List comprehensions were first introduced in Python 2.0; `map` has been around forever. 

[![3](../images/callouts/3.png)](#regression.map.1.3) You could, if you insist on thinking like a Visual Basic programmer, use a `for` loop to accomplish the same thing. 

### Example 16.11. `map` with lists of mixed datatypes

    >>> li = [5, 'a', (2, 'b')]
    >>> map(double, li)                       
    [10, 'aa', (2, 'b', 2, 'b')]



[![1](../images/callouts/1.png)](#regression.map.2.1) As a side note, I'd like to point out that `map` works just as well with lists of mixed datatypes, as long as the function you're using correctly handles each type. In this case, the `double` function simply multiplies the given argument by 2, and Python Does The Right Thing depending on the datatype of the argument. For integers, this means actually multiplying it by 2; for strings, it means concatenating the string with itself; for tuples, it means making a new tuple that has all of the elements of the original, then all of the elements of the original again. 

All right, enough play time. Let's look at some real code.

### Example 16.12. `map` in `regression.py`

        filenameToModuleName = lambda f: os.path.splitext(f)[0] 
        moduleNames = map(filenameToModuleName, files)          



[![1](../images/callouts/1.png)](#regression.map.3.1) As you saw in [Section 4.7, “Using lambda Functions”](../power_of_introspection/lambda_functions.html "4.7. Using lambda Functions"), `lambda` defines an inline function. And as you saw in [Example 6.17, “Splitting Pathnames”](../file_handling/os_module.html#splittingpathnames.example "Example 6.17. Splitting Pathnames"), `os.path.splitext` takes a filename and returns a tuple `(name, extension)`. So `filenameToModuleName` is a function which will take a filename and strip off the file extension, and return just the name. 

[![2](../images/callouts/2.png)](#regression.map.3.2) Calling `map` takes each filename listed in `files`, passes it to the function `filenameToModuleName`, and returns a list of the return values of each of those function calls. In other words, you strip the file extension off of each filename, and store the list of all those stripped filenames in `moduleNames`. 

As you'll see in the rest of the chapter, you can extend this type of
data-centric thinking all the way to the final goal, which is to define
and execute a single test suite that contains the tests from all of
those individual test suites.

### Footnotes

<sup>[[8](#d0e36079)]</sup>Again, I should point out that `map` can take
a list, a tuple, or any object that acts like a sequence. See previous
footnote about `filter`.

  

