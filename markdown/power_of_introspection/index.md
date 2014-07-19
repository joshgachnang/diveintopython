

Chapter 4. The Power Of Introspection
-------------------------------------

-   [4.1. Diving In](index.html#apihelper.divein)
-   [4.2. Using Optional and Named Arguments](optional_arguments.html)
-   [4.3. Using type, str, dir, and Other Built-In
    Functions](built_in_functions.html)
    -   [4.3.1. The type Function](built_in_functions.html#d0e8510)
    -   [4.3.2. The str Function](built_in_functions.html#d0e8609)
    -   [4.3.3. Built-In Functions](built_in_functions.html#d0e8958)
-   [4.4. Getting Object References With getattr](getattr.html)
    -   [4.4.1. getattr with Modules](getattr.html#d0e9194)
    -   [4.4.2. getattr As a Dispatcher](getattr.html#d0e9362)
-   [4.5. Filtering Lists](filtering_lists.html)
-   [4.6. The Peculiar Nature of and and or](and_or.html)
    -   [4.6.1. Using the and-or Trick](and_or.html#d0e9975)
-   [4.7. Using lambda Functions](lambda_functions.html)
    -   [4.7.1. Real-World lambda
        Functions](lambda_functions.html#d0e10403)
-   [4.8. Putting It All Together](all_together.html)
-   [4.9. Summary](summary.html)

This chapter covers one of Python's strengths: introspection. As you
know, [everything in Python is an
object](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object"),
and introspection is code looking at other modules and functions in
memory as objects, getting information about them, and manipulating
them. Along the way, you'll define functions with no name, call
functions with arguments out of order, and reference functions whose
names you don't even know ahead of time.

4.1. Diving In
--------------

Here is a complete, working Python program. You should understand a good
deal about it just by looking at it. The numbered lines illustrate
concepts covered in [Chapter 2, *Your First Python
Program*](../getting_to_know_python/index.html "Chapter 2. Your First Python Program").
Don't worry if the rest of the code looks intimidating; you'll learn all
about it throughout this chapter.

### Example 4.1. `apihelper.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    def info(object, spacing=10, collapse=1):   
        """Print methods and doc strings.
        
        Takes module, class, list, dictionary, or string."""
        methodList = [method for method in dir(object) if callable(getattr(object, method))]
        processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
        print "\n".join(["%s %s" %
                          (method.ljust(spacing),
                           processFunc(str(getattr(object, method).__doc__)))
                         for method in methodList])

    if __name__ == "__main__":                 
        print info.__doc__



[![1](../images/callouts/1.png)](#apihelper.intro.1.1) This module has one function, `info`. According to its [function declaration](../getting_to_know_python/declaring_functions.html "2.2. Declaring Functions"), it takes three parameters: `object`, `spacing`, and `collapse`. The last two are actually optional parameters, as you'll see shortly. 

[![2](../images/callouts/2.png)](#apihelper.intro.1.2) The `info` function has a multi-line [`doc string`](../getting_to_know_python/documenting_functions.html "2.3. Documenting Functions") that succinctly describes the function's purpose. Note that no return value is mentioned; this function will be used solely for its effects, rather than its value. 

[![3](../images/callouts/3.png)](#apihelper.intro.1.3) Code within the function is [indented](../getting_to_know_python/indenting_code.html "2.5. Indenting Code"). 

[![4](../images/callouts/4.png)](#apihelper.intro.1.4) The `if __name__` [trick](../getting_to_know_python/testing_modules.html#odbchelper.ifnametrick) allows this program do something useful when run by itself, without interfering with its use as a module for other programs. In this case, the program simply prints out the `doc string` of the `info` function. 

[![5](../images/callouts/5.png)](#apihelper.intro.1.5) [`if` statements](../getting_to_know_python/testing_modules.html#odbchelper.ifnametrick) use `==` for comparison, and parentheses are not required. 

The `info` function is designed to be used by you, the programmer, while
working in the Python IDE. It takes any object that has functions or
methods (like a module, which has functions, or a list, which has
methods) and prints out the functions and their `doc string`s.

### Example 4.2. Sample Usage of `apihelper.py`

    >>> from apihelper import info
    >>> li =
    >>> info(li)
    append     L.append(object) -- append object to end
    count      L.count(value) -> integer -- return number of occurrences of value
    extend     L.extend(list) -- extend list by appending list elements
    index      L.index(value) -> integer -- return index of first occurrence of value
    insert     L.insert(index, object) -- insert object before index
    pop        L.pop([index]) -> item -- remove and return item at index (default last)
    remove     L.remove(value) -- remove first occurrence of value
    reverse    L.reverse() -- reverse *IN PLACE*
    sort       L.sort([cmpfunc]) -- sort *IN PLACE*; if given, cmpfunc(x, y) -> -1, 0, 1

By default the output is formatted to be easy to read. Multi-line
`doc string`s are collapsed into a single long line, but this option can
be changed by specifying `0` for the *`collapse`* argument. If the
function names are longer than 10 characters, you can specify a larger
value for the *`spacing`* argument to make the output easier to read.

### Example 4.3. Advanced Usage of `apihelper.py`

    >>> import odbchelper
    >>> info(odbchelper)
    buildConnectionString Build a connection string from a dictionary Returns string.
    >>> info(odbchelper, 30)
    buildConnectionString          Build a connection string from a dictionary Returns string.
    >>> info(odbchelper, 30, 0)
    buildConnectionString          Build a connection string from a dictionary
        
        Returns string.

  

