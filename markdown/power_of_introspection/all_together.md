

4.8. Putting It All Together
----------------------------

The last line of code, the only one you haven't deconstructed yet, is
the one that does all the work. But by now the work is easy, because
everything you need is already set up just the way you need it. All the
dominoes are in place; it's time to knock them down.

This is the meat of `apihelper.py`:

        print "\n".join(["%s %s" %
                          (method.ljust(spacing),
                           processFunc(str(getattr(object, method).__doc__)))
                         for method in methodList])

Note that this is one command, split over multiple lines, but it doesn't
use the line continuation character (`\`). Remember when I said that
[some expressions can be split into multiple
lines](../native_data_types/declaring_variables.html#tip.implicitmultiline)
without using a backslash? A list comprehension is one of those
expressions, since the entire expression is contained in square
brackets.

Now, let's take it from the end and work backwards. The

    for method in methodList

shows that this is a [list
comprehension](../native_data_types/mapping_lists.html "3.6. Mapping Lists").
As you know, `methodList` is a list of [all the methods you care
about](filtering_lists.html#apihelper.filter.care) in `object`. So
you're looping through that list with `method`.

### Example 4.22. Getting a `doc string` Dynamically

    >>> import odbchelper
    >>> object = odbchelper                   
    >>> method = 'buildConnectionString'      
    >>> getattr(object, method)               
    <function buildConnectionString at 010D6D74>
    >>> print getattr(object, method).__doc__ 
    Build a connection string from a dictionary of parameters.

        Returns string.



[![1](../images/callouts/1.png)](#apihelper.alltogether.1.1) In the `info` function, `object` is the object you're getting help on, passed in as an argument. 

[![2](../images/callouts/2.png)](#apihelper.alltogether.1.2) As you're looping through `methodList`, `method` is the name of the current method. 

[![3](../images/callouts/3.png)](#apihelper.alltogether.1.3) Using the [`getattr`](getattr.html "4.4. Getting Object References With getattr") function, you're getting a reference to the *`method`* function in the *`object`* module. 

[![4](../images/callouts/4.png)](#apihelper.alltogether.1.4) Now, printing the actual `doc string` of the method is easy. 

The next piece of the puzzle is the use of `str` around the
`doc string`. As you may recall, `str` is a built-in function that
[coerces data into a
string](built_in_functions.html "4.3. Using type, str, dir, and Other Built-In Functions").
But a `doc string` is always a string, so why bother with the `str`
function? The answer is that not every function has a `doc string`, and
if it doesn't, its `__doc__` attribute is `None`.

### Example 4.23. Why Use `str` on a `doc string`?

    >>> >>> def foo(): print 2
    >>> >>> foo()
    2
    >>> >>> foo.__doc__     
    >>> foo.__doc__ == None 
    True
    >>> str(foo.__doc__)    
    'None'



[![1](../images/callouts/1.png)](#apihelper.alltogether.2.1) You can easily define a function that has no `doc string`, so its `__doc__` attribute is `None`. Confusingly, if you evaluate the `__doc__` attribute directly, the Python IDE prints nothing at all, which makes sense if you think about it, but is still unhelpful. 

[![2](../images/callouts/2.png)](#apihelper.alltogether.2.2) You can verify that the value of the `__doc__` attribute is actually `None` by comparing it directly. 

[![3](../images/callouts/3.png)](#apihelper.alltogether.2.3) The `str` function takes the null value and returns a string representation of it, `'None'`. 


![Note](../images/note.png) 
In SQL, you must use `IS NULL` instead of `= NULL` to compare a null value. In Python, you can use either `== None` or `is None`, but `is None` is faster. 

Now that you are guaranteed to have a string, you can pass the string to
`processFunc`, which you have [already
defined](lambda_functions.html "4.7. Using lambda Functions") as a
function that either does or doesn't collapse whitespace. Now you see
why it was important to use `str` to convert a `None` value into a
string representation. `processFunc` is assuming a string argument and
calling its `split` method, which would crash if you passed it `None`
because `None` doesn't have a `split` method.

Stepping back even further, you see that you're using string formatting
again to concatenate the return value of `processFunc` with the return
value of `method`'s `ljust` method. This is a new string method that you
haven't seen before.

### Example 4.24. Introducing `ljust`

    >>> s = 'buildConnectionString'
    >>> s.ljust(30) 
    'buildConnectionString         '
    >>> s.ljust(20) 
    'buildConnectionString'



[![1](../images/callouts/1.png)](#apihelper.alltogether.3.1) `ljust` pads the string with spaces to the given length. This is what the `info` function uses to make two columns of output and line up all the `doc string`s in the second column. 

[![2](../images/callouts/2.png)](#apihelper.alltogether.3.2) If the given length is smaller than the length of the string, `ljust` will simply return the string unchanged. It never truncates the string. 

You're almost finished. Given the padded method name from the `ljust`
method and the (possibly collapsed) `doc string` from the call to
`processFunc`, you concatenate the two and get a single string. Since
you're mapping `methodList`, you end up with a list of strings. Using
the `join` method of the string `"\n"`, you join this list into a single
string, with each element of the list on a separate line, and print the
result.

### Example 4.25. Printing a List

    >>> li = ['a', 'b', 'c']
    >>> print "\n".join(li) 
    a
    b
    c



[![1](../images/callouts/1.png)](#apihelper.alltogether.4.1) This is also a useful debugging trick when you're working with lists. And in Python, you're always working with lists. 

That's the last piece of the puzzle. You should now understand this
code.

        print "\n".join(["%s %s" %
                          (method.ljust(spacing),
                           processFunc(str(getattr(object, method).__doc__)))
                         for method in methodList])

  

