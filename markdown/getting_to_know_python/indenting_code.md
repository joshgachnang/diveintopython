

2.5. Indenting Code
-------------------

Python functions have no explicit `begin` or `end`, and no curly braces
to mark where the function code starts and stops. The only delimiter is
a colon (`:`) and the indentation of the code itself.

### Example 2.5. Indenting the `buildConnectionString` Function

    def buildConnectionString(params):
        """Build a connection string from a dictionary of parameters.

        Returns string."""
        return ";".join(["%s=%s" % (k, v) for k, v in params.items()])

Code blocks are defined by their indentation. By "code block", I mean
functions, `if` statements, `for` loops, `while` loops, and so forth.
Indenting starts a block and unindenting ends it. There are no explicit
braces, brackets, or keywords. This means that whitespace is
significant, and must be consistent. In this example, the function code
(including the `doc string`) is indented four spaces. It doesn't need to
be four spaces, it just needs to be consistent. The first line that is
not indented is outside the function.

[Example 2.6, “if
Statements”](indenting_code.html#odbchelper.indenting.if "Example 2.6. if Statements")
shows an example of code indentation with `if` statements.

### Example 2.6. `if` Statements

    def fib(n):                   
        print 'n =', n            
        if n > 1:                 
            return n * fib(n - 1)
        else:                     
            print 'end of the line'
            return 1



[![1](../images/callouts/1.png)](#odbchelper.indenting.2.1) This is a function named `fib` that takes one argument, `n`. All the code within the function is indented. 

[![2](../images/callouts/2.png)](#odbchelper.indenting.2.2) Printing to the screen is very easy in Python, just use `print`. `print` statements can take any data type, including strings, integers, and other native types like dictionaries and lists that you'll learn about in the next chapter. You can even mix and match to print several things on one line by using a comma-separated list of values. Each value is printed on the same line, separated by spaces (the commas don't print). So when `fib` is called with `5`, this will print "n = 5". 

[![3](../images/callouts/3.png)](#odbchelper.indenting.2.3) `if` statements are a type of code block. If the `if` expression evaluates to true, the indented block is executed, otherwise it falls to the `else` block. 

[![4](../images/callouts/4.png)](#odbchelper.indenting.2.4) Of course `if` and `else` blocks can contain multiple lines, as long as they are all indented the same amount. This `else` block has two lines of code in it. There is no other special syntax for multi-line code blocks. Just indent and get on with your life. 

After some initial protests and several snide analogies to Fortran, you
will make peace with this and start seeing its benefits. One major
benefit is that all Python programs look similar, since indentation is a
language requirement and not a matter of style. This makes it easier to
read and understand other people's Python code.


![Note](../images/note.png) 
Python uses carriage returns to separate statements and a colon and indentation to separate code blocks. C++ and Java use semicolons to separate statements and curly braces to separate code blocks. 

### Further Reading on Code Indentation

-   [*Python Reference Manual*](http://www.python.org/doc/current/ref/)
    discusses cross-platform indentation issues and [shows various
    indentation
    errors](http://www.python.org/doc/current/ref/indentation.html).
-   [*Python Style
    Guide*](http://www.python.org/doc/essays/styleguide.html) discusses
    good indentation style.

  

