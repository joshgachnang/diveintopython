

Chapter 16. Functional Programming
----------------------------------

-   [16.1. Diving in](index.html#regression.divein)
-   [16.2. Finding the path](finding_the_path.html)
-   [16.3. Filtering lists revisited](filtering_lists.html)
-   [16.4. Mapping lists revisited](mapping_lists.html)
-   [16.5. Data-centric programming](data_centric.html)
-   [16.6. Dynamically importing modules](dynamic_import.html)
-   [16.7. Putting it all together](all_together.html)
-   [16.8. Summary](summary.html)

16.1. Diving in
---------------

In [Chapter 13, *Unit
Testing*](../unit_testing/index.html "Chapter 13. Unit Testing"), you
learned about the philosophy of unit testing. In [Chapter 14,
*Test-First
Programming*](../unit_testing/stage_1.html "Chapter 14. Test-First Programming"),
you stepped through the implementation of basic unit tests in Python. In
[Chapter 15,
*Refactoring*](../refactoring/index.html "Chapter 15. Refactoring"), you
saw how unit testing makes large-scale refactoring easier. This chapter
will build on those sample programs, but here we will focus more on
advanced Python-specific techniques, rather than on unit testing itself.

The following is a complete Python program that acts as a cheap and
simple regression testing framework. It takes unit tests that you've
written for individual modules, collects them all into one big test
suite, and runs them all at once. I actually use this script as part of
the build process for this book; I have unit tests for several of the
example programs (not just the `roman.py` module featured in
[Chapter 13, *Unit
Testing*](../unit_testing/index.html "Chapter 13. Unit Testing")), and
the first thing my automated build script does is run this program to
make sure all my examples still work. If this regression test fails, the
build immediately stops. I don't want to release non-working examples
any more than you want to download them and sit around scratching your
head and yelling at your monitor and wondering why they don't work.

### Example 16.1. `regression.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Regression testing framework

    This module will search for scripts in the same directory named
    XYZtest.py.  Each such script should be a test suite that tests a
    module through PyUnit.  (As of Python 2.1, PyUnit is included in
    the standard library as "unittest".)  This script will aggregate all
    found test suites into one big test suite and run them all at once.
    """

    import sys, os, re, unittest

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

    if __name__ == "__main__":                   
        unittest.main(defaultTest="regressionTest")

Running this script in the same directory as the rest of the example
scripts that come with this book will find all the unit tests, named
`module`test.py, run them as a single test, and pass or fail them all at
once.

### Example 16.2. Sample output of `regression.py`

    [you@localhost py]$ python regression.py -v
    help should fail with no object ... ok                             
    help should return known result for apihelper ... ok
    help should honor collapse argument ... ok
    help should honor spacing argument ... ok
    buildConnectionString should fail with list input ... ok           
    buildConnectionString should fail with string input ... ok
    buildConnectionString should fail with tuple input ... ok
    buildConnectionString handles empty dictionary ... ok
    buildConnectionString returns known result with known input ... ok
    fromRoman should only accept uppercase input ... ok                
    toRoman should always return uppercase ... ok
    fromRoman should fail with blank string ... ok
    fromRoman should fail with malformed antecedents ... ok
    fromRoman should fail with repeated pairs of numerals ... ok
    fromRoman should fail with too many repeated numerals ... ok
    fromRoman should give known result with known input ... ok
    toRoman should give known result with known input ... ok
    fromRoman(toRoman(n))==n for all n ... ok
    toRoman should fail with non-integer input ... ok
    toRoman should fail with negative input ... ok
    toRoman should fail with large input ... ok
    toRoman should fail with 0 input ... ok
    kgp a ref test ... ok
    kgp b ref test ... ok
    kgp c ref test ... ok
    kgp d ref test ... ok
    kgp e ref test ... ok
    kgp f ref test ... ok
    kgp g ref test ... ok

    ----------------------------------------------------------------------
    Ran 29 tests in 2.799s

    OK



[![1](../images/callouts/1.png)](#regression.divein.1.1) The first 5 tests are from `apihelpertest.py`, which tests the example script from [Chapter 4, *The Power Of Introspection*](../power_of_introspection/index.html "Chapter 4. The Power Of Introspection"). 

[![2](../images/callouts/2.png)](#regression.divein.1.2) The next 5 tests are from `odbchelpertest.py`, which tests the example script from [Chapter 2, *Your First Python Program*](../getting_to_know_python/index.html "Chapter 2. Your First Python Program"). 

[![3](../images/callouts/3.png)](#regression.divein.1.3) The rest are from `romantest.py`, which you studied in depth in [Chapter 13, *Unit Testing*](../unit_testing/index.html "Chapter 13. Unit Testing"). 

  

