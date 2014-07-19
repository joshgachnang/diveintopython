

3.4. Declaring variables
------------------------

-   [3.4.1. Referencing Variables](declaring_variables.html#d0e6873)
-   [3.4.2. Assigning Multiple Values at
    Once](declaring_variables.html#odbchelper.multiassign)

Now that you know something about dictionaries, tuples, and lists (oh
my!), let's get back to the sample program from [Chapter
2](../getting_to_know_python/index.html), `odbchelper.py`.

Python has local and global variables like most other languages, but it
has no explicit variable declarations. Variables spring into existence
by being assigned a value, and they are automatically destroyed when
they go out of scope.

### Example 3.17. Defining the `myParams` Variable

    if __name__ == "__main__":
        myParams = {"server":"mpilgrim", \
                    "database":"master", \
                    "uid":"sa", \
                    "pwd":"secret" \
                    }

Notice the indentation. An `if` statement is a code block and needs to
be indented just like a function.

Also notice that the variable assignment is one command split over
several lines, with a backslash (“`\`”) serving as a line-continuation
marker.


![Note](../images/note.png) 
When a command is split among several lines with the line-continuation marker (“`\`”), the continued lines can be indented in any manner; Python's normally stringent indentation rules do not apply. If your Python IDE auto-indents the continued line, you should probably accept its default unless you have a burning reason not to. 

Strictly speaking, expressions in parentheses, straight brackets, or
curly braces (like [defining a
dictionary](declaring_variables.html#myparamsdef "Example 3.17. Defining the myParams Variable"))
can be split into multiple lines with or without the line continuation
character (“`\`”). I like to include the backslash even when it's not
required because I think it makes the code easier to read, but that's a
matter of style.

Third, you never declared the variable `myParams`, you just assigned a
value to it. This is like VBScript without the `option explicit` option.
Luckily, unlike VBScript, Python will not allow you to reference a
variable that has never been assigned a value; trying to do so will
raise an exception.

### 3.4.1. Referencing Variables

### Example 3.18. Referencing an Unbound Variable

    >>> x
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    NameError: There is no variable named 'x'
    >>> x = 1
    >>> x
    1

You will thank Python for this one day.

### 3.4.2. Assigning Multiple Values at Once

One of the cooler programming shortcuts in Python is using sequences to
assign multiple values at once.

### Example 3.19. Assigning multiple values at once

    >>> v = ('a', 'b', 'e')
    >>> (x, y, z) = v     
    >>> x
    'a'
    >>> y
    'b'
    >>> z
    'e'



[![1](../images/callouts/1.png)](#odbchelper.multiassign.1.1) `v` is a tuple of three elements, and `(x, y, z)` is a tuple of three variables. Assigning one to the other assigns each of the values of `v` to each of the variables, in order. 

This has all sorts of uses. I often want to assign names to a range of
values. In C, you would use `enum` and manually list each constant and
its associated value, which seems especially tedious when the values are
consecutive. In Python, you can use the built-in `range` function with
multi-variable assignment to quickly assign consecutive values.

### Example 3.20. Assigning Consecutive Values

    >>> range(7)                                                                    
    [0, 1, 2, 3, 4, 5, 6]
    >>> (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7) 
    >>> MONDAY                                                                      
    0
    >>> TUESDAY
    1
    >>> SUNDAY
    6



[![1](../images/callouts/1.png)](#odbchelper.multiassign.2.1) The built-in `range` function returns a list of integers. In its simplest form, it takes an upper limit and returns a zero-based list counting up to but not including the upper limit. (If you like, you can pass other parameters to specify a base other than `0` and a step other than `1`. You can `print range.__doc__` for details.) 

[![2](../images/callouts/2.png)](#odbchelper.multiassign.2.2) `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, `SATURDAY`, and `SUNDAY` are the variables you're defining. (This example came from the `calendar` module, a fun little module that prints calendars, like the UNIX program `cal`. The `calendar` module defines integer constants for days of the week.) 

[![3](../images/callouts/3.png)](#odbchelper.multiassign.2.3) Now each variable has its value: `MONDAY` is `0`, `TUESDAY` is `1`, and so forth. 

You can also use multi-variable assignment to build functions that
return multiple values, simply by returning a tuple of all the values.
The caller can treat it as a tuple, or assign the values to individual
variables. Many standard Python libraries do this, including the `os`
module, which you'll discuss in [Chapter
6](../file_handling/index.html).

### Further Reading on Variables

-   [*Python Reference Manual*](http://www.python.org/doc/current/ref/)
    shows examples of [when you can skip the line continuation
    character](http://www.python.org/doc/current/ref/implicit-joining.html)
    and [when you need to use
    it](http://www.python.org/doc/current/ref/explicit-joining.html).
-   [*How to Think Like a Computer
    Scientist*](http://www.ibiblio.org/obp/thinkCSpy/ "Python book for computer science majors")
    shows how to use multi-variable assignment to [swap the values of
    two variables](http://www.ibiblio.org/obp/thinkCSpy/chap09.htm).

  

