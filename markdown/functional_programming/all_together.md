

16.7. Putting it all together
-----------------------------

You've learned enough now to deconstruct the first seven lines of this
chapter's code sample: reading a directory and importing selected
modules within it.

### Example 16.16. The `regressionTest` function

    def regressionTest():
        path = os.path.abspath(os.path.dirname(sys.argv[0]))   
        files = os.listdir(path)                               
        test = re.compile("test\.py$", re.IGNORECASE)          
        files = filter(test.search, files)                     
        filenameToModuleName = lambda f: os.path.splitext(f)[0]
        moduleNames = map(filenameToModuleName, files)         
        modules = map(__import__, moduleNames)                 
    load = unittest.defaultTestLoader.loadTestsFromModule  
    return unittest.TestSuite(map(load, modules))          

Let's look at it line by line, interactively. Assume that the current
directory is `c:\diveintopython\py`, which contains the examples that
come with this book, including this chapter's script. As you saw in
[Section 16.2, “Finding the
path”](finding_the_path.html "16.2. Finding the path"), the script
directory will end up in the `path` variable, so let's start hard-code
that and go from there.

### Example 16.17. Step 1: Get all the files

    >>> import sys, os, re, unittest
    >>> path = r'c:\diveintopython\py'
    >>> files = os.listdir(path)                               
    >>> files 
    ['BaseHTMLProcessor.py', 'LICENSE.txt', 'apihelper.py', 'apihelpertest.py',
    'argecho.py', 'autosize.py', 'builddialectexamples.py', 'dialect.py',
    'fileinfo.py', 'fullpath.py', 'kgptest.py', 'makerealworddoc.py',
    'odbchelper.py', 'odbchelpertest.py', 'parsephone.py', 'piglatin.py',
    'plural.py', 'pluraltest.py', 'pyfontify.py', 'regression.py', 'roman.py', 'romantest.py',
    'uncurly.py', 'unicode2koi8r.py', 'urllister.py', 'kgp', 'plural', 'roman',
    'colorize.py']



[![1](../images/callouts/1.png)](#regression.alltogether.1.1) `files` is a list of all the files and directories in the script's directory. (If you've been running some of the examples already, you may also see some `.pyc` files in there as well.) 

### Example 16.18. Step 2: Filter to find the files you care about

    >>> test = re.compile("test\.py$", re.IGNORECASE)           
    >>> files = filter(test.search, files)                      
    >>> files                                                   
    ['apihelpertest.py', 'kgptest.py', 'odbchelpertest.py', 'pluraltest.py', 'romantest.py']



[![1](../images/callouts/1.png)](#regression.alltogether.2.1) This regular expression will match any string that ends with `test.py`. Note that you need to escape the period, since a period in a regular expression usually means “match any single character”, but you actually want to match a literal period instead. 

[![2](../images/callouts/2.png)](#regression.alltogether.2.2) The compiled regular expression acts like a function, so you can use it to filter the large list of files and directories, to find the ones that match the regular expression. 

[![3](../images/callouts/3.png)](#regression.alltogether.2.3) And you're left with the list of unit testing scripts, because they were the only ones named `SOMETHINGtest.py`. 

### Example 16.19. Step 3: Map filenames to module names

    >>> filenameToModuleName = lambda f: os.path.splitext(f)[0] 
    >>> filenameToModuleName('romantest.py')                    
    'romantest'
    >>> filenameToModuleName('odchelpertest.py')
    'odbchelpertest'
    >>> moduleNames = map(filenameToModuleName, files)          
    >>> moduleNames                                             
    ['apihelpertest', 'kgptest', 'odbchelpertest', 'pluraltest', 'romantest']



[![1](../images/callouts/1.png)](#regression.alltogether.3.1) As you saw in [Section 4.7, “Using lambda Functions”](../power_of_introspection/lambda_functions.html "4.7. Using lambda Functions"), `lambda` is a quick-and-dirty way of creating an inline, one-line function. This one takes a filename with an extension and returns just the filename part, using the standard library function `os.path.splitext` that you saw in [Example 6.17, “Splitting Pathnames”](../file_handling/os_module.html#splittingpathnames.example "Example 6.17. Splitting Pathnames"). 

[![2](../images/callouts/2.png)](#regression.alltogether.3.2) `filenameToModuleName` is a function. There's nothing magic about `lambda` functions as opposed to regular functions that you define with a `def` statement. You can call the `filenameToModuleName` function like any other, and it does just what you wanted it to do: strips the file extension off of its argument. 

[![3](../images/callouts/3.png)](#regression.alltogether.3.3) Now you can apply this function to each file in the list of unit test files, using `map`. 

[![4](../images/callouts/4.png)](#regression.alltogether.3.4) And the result is just what you wanted: a list of modules, as strings. 

### Example 16.20. Step 4: Mapping module names to modules

    >>> modules = map(__import__, moduleNames)                  
    >>> modules                                                 
    [<module 'apihelpertest' from 'apihelpertest.py'>,
    <module 'kgptest' from 'kgptest.py'>,
    <module 'odbchelpertest' from 'odbchelpertest.py'>,
    <module 'pluraltest' from 'pluraltest.py'>,
    <module 'romantest' from 'romantest.py'>]
    >>> modules[-1]                                             
    <module 'romantest' from 'romantest.py'>



[![1](../images/callouts/1.png)](#regression.alltogether.4.1) As you saw in [Section 16.6, “Dynamically importing modules”](dynamic_import.html "16.6. Dynamically importing modules"), you can use a combination of `map` and `__import__` to map a list of module names (as strings) into actual modules (which you can call or access like any other module). 

[![2](../images/callouts/2.png)](#regression.alltogether.4.2) `modules` is now a list of modules, fully accessible like any other module. 

[![3](../images/callouts/3.png)](#regression.alltogether.4.3) The last module in the list *is* the `romantest` module, just as if you had said `import romantest`. 

### Example 16.21. Step 5: Loading the modules into a test suite

    >>> load = unittest.defaultTestLoader.loadTestsFromModule  
    >>> map(load, modules)                     
    [<unittest.TestSuite tests=[
      <unittest.TestSuite tests=[<apihelpertest.BadInput testMethod=testNoObject>]>,
      <unittest.TestSuite tests=[<apihelpertest.KnownValues testMethod=testApiHelper>]>,
      <unittest.TestSuite tests=[
        <apihelpertest.ParamChecks testMethod=testCollapse>, 
        <apihelpertest.ParamChecks testMethod=testSpacing>]>, 
        ...
      ]
    ]
    >>> unittest.TestSuite(map(load, modules)) 



[![1](../images/callouts/1.png)](#regression.alltogether.5.1) These are real module objects. Not only can you access them like any other module, instantiate classes and call functions, you can also introspect into the module to figure out which classes and functions it has in the first place. That's what the `loadTestsFromModule` method does: it introspects into each module and returns a `unittest.TestSuite` object for each module. Each `TestSuite` object actually contains a list of `TestSuite` objects, one for each `TestCase` class in your module, and each of those `TestSuite` objects contains a list of tests, one for each test method in your module. 

[![2](../images/callouts/2.png)](#regression.alltogether.5.2) Finally, you wrap the list of `TestSuite` objects into one big test suite. The `unittest` module has no problem traversing this tree of nested test suites within test suites; eventually it gets down to an individual test method and executes it, verifies that it passes or fails, and moves on to the next one. 

This introspection process is what the `unittest` module usually does
for us. Remember that magic-looking `unittest.main()` function that our
individual test modules called to kick the whole thing off?
`unittest.main()` actually creates an instance of
`unittest.TestProgram`, which in turn creates an instance of a
`unittest.defaultTestLoader` and loads it up with the module that called
it. (How does it get a reference to the module that called it if you
don't give it one? By using the equally-magic `__import__('__main__')`
command, which dynamically imports the currently-running module. I could
write a book on all the tricks and techniques used in the `unittest`
module, but then I'd never finish this one.)

### Example 16.22. Step 6: Telling `unittest` to use your test suite

    if __name__ == "__main__":                   
        unittest.main(defaultTest="regressionTest") 



[![1](../images/callouts/1.png)](#regression.alltogether.6.1) Instead of letting the `unittest` module do all its magic for us, you've done most of it yourself. You've created a function (`regressionTest`) that imports the modules yourself, calls `unittest.defaultTestLoader` yourself, and wraps it all up in a test suite. Now all you need to do is tell `unittest` that, instead of looking for tests and building a test suite in the usual way, it should just call the `regressionTest` function, which returns a ready-to-use `TestSuite`. 

  

