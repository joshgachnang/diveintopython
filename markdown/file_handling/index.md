

Chapter 6. Exceptions and File Handling
---------------------------------------

-   [6.1. Handling Exceptions](index.html#fileinfo.exception)
    -   [6.1.1. Using Exceptions For Other
        Purposes](index.html#d0e14344)
-   [6.2. Working with File Objects](file_objects.html)
    -   [6.2.1. Reading Files](file_objects.html#d0e14670)
    -   [6.2.2. Closing Files](file_objects.html#d0e14800)
    -   [6.2.3. Handling I/O Errors](file_objects.html#d0e14928)
    -   [6.2.4. Writing to Files](file_objects.html#d0e15055)
-   [6.3. Iterating with for Loops](for_loops.html)
-   [6.4. Using sys.modules](more_on_modules.html)
-   [6.5. Working with Directories](os_module.html)
-   [6.6. Putting It All Together](all_together.html)
-   [6.7. Summary](summary.html)

In this chapter, you will dive into exceptions, file objects, `for`
loops, and the `os` and `sys` modules. If you've used exceptions in
another programming language, you can skim the first section to get a
sense of Python's syntax. Be sure to tune in again for file handling.

6.1. Handling Exceptions
------------------------

-   [6.1.1. Using Exceptions For Other Purposes](index.html#d0e14344)

Like many other programming languages, Python has exception handling via
`try...except` blocks.


![Note](../images/note.png) 
Python uses `try...except` to handle exceptions and `raise` to generate them. Java and C++ use `try...catch` to handle exceptions, and `throw` to generate them. 

Exceptions are everywhere in Python. Virtually every module in the
standard Python library uses them, and Python itself will raise them in
a lot of different circumstances. You've already seen them repeatedly
throughout this book.

-   [Accessing a non-existent dictionary
    key](../native_data_types/index.html#odbchelper.dict.define "Example 3.1. Defining a Dictionary")
    will raise a `KeyError` exception.
-   [Searching a list for a non-existent
    value](../native_data_types/lists.html#odbchelper.list.search "Example 3.12. Searching a List")
    will raise a `ValueError` exception.
-   [Calling a non-existent
    method](../native_data_types/tuples.html#odbchelper.tuplemethods "Example 3.16. Tuples Have No Methods")
    will raise an `AttributeError` exception.
-   [Referencing a non-existent
    variable](../native_data_types/declaring_variables.html#odbchelper.unboundvariable "Example 3.18. Referencing an Unbound Variable")
    will raise a `NameError` exception.
-   [Mixing datatypes without
    coercion](../native_data_types/formatting_strings.html#odbchelper.stringformatting.coerce "Example 3.22. String Formatting vs. Concatenating")
    will raise a `TypeError` exception.

In each of these cases, you were simply playing around in the Python
IDE: an error occurred, the exception was printed (depending on your
IDE, perhaps in an intentionally jarring shade of red), and that was
that. This is called an *unhandled* exception. When the exception was
raised, there was no code to explicitly notice it and deal with it, so
it bubbled its way back to the default behavior built in to Python,
which is to spit out some debugging information and give up. In the IDE,
that's no big deal, but if that happened while your actual Python
program was running, the entire program would come to a screeching halt.

An exception doesn't need result in a complete program crash, though.
Exceptions, when raised, can be *handled*. Sometimes an exception is
really because you have a bug in your code (like accessing a variable
that doesn't exist), but many times, an exception is something you can
anticipate. If you're opening a file, it might not exist. If you're
connecting to a database, it might be unavailable, or you might not have
the correct security credentials to access it. If you know a line of
code may raise an exception, you should handle the exception using a
`try...except` block.

### Example 6.1. Opening a Non-Existent File

    >>> fsock = open("/notthere", "r")      
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    IOError: [Errno 2] No such file or directory: '/notthere'
    >>> try:
    ...     fsock = open("/notthere")       
    ... except IOError:                     
    ...     print "The file does not exist, exiting gracefully"
    ... print "This line will always print" 
    The file does not exist, exiting gracefully
    This line will always print



[![1](../images/callouts/1.png)](#fileinfo.exceptions.1.1) Using the built-in `open` function, you can try to open a file for reading (more on `open` in the next section). But the file doesn't exist, so this raises the `IOError` exception. Since you haven't provided any explicit check for an `IOError` exception, Python just prints out some debugging information about what happened and then gives up. 

[![2](../images/callouts/2.png)](#fileinfo.exceptions.1.2) You're trying to open the same non-existent file, but this time you're doing it within a `try...except` block. 

[![3](../images/callouts/3.png)](#fileinfo.exceptions.1.3) When the `open` method raises an `IOError` exception, you're ready for it. The `except IOError:` line catches the exception and executes your own block of code, which in this case just prints a more pleasant error message. 

[![4](../images/callouts/4.png)](#fileinfo.exceptions.1.4) Once an exception has been handled, processing continues normally on the first line after the `try...except` block. Note that this line will always print, whether or not an exception occurs. If you really did have a file called `notthere` in your root directory, the call to `open` would succeed, the `except` clause would be ignored, and this line would still be executed. 

Exceptions may seem unfriendly (after all, if you don't catch the
exception, your entire program will crash), but consider the
alternative. Would you rather get back an unusable file object to a
non-existent file? You'd need to check its validity somehow anyway, and
if you forgot, somewhere down the line, your program would give you
strange errors somewhere down the line that you would need to trace back
to the source. I'm sure you've experienced this, and you know it's not
fun. With exceptions, errors occur immediately, and you can handle them
in a standard way at the source of the problem.

### 6.1.1. Using Exceptions For Other Purposes

There are a lot of other uses for exceptions besides handling actual
error conditions. A common use in the standard Python library is to try
to import a module, and then check whether it worked. Importing a module
that does not exist will raise an `ImportError` exception. You can use
this to define multiple levels of functionality based on which modules
are available at run-time, or to support multiple platforms (where
platform-specific code is separated into different modules).

You can also define your own exceptions by creating a class that
inherits from the built-in `Exception` class, and then raise your
exceptions with the `raise` command. See the further reading section if
you're interested in doing this.

The next example demonstrates how to use an exception to support
platform-specific functionality. This code comes from the `getpass`
module, a wrapper module for getting a password from the user. Getting a
password is accomplished differently on UNIX, Windows, and Mac OS
platforms, but this code encapsulates all of those differences.

### Example 6.2. Supporting Platform-Specific Functionality

      # Bind the name getpass to the appropriate function
      try:
          import termios, TERMIOS                     
      except ImportError:
          try:
              import msvcrt                           
          except ImportError:
              try:
                  from EasyDialogs import AskPassword 
              except ImportError:
                  getpass = default_getpass           
              else:                                   
                  getpass = AskPassword
          else:
              getpass = win_getpass
      else:
          getpass = unix_getpass



[![1](../images/callouts/1.png)](#fileinfo.exceptions.2.1) `termios` is a UNIX-specific module that provides low-level control over the input terminal. If this module is not available (because it's not on your system, or your system doesn't support it), the import fails and Python raises an `ImportError`, which you catch. 

[![2](../images/callouts/2.png)](#fileinfo.exceptions.2.2) OK, you didn't have `termios`, so let's try `msvcrt`, which is a Windows-specific module that provides an API to many useful functions in the Microsoft Visual C++ runtime services. If this import fails, Python will raise an `ImportError`, which you catch. 

[![3](../images/callouts/3.png)](#fileinfo.exceptions.2.3) If the first two didn't work, you try to import a function from `EasyDialogs`, which is a Mac OS-specific module that provides functions to pop up dialog boxes of various types. Once again, if this import fails, Python will raise an `ImportError`, which you catch. 

[![4](../images/callouts/4.png)](#fileinfo.exceptions.2.4) None of these platform-specific modules is available (which is possible, since Python has been ported to a lot of different platforms), so you need to fall back on a default password input function (which is defined elsewhere in the `getpass` module). Notice what you're doing here: assigning the function `default_getpass` to the variable `getpass`. If you read the official `getpass` documentation, it tells you that the `getpass` module defines a `getpass` function. It does this by binding `getpass` to the correct function for your platform. Then when you call the `getpass` function, you're really calling a platform-specific function that this code has set up for you. You don't need to know or care which platform your code is running on -- just call `getpass`, and it will always do the right thing. 

[![5](../images/callouts/5.png)](#fileinfo.exceptions.2.5) A `try...except` block can have an `else` clause, like an `if` statement. If no exception is raised during the `try` block, the `else` clause is executed afterwards. In this case, that means that the `from EasyDialogs import AskPassword` import worked, so you should bind `getpass` to the `AskPassword` function. Each of the other `try...except` blocks has similar `else` clauses to bind `getpass` to the appropriate function when you find an `import` that works. 

### Further Reading on Exception Handling

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses [defining and raising your own exceptions, and handling
    multiple exceptions at
    once](http://www.python.org/doc/current/tut/node10.html#SECTION0010400000000000000000).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the built-in
    exceptions](http://www.python.org/doc/current/lib/module-exceptions.html).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the
    [getpass](http://www.python.org/doc/current/lib/module-getpass.html)
    module.
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the [`traceback`
    module](http://www.python.org/doc/current/lib/module-traceback.html),
    which provides low-level access to exception attributes after an
    exception is raised.
-   [*Python Reference Manual*](http://www.python.org/doc/current/ref/)
    discusses the inner workings of the [`try...except`
    block](http://www.python.org/doc/current/ref/try.html).

  

