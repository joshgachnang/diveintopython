

4.7. Using `lambda` Functions
-----------------------------

-   [4.7.1. Real-World lambda Functions](lambda_functions.html#d0e10403)

Python supports an interesting syntax that lets you define one-line
mini-functions on the fly. Borrowed from Lisp, these so-called `lambda`
functions can be used anywhere a function is required.

### Example 4.20. Introducing `lambda` Functions

    >>> def f(x):
    ...     return x*2
    ...     
    >>> f(3)
    6
    >>> g = lambda x: x*2  
    >>> g(3)
    6
    >>> (lambda x: x*2)(3) 
    6



[![1](../images/callouts/1.png)](#apihelper.lambda.1.2) This is a `lambda` function that accomplishes the same thing as the normal function above it. Note the abbreviated syntax here: there are no parentheses around the argument list, and the `return` keyword is missing (it is implied, since the entire function can only be one expression). Also, the function has no name, but it can be called through the variable it is assigned to. 

[![2](../images/callouts/2.png)](#apihelper.lambda.1.3) You can use a `lambda` function without even assigning it to a variable. This may not be the most useful thing in the world, but it just goes to show that a lambda is just an in-line function. 

To generalize, a `lambda` function is a function that takes any number
of arguments (including [optional
arguments](optional_arguments.html "4.2. Using Optional and Named Arguments"))
and returns the value of a single expression. `lambda` functions can not
contain commands, and they can not contain more than one expression.
Don't try to squeeze too much into a `lambda` function; if you need
something more complex, define a normal function instead and make it as
long as you want.


![Note](../images/note.png) 
`lambda` functions are a matter of style. Using them is never required; anywhere you could use them, you could define a separate normal function and use that instead. I use them in places where I want to encapsulate specific, non-reusable code without littering my code with a lot of little one-line functions. 

### 4.7.1. Real-World `lambda` Functions

Here are the `lambda` functions in `apihelper.py`:

        processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)

Notice that this uses the simple form of the
[`and-or`](and_or.html "4.6. The Peculiar Nature of and and or") trick,
which is okay, because a `lambda` function is always true [in a boolean
context](../native_data_types/lists.html#tip.boolean). (That doesn't
mean that a `lambda` function can't return a false value. The function
is always true; its return value could be anything.)

Also notice that you're using the `split` function with no arguments.
You've already seen it used with [one or two
arguments](../native_data_types/joining_lists.html#odbchelper.split.example "Example 3.28. Splitting a String"),
but without any arguments it splits on whitespace.

### Example 4.21. `split` With No Arguments

    >>> s = "this   is\na\ttest"  
    >>> print s
    this   is
    a   test
    >>> print s.split()           
    ['this', 'is', 'a', 'test']
    >>> print " ".join(s.split()) 
    'this is a test'



[![1](../images/callouts/1.png)](#apihelper.split.1.1) This is a multiline string, defined by escape characters instead of [triple quotes](../getting_to_know_python/documenting_functions.html#odbchelper.triplequotes "Example 2.2. Defining the buildConnectionString Function's doc string"). `\n` is a carriage return, and `\t` is a tab character. 

[![2](../images/callouts/2.png)](#apihelper.split.1.2) `split` without any arguments splits on whitespace. So three spaces, a carriage return, and a tab character are all the same. 

[![3](../images/callouts/3.png)](#apihelper.split.1.3) You can normalize whitespace by splitting a string with `split` and then rejoining it with `join`, using a single space as a delimiter. This is what the `info` function does to collapse multi-line `doc string`s into a single line. 

So what is the `info` function actually doing with these `lambda`
functions, `split`s, and `and-or` tricks?

        processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)

`processFunc` is now a function, but which function it is depends on the
value of the `collapse` variable. If `collapse` is true,
`processFunc`(*string*) will collapse whitespace; otherwise,
`processFunc`(*string*) will return its argument unchanged.

To do this in a less robust language, like Visual Basic, you would
probably create a function that took a string and a *`collapse`*
argument and used an `if` statement to decide whether to collapse the
whitespace or not, then returned the appropriate value. This would be
inefficient, because the function would need to handle every possible
case. Every time you called it, it would need to decide whether to
collapse whitespace before it could give you what you wanted. In Python,
you can take that decision logic out of the function and define a
`lambda` function that is custom-tailored to give you exactly (and only)
what you want. This is more efficient, more elegant, and less prone to
those nasty oh-I-thought-those-arguments-were-reversed kinds of errors.

### Further Reading on `lambda` Functions

-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    discusses using `lambda` to [call functions
    indirectly](http://www.faqts.com/knowledge-base/view.phtml/aid/6081/fid/241).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    shows how to [access outside variables from inside a `lambda`
    function](http://www.python.org/doc/current/tut/node6.html#SECTION006740000000000000000).
    ([PEP 227](http://python.sourceforge.net/peps/pep-0227.html)
    explains how this will change in future versions of Python.)
-   [*The Whole Python FAQ*](http://www.python.org/doc/FAQ.html) has
    examples of [obfuscated one-liners using
    `lambda`](http://www.python.org/cgi-bin/faqw.py?query=4.15&querytype=simple&casefold=yes&req=search).

  

