

4.5. Filtering Lists
--------------------

As you know, Python has powerful capabilities for mapping lists into
other lists, via list comprehensions ([Section 3.6, “Mapping
Lists”](../native_data_types/mapping_lists.html "3.6. Mapping Lists")).
This can be combined with a filtering mechanism, where some elements in
the list are mapped while others are skipped entirely.

Here is the list filtering syntax:

    [mapping-expression for element in source-list if filter-expression]

This is an extension of the [list
comprehensions](../native_data_types/mapping_lists.html "3.6. Mapping Lists")
that you know and love. The first two thirds are the same; the last
part, starting with the `if`, is the filter expression. A filter
expression can be any expression that evaluates true or false (which in
Python can be [almost
anything](../native_data_types/lists.html#tip.boolean)). Any element for
which the filter expression evaluates true will be included in the
mapping. All other elements are ignored, so they are never put through
the mapping expression and are not included in the output list.

### Example 4.14. Introducing List Filtering

    >>> li = ["a", "mpilgrim", "foo", "b", "c", "b", "d", "d"]
    >>> [elem for elem in li if len(elem) > 1]       
    ['mpilgrim', 'foo']
    >>> [elem for elem in li if elem != "b"]         
    ['a', 'mpilgrim', 'foo', 'c', 'd', 'd']
    >>> [elem for elem in li if li.count(elem) == 1] 
    ['a', 'mpilgrim', 'foo', 'c']



[![1](../images/callouts/1.png)](#apihelper.filter.1.1) The mapping expression here is simple (it just returns the value of each element), so concentrate on the filter expression. As Python loops through the list, it runs each element through the filter expression. If the filter expression is true, the element is mapped and the result of the mapping expression is included in the returned list. Here, you are filtering out all the one-character strings, so you're left with a list of all the longer strings. 

[![2](../images/callouts/2.png)](#apihelper.filter.1.2) Here, you are filtering out a specific value, `b`. Note that this filters all occurrences of `b`, since each time it comes up, the filter expression will be false. 

[![3](../images/callouts/3.png)](#apihelper.filter.1.3) `count` is a list method that returns the number of times a value occurs in a list. You might think that this filter would eliminate duplicates from a list, returning a list containing only one copy of each value in the original list. But it doesn't, because values that appear twice in the original list (in this case, `b` and `d`) are excluded completely. There are ways of eliminating duplicates from a list, but filtering is not the solution. 

Let's get back to this line from `apihelper.py`:

        methodList = [method for method in dir(object) if callable(getattr(object, method))]

This looks complicated, and it is complicated, but the basic structure
is the same. The whole filter expression returns a list, which is
assigned to the `methodList` variable. The first half of the expression
is the list mapping part. The mapping expression is an identity
expression, which it returns the value of each element. `dir`(`object`)
returns a list of `object`'s attributes and methods -- that's the list
you're mapping. So the only new part is the filter expression after the
`if`.

The filter expression looks scary, but it's not. You already know about
[`callable`](built_in_functions.html#apihelper.builtin.callable "Example 4.8. Introducing callable"),
[`getattr`](getattr.html#apihelper.getattr.intro "Example 4.10. Introducing getattr"),
and
[`in`](../native_data_types/tuples.html#odbchelper.tuplemethods "Example 3.16. Tuples Have No Methods").
As you saw in the [previous
section](getattr.html "4.4. Getting Object References With getattr"),
the expression `getattr(object, method)` returns a function object if
`object` is a module and `method` is the name of a function in that
module.

So this expression takes an object (named `object`). Then it gets a list
of the names of the object's attributes, methods, functions, and a few
other things. Then it filters that list to weed out all the stuff that
you don't care about. You do the weeding out by taking the name of each
attribute/method/function and getting a reference to the real thing, via
the `getattr` function. Then you check to see if that object is
callable, which will be any methods and functions, both built-in (like
the `pop` method of a list) and user-defined (like the
`buildConnectionString` function of the `odbchelper` module). You don't
care about other attributes, like the `__name__` attribute that's built
in to every module.

### Further Reading on Filtering Lists

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses another way to filter lists [using the built-in `filter`
    function](http://www.python.org/doc/current/tut/node7.html#SECTION007130000000000000000).

  

