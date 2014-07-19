

Chapter 2. Your First Python Program
------------------------------------

-   [2.1. Diving in](index.html#odbchelper.divein)
-   [2.2. Declaring Functions](declaring_functions.html)
    -   [2.2.1. How Python's Datatypes Compare to Other Programming
        Languages](declaring_functions.html#d0e4188)
-   [2.3. Documenting Functions](documenting_functions.html)
-   [2.4. Everything Is an Object](everything_is_an_object.html)
    -   [2.4.1. The Import Search
        Path](everything_is_an_object.html#d0e4550)
    -   [2.4.2. What's an Object?](everything_is_an_object.html#d0e4665)
-   [2.5. Indenting Code](indenting_code.html)
-   [2.6. Testing Modules](testing_modules.html)

You know how other books go on and on about programming fundamentals and
finally work up to building a complete, working program? Let's skip all
that.

2.1. Diving in
--------------

Here is a complete, working Python program.

It probably makes absolutely no sense to you. Don't worry about that,
because you're going to dissect it line by line. But read through it
first and see what, if anything, you can make of it.

### Example 2.1. `odbchelper.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    def buildConnectionString(params):
        """Build a connection string from a dictionary of parameters.

        Returns string."""
        return ";".join(["%s=%s" % (k, v) for k, v in params.items()])

    if __name__ == "__main__":
        myParams = {"server":"mpilgrim", \
                    "database":"master", \
                    "uid":"sa", \
                    "pwd":"secret" \
                    }
        print buildConnectionString(myParams)

Now run this program and see what happens.


![Tip](../images/tip.png) 
In the ActivePython IDE on Windows, you can run the Python program you're editing by choosing File-\>Run... (****Ctrl**-R**). Output is displayed in the interactive window. 


![Tip](../images/tip.png) 
In the Python IDE on Mac OS, you can run a Python program with Python-\>Run window... (****Cmd**-R**), but there is an important option you must set first. Open the `.py` file in the IDE, pop up the options menu by clicking the black triangle in the upper-right corner of the window, and make sure the Run as \_\_main\_\_ option is checked. This is a per-file setting, but you'll only need to do it once per file. 


![Tip](../images/tip.png) 
On UNIX-compatible systems (including Mac OS X), you can run a Python program from the command line: **`python odbchelper.py`** 

The output of `odbchelper.py` will look like this:

    server=mpilgrim;uid=sa;database=master;pwd=secret

  

