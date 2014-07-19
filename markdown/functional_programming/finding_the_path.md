

16.2. Finding the path
----------------------

When running Python scripts from the command line, it is sometimes
useful to know where the currently running script is located on disk.

This is one of those obscure little tricks that is virtually impossible
to figure out on your own, but simple to remember once you see it. The
key to it is `sys.argv`. As you saw in [Chapter 9, *XML
Processing*](../xml_processing/index.html "Chapter 9. XML Processing"),
this is a list that holds the list of command-line arguments. However,
it also holds the name of the running script, exactly as it was called
from the command line, and this is enough information to determine its
location.

### Example 16.3. `fullpath.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    import sys, os

    print 'sys.argv[0] =', sys.argv[0]             
    pathname = os.path.dirname(sys.argv[0])        
    print 'path =', pathname
    print 'full path =', os.path.abspath(pathname) 



[![1](../images/callouts/1.png)](#regression.path.1.1) Regardless of how you run a script, `sys.argv[0]` will always contain the name of the script, exactly as it appears on the command line. This may or may not include any path information, as you'll see shortly. 

[![2](../images/callouts/2.png)](#regression.path.1.2) `os.path.dirname` takes a filename as a string and returns the directory path portion. If the given filename does not include any path information, `os.path.dirname` returns an empty string. 

[![3](../images/callouts/3.png)](#regression.path.1.3) `os.path.abspath` is the key here. It takes a pathname, which can be partial or even blank, and returns a fully qualified pathname. 

`os.path.abspath` deserves further explanation. It is very flexible; it
can take any kind of pathname.

### Example 16.4. Further explanation of `os.path.abspath`

    >>> import os
    >>> os.getcwd()                        
    /home/you
    >>> os.path.abspath('')                
    /home/you
    >>> os.path.abspath('.ssh')            
    /home/you/.ssh
    >>> os.path.abspath('/home/you/.ssh') 
    /home/you/.ssh
    >>> os.path.abspath('.ssh/../foo/')    
    /home/you/foo



[![1](../images/callouts/1.png)](#regression.path.2.1) `os.getcwd()` returns the current working directory. 

[![2](../images/callouts/2.png)](#regression.path.2.2) Calling `os.path.abspath` with an empty string returns the current working directory, same as `os.getcwd()`. 

[![3](../images/callouts/3.png)](#regression.path.2.3) Calling `os.path.abspath` with a partial pathname constructs a fully qualified pathname out of it, based on the current working directory. 

[![4](../images/callouts/4.png)](#regression.path.2.4) Calling `os.path.abspath` with a full pathname simply returns it. 

[![5](../images/callouts/5.png)](#regression.path.2.5) `os.path.abspath` also *normalizes* the pathname it returns. Note that this example worked even though I don't actually have a 'foo' directory. `os.path.abspath` never checks your actual disk; this is all just string manipulation. 


![Note](../images/note.png) 
The pathnames and filenames you pass to `os.path.abspath` do not need to exist. 


![Note](../images/note.png) 
`os.path.abspath` not only constructs full path names, it also normalizes them. That means that if you are in the `/usr/` directory, `os.path.abspath('bin/../local/bin')` will return `/usr/local/bin`. It normalizes the path by making it as simple as possible. If you just want to normalize a pathname like this without turning it into a full pathname, use `os.path.normpath` instead. 

### Example 16.5. Sample output from `fullpath.py`

    [you@localhost py]$ python /home/you/diveintopython/common/py/fullpath.py 
    sys.argv[0] = /home/you/diveintopython/common/py/fullpath.py
    path = /home/you/diveintopython/common/py
    full path = /home/you/diveintopython/common/py
    [you@localhost diveintopython]$ python common/py/fullpath.py               
    sys.argv[0] = common/py/fullpath.py
    path = common/py
    full path = /home/you/diveintopython/common/py
    [you@localhost diveintopython]$ cd common/py
    [you@localhost py]$ python fullpath.py                                     
    sys.argv[0] = fullpath.py
    path = 
    full path = /home/you/diveintopython/common/py



[![1](../images/callouts/1.png)](#regression.path.3.1) In the first case, `sys.argv[0]` includes the full path of the script. You can then use the `os.path.dirname` function to strip off the script name and return the full directory name, and `os.path.abspath` simply returns what you give it. 

[![2](../images/callouts/2.png)](#regression.path.3.2) If the script is run by using a partial pathname, `sys.argv[0]` will still contain exactly what appears on the command line. `os.path.dirname` will then give you a partial pathname (relative to the current directory), and `os.path.abspath` will construct a full pathname from the partial pathname. 

[![3](../images/callouts/3.png)](#regression.path.3.3) If the script is run from the current directory without giving any path, `os.path.dirname` will simply return an empty string. Given an empty string, `os.path.abspath` returns the current directory, which is what you want, since the script was run from the current directory. 


![Note](../images/note.png) 
Like the other functions in the `os` and `os.path` modules, `os.path.abspath` is cross-platform. Your results will look slightly different than my examples if you're running on Windows (which uses backslash as a path separator) or Mac OS (which uses colons), but they'll still work. That's the whole point of the `os` module. 

**Addendum. **One reader was dissatisfied with this solution, and wanted
to be able to run all the unit tests in the current directory, not the
directory where `regression.py` is located. He suggests this approach
instead:

### Example 16.6. Running scripts in the current directory

    import sys, os, re, unittest

    def regressionTest():
        path = os.getcwd()       
        sys.path.append(path)    
        files = os.listdir(path) 



[![1](../images/callouts/1.png)](#regression.path.4.1) Instead of setting `path` to the directory where the currently running script is located, you set it to the current working directory instead. This will be whatever directory you were in before you ran the script, which is not necessarily the same as the directory the script is in. (Read that sentence a few times until you get it.) 

[![2](../images/callouts/2.png)](#regression.path.4.2) Append this directory to the Python library search path, so that when you dynamically import the unit test modules later, Python can find them. You didn't need to do this when `path` was the directory of the currently running script, because Python always looks in that directory. 

[![3](../images/callouts/3.png)](#regression.path.4.3) The rest of the function is the same. 

This technique will allow you to re-use this `regression.py` script on
multiple projects. Just put the script in a common directory, then
change to the project's directory before running it. All of that
project's unit tests will be found and tested, instead of the unit tests
in the common directory where `regression.py` is located.

  

