

10.2. Standard input, output, and error
---------------------------------------

UNIX users are already familiar with the concept of standard input,
standard output, and standard error. This section is for the rest of
you.

Standard output and standard error (commonly abbreviated `stdout` and
`stderr`) are pipes that are built into every UNIX system. When you
`print` something, it goes to the `stdout` pipe; when your program
crashes and prints out debugging information (like a traceback in
Python), it goes to the `stderr` pipe. Both of these pipes are
ordinarily just connected to the terminal window where you are working,
so when a program prints, you see the output, and when a program
crashes, you see the debugging information. (If you're working on a
system with a window-based Python IDE, `stdout` and `stderr` default to
your “Interactive Window”.)

### Example 10.8. Introducing `stdout` and `stderr`

    >>> for i in range(3):
    ...     print 'Dive in'             
    Dive in
    Dive in
    Dive in
    >>> import sys
    >>> for i in range(3):
    ...     sys.stdout.write('Dive in') 
    Dive inDive inDive in
    >>> for i in range(3):
    ...     sys.stderr.write('Dive in') 
    Dive inDive inDive in



[![1](../images/callouts/1.png)](#kgp.stdio.1.1) As you saw in [Example 6.9, “Simple Counters”](../file_handling/for_loops.html#fileinfo.for.counter "Example 6.9. Simple Counters"), you can use Python's built-in `range` function to build simple counter loops that repeat something a set number of times. 

[![2](../images/callouts/2.png)](#kgp.stdio.1.2) `stdout` is a file-like object; calling its `write` function will print out whatever string you give it. In fact, this is what the `print` function really does; it adds a carriage return to the end of the string you're printing, and calls `sys.stdout.write`. 

[![3](../images/callouts/3.png)](#kgp.stdio.1.3) In the simplest case, `stdout` and `stderr` send their output to the same place: the Python IDE (if you're in one), or the terminal (if you're running Python from the command line). Like `stdout`, `stderr` does not add carriage returns for you; if you want them, add them yourself. 

`stdout` and `stderr` are both file-like objects, like the ones you
discussed in [Section 10.1, “Abstracting input
sources”](index.html#kgp.openanything "10.1. Abstracting input sources"),
but they are both write-only. They have no `read` method, only `write`.
Still, they are file-like objects, and you can assign any other file- or
file-like object to them to redirect their output.

### Example 10.9. Redirecting output

    [you@localhost kgp]$ python stdout.py
    Dive in
    [you@localhost kgp]$ cat out.log
    This message will be logged instead of displayed

(On Windows, you can use `type` instead of `cat` to display the contents
of a file.)

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    #stdout.py
    import sys

    print 'Dive in'                                          
    saveout = sys.stdout                                     
    fsock = open('out.log', 'w')                             
    sys.stdout = fsock                                       
    print 'This message will be logged instead of displayed' 
    sys.stdout = saveout                                     
    fsock.close()                                            



[![1](../images/callouts/1.png)](#kgp.stdio.2.1) This will print to the IDE “Interactive Window” (or the terminal, if running the script from the command line). 

[![2](../images/callouts/2.png)](#kgp.stdio.2.2) Always save `stdout` before redirecting it, so you can set it back to normal later. 

[![3](../images/callouts/3.png)](#kgp.stdio.2.3) Open a file for writing. If the file doesn't exist, it will be created. If the file does exist, it will be overwritten. 

[![4](../images/callouts/4.png)](#kgp.stdio.2.4) Redirect all further output to the new file you just opened. 

[![5](../images/callouts/5.png)](#kgp.stdio.2.5) This will be “printed” to the log file only; it will not be visible in the IDE window or on the screen. 

[![6](../images/callouts/6.png)](#kgp.stdio.2.6) Set `stdout` back to the way it was before you mucked with it. 

[![7](../images/callouts/7.png)](#kgp.stdio.2.7) Close the log file. 

Redirecting `stderr` works exactly the same way, using `sys.stderr`
instead of `sys.stdout`.

### Example 10.10. Redirecting error information

    [you@localhost kgp]$ python stderr.py
    [you@localhost kgp]$ cat error.log
    Traceback (most recent line last):
      File "stderr.py", line 5, in ?
        raise Exception, 'this error will be logged'
    Exception: this error will be logged

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    #stderr.py
    import sys

    fsock = open('error.log', 'w')               
    sys.stderr = fsock                           
    raise Exception, 'this error will be logged'  



[![1](../images/callouts/1.png)](#kgp.stdio.3.1) Open the log file where you want to store debugging information. 

[![2](../images/callouts/2.png)](#kgp.stdio.3.2) Redirect standard error by assigning the file object of the newly-opened log file to `stderr`. 

[![3](../images/callouts/3.png)](#kgp.stdio.3.3) Raise an exception. Note from the screen output that this does *not* print anything on screen. All the normal traceback information has been written to `error.log`. 

[![4](../images/callouts/4.png)](#kgp.stdio.3.4) Also note that you're not explicitly closing your log file, nor are you setting `stderr` back to its original value. This is fine, since once the program crashes (because of the exception), Python will clean up and close the file for us, and it doesn't make any difference that `stderr` is never restored, since, as I mentioned, the program crashes and Python ends. Restoring the original is more important for `stdout`, if you expect to go do other stuff within the same script afterwards. 

Since it is so common to write error messages to standard error, there
is a shorthand syntax that can be used instead of going through the
hassle of redirecting it outright.

### Example 10.11. Printing to `stderr`

    >>> print 'entering function'
    entering function
    >>> import sys
    >>> print >> sys.stderr, 'entering function' 
    entering function



[![1](../images/callouts/1.png)](#kgp.stdio.6.1) This shorthand syntax of the `print` statement can be used to write to any open file, or file-like object. In this case, you can redirect a single `print` statement to `stderr` without affecting subsequent `print` statements. 

Standard input, on the other hand, is a read-only file object, and it
represents the data flowing into the program from some previous program.
This will likely not make much sense to classic Mac OS users, or even
Windows users unless you were ever fluent on the MS-DOS command line.
The way it works is that you can construct a chain of commands in a
single line, so that one program's output becomes the input for the next
program in the chain. The first program simply outputs to standard
output (without doing any special redirecting itself, just doing normal
`print` statements or whatever), and the next program reads from
standard input, and the operating system takes care of connecting one
program's output to the next program's input.

### Example 10.12. Chaining commands

    [you@localhost kgp]$ python kgp.py -g binary.xml         
    01100111
    [you@localhost kgp]$ cat binary.xml                      
    <?xml version="1.0"?>
    <!DOCTYPE grammar PUBLIC "-//diveintopython.net//DTD Kant Generator Pro v1.0//EN" "kgp.dtd">
    <grammar>
    <ref id="bit">
      <p>0</p>
      <p>1</p>
    </ref>
    <ref id="byte">
      <p><xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/>\
    <xref id="bit"/><xref id="bit"/><xref id="bit"/><xref id="bit"/></p>
    </ref>
    </grammar>
    [you@localhost kgp]$ cat binary.xml   python kgp.py -g -  
    10110001



[![1](../images/callouts/1.png)](#kgp.stdio.4.1) As you saw in [Section 9.1, “Diving in”](../xml_processing/index.html#kgp.divein "9.1. Diving in"), this will print a string of eight random bits, `0` or `1`. 

[![2](../images/callouts/2.png)](#kgp.stdio.4.2) This simply prints out the entire contents of `binary.xml`. (Windows users should use `type` instead of `cat`.) 

[![3](../images/callouts/3.png)](#kgp.stdio.4.3) This prints the contents of `binary.xml`, but the “` `” character, called the “pipe” character, means that the contents will not be printed to the screen. Instead, they will become the standard input of the next command, which in this case calls your Python script. 

[![4](../images/callouts/4.png)](#kgp.stdio.4.4) Instead of specifying a module (like `binary.xml`), you specify “`-`”, which causes your script to load the grammar from standard input instead of from a specific file on disk. (More on how this happens in the next example.) So the effect is the same as the first syntax, where you specified the grammar filename directly, but think of the expansion possibilities here. Instead of simply doing `cat binary.xml`, you could run a script that dynamically generates the grammar, then you can pipe it into your script. It could come from anywhere: a database, or some grammar-generating meta-script, or whatever. The point is that you don't need to change your `kgp.py` script at all to incorporate any of this functionality. All you need to do is be able to take grammar files from standard input, and you can separate all the other logic into another program. 

So how does the script “know” to read from standard input when the
grammar file is “`-`”? It's not magic; it's just code.

### Example 10.13. Reading from standard input in `kgp.py`

    def openAnything(source):
        if source == "-":    
            import sys
            return sys.stdin

        # try to open with urllib (if source is http, ftp, or file URL)
        import urllib
        try:

    [... snip ...]



[![1](../images/callouts/1.png)](#kgp.stdio.5.1) This is the `openAnything` function from `toolbox.py`, which you previously examined in [Section 10.1, “Abstracting input sources”](index.html#kgp.openanything "10.1. Abstracting input sources"). All you've done is add three lines of code at the beginning of the function to check if the source is “`-`”; if so, you return `sys.stdin`. Really, that's it! Remember, `stdin` is a file-like object with a `read` method, so the rest of the code (in `kgp.py`, where you call `openAnything`) doesn't change a bit. 

  

