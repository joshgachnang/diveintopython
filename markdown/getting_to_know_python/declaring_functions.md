


2.2. Declaring Functions
------------------------

-   [2.2.1. How Python's Datatypes Compare to Other Programming
    Languages](declaring_functions.html#d0e4188)

Python has functions like most other languages, but it does not have
separate header files like C++ or `interface`/`implementation` sections
like Pascal. When you need a function, just declare it, like this:

    def buildConnectionString(params):

Note that the keyword `def` starts the function declaration, followed by
the function name, followed by the arguments in parentheses. Multiple
arguments (not shown here) are separated with commas.

Also note that the function doesn't define a return datatype. Python
functions do not specify the datatype of their return value; they don't
even specify whether or not they return a value. In fact, every Python
function returns a value; if the function ever executes a `return`
statement, it will return that value, otherwise it will return `None`,
the Python null value.


![Note](../images/note.png) 
In Visual Basic, functions (that return a value) start with `function`, and subroutines (that do not return a value) start with `sub`. There are no subroutines in Python. Everything is a function, all functions return a value (even if it's `None`), and all functions start with `def`. 

The argument, `params`, doesn't specify a datatype. In Python, variables
are never explicitly typed. Python figures out what type a variable is
and keeps track of it internally.


![Note](../images/note.png) 
In Java, C++, and other statically-typed languages, you must specify the datatype of the function return value and each function argument. In Python, you never explicitly specify the datatype of anything. Based on what value you assign, Python keeps track of the datatype internally. 

### 2.2.1. How Python's Datatypes Compare to Other Programming Languages

An erudite reader sent me this explanation of how Python compares to
other programming languages:

statically typed language
:   A language in which types are fixed at compile time. Most statically
    typed languages enforce this by requiring you to declare all
    variables with their datatypes before using them. Java and C are
    statically typed languages.
dynamically typed language
:   A language in which types are discovered at execution time; the
    opposite of statically typed. VBScript and Python are dynamically
    typed, because they figure out what type a variable is when you
    first assign it a value.
strongly typed language
:   A language in which types are always enforced. Java and Python are
    strongly typed. If you have an integer, you can't treat it like a
    string without explicitly converting it.
weakly typed language
:   A language in which types may be ignored; the opposite of strongly
    typed. VBScript is weakly typed. In VBScript, you can concatenate
    the string `'12'` and the integer `3` to get the string `'123'`,
    then treat that as the integer `123`, all without any explicit
    conversion.

So Python is both *dynamically typed* (because it doesn't use explicit
datatype declarations) and *strongly typed* (because once a variable has
a datatype, it actually matters).

  

