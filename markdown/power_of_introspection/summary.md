

4.9. Summary
------------

The `apihelper.py` program and its output should now make perfect sense.

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

Here is the output of `apihelper.py`:

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

Before diving into the next chapter, make sure you're comfortable doing
all of these things:

-   Defining and calling functions with [optional and named
    arguments](optional_arguments.html "4.2. Using Optional and Named Arguments")
-   Using
    [`str`](built_in_functions.html#apihelper.str.intro "Example 4.6. Introducing str")
    to coerce any arbitrary value into a string representation
-   Using
    [`getattr`](getattr.html "4.4. Getting Object References With getattr")
    to get references to functions and other attributes dynamically
-   Extending the list comprehension syntax to do [list
    filtering](filtering_lists.html "4.5. Filtering Lists")
-   Recognizing [the `and-or`
    trick](and_or.html "4.6. The Peculiar Nature of and and or") and
    using it safely
-   Defining [`lambda`
    functions](lambda_functions.html "4.7. Using lambda Functions")
-   [Assigning functions to
    variables](lambda_functions.html#apihelper.funcassign) and calling
    the function by referencing the variable. I can't emphasize this
    enough, because this mode of thought is vital to advancing your
    understanding of Python. You'll see more complex applications of
    this concept throughout this book.

  

