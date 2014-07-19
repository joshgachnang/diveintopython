

Chapter 14. Test-First Programming
----------------------------------

-   [14.1. roman.py, stage 1](stage_1.html#roman.stage1)
-   [14.2. roman.py, stage 2](stage_2.html)
-   [14.3. roman.py, stage 3](stage_3.html)
-   [14.4. roman.py, stage 4](stage_4.html)
-   [14.5. roman.py, stage 5](stage_5.html)

14.1. `roman.py`, stage 1
-------------------------

Now that the unit tests are complete, it's time to start writing the
code that the test cases are attempting to test. You're going to do this
in stages, so you can see all the unit tests fail, then watch them pass
one by one as you fill in the gaps in `roman.py`.

### Example 14.1. `roman1.py`

This file is available in `py/roman/stage1/` in the examples directory.

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Convert to and from Roman numerals"""

    #Define exceptions
    class RomanError(Exception): pass                
    class OutOfRangeError(RomanError): pass          
    class NotIntegerError(RomanError): pass
    class InvalidRomanNumeralError(RomanError): pass 

    def toRoman(n):
        """convert integer to Roman numeral"""
        pass                                         

    def fromRoman(s):
        """convert Roman numeral to integer"""
        pass



[![1](../images/callouts/1.png)](#roman.stage1.1.1) This is how you define your own custom exceptions in Python. Exceptions are classes, and you create your own by subclassing existing exceptions. It is strongly recommended (but not required) that you subclass `Exception`, which is the base class that all built-in exceptions inherit from. Here I am defining `RomanError` (inherited from `Exception`) to act as the base class for all my other custom exceptions to follow. This is a matter of style; I could just as easily have inherited each individual exception from the `Exception` class directly. 

[![2](../images/callouts/2.png)](#roman.stage1.1.2) The `OutOfRangeError` and `NotIntegerError` exceptions will eventually be used by `toRoman` to flag various forms of invalid input, as specified in [`ToRomanBadInput`](testing_for_failure.html#roman.tobadinput.example "Example 13.3. Testing bad input to toRoman"). 

[![3](../images/callouts/3.png)](#roman.stage1.1.3) The `InvalidRomanNumeralError` exception will eventually be used by `fromRoman` to flag invalid input, as specified in [`FromRomanBadInput`](testing_for_failure.html#roman.frombadinput.example "Example 13.4. Testing bad input to fromRoman"). 

[![4](../images/callouts/4.png)](#roman.stage1.1.4) At this stage, you want to define the API of each of your functions, but you don't want to code them yet, so you stub them out using the Python reserved word [`pass`](../object_oriented_framework/defining_classes.html#fileinfo.class.simplest "Example 5.3. The Simplest Python Class"). 

Now for the big moment (drum roll please): you're finally going to run
the unit test against this stubby little module. At this point, every
test case should fail. In fact, if any test case passes in stage 1, you
should go back to `romantest.py` and re-evaluate why you coded a test so
useless that it passes with do-nothing functions.

Run `romantest1.py` with the `-v` command-line option, which will give
more verbose output so you can see exactly what's going on as each test
case runs. With any luck, your output should look like this:

### Example 14.2. Output of `romantest1.py` against `roman1.py`

    fromRoman should only accept uppercase input ... ERROR
    toRoman should always return uppercase ... ERROR
    fromRoman should fail with malformed antecedents ... FAIL
    fromRoman should fail with repeated pairs of numerals ... FAIL
    fromRoman should fail with too many repeated numerals ... FAIL
    fromRoman should give known result with known input ... FAIL
    toRoman should give known result with known input ... FAIL
    fromRoman(toRoman(n))==n for all n ... FAIL
    toRoman should fail with non-integer input ... FAIL
    toRoman should fail with negative input ... FAIL
    toRoman should fail with large input ... FAIL
    toRoman should fail with 0 input ... FAIL

    ======================================================================
    ERROR: fromRoman should only accept uppercase input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 154, in testFromRomanCase
        roman1.fromRoman(numeral.upper())
    AttributeError: 'None' object has no attribute 'upper'
    ======================================================================
    ERROR: toRoman should always return uppercase
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 148, in testToRomanCase
        self.assertEqual(numeral, numeral.upper())
    AttributeError: 'None' object has no attribute 'upper'
    ======================================================================
    FAIL: fromRoman should fail with malformed antecedents
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 133, in testMalformedAntecedent
        self.assertRaises(roman1.InvalidRomanNumeralError, roman1.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with repeated pairs of numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 127, in testRepeatedPairs
        self.assertRaises(roman1.InvalidRomanNumeralError, roman1.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with too many repeated numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 122, in testTooManyRepeatedNumerals
        self.assertRaises(roman1.InvalidRomanNumeralError, roman1.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 99, in testFromRomanKnownValues
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ======================================================================
    FAIL: toRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 93, in testToRomanKnownValues
        self.assertEqual(numeral, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: I != None
    ======================================================================
    FAIL: fromRoman(toRoman(n))==n for all n
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 141, in testSanity
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ======================================================================
    FAIL: toRoman should fail with non-integer input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 116, in testNonInteger
        self.assertRaises(roman1.NotIntegerError, roman1.toRoman, 0.5)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: NotIntegerError
    ======================================================================
    FAIL: toRoman should fail with negative input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 112, in testNegative
        self.assertRaises(roman1.OutOfRangeError, roman1.toRoman, -1)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError
    ======================================================================
    FAIL: toRoman should fail with large input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 104, in testTooLarge
        self.assertRaises(roman1.OutOfRangeError, roman1.toRoman, 4000)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError
    ======================================================================
    FAIL: toRoman should fail with 0 input                                 
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage1\romantest1.py", line 108, in testZero
        self.assertRaises(roman1.OutOfRangeError, roman1.toRoman, 0)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError                                        
    ----------------------------------------------------------------------
    Ran 12 tests in 0.040s                                                 

    FAILED (failures=10, errors=2)                                         



[![1](../images/callouts/1.png)](#roman.stage1.2.1) Running the script runs `unittest.main()`, which runs each test case, which is to say each method defined in each class within `romantest.py`. For each test case, it prints out the `doc string` of the method and whether that test passed or failed. As expected, none of the test cases passed. 

[![2](../images/callouts/2.png)](#roman.stage1.2.2) For each failed test case, `unittest` displays the trace information showing exactly what happened. In this case, the call to `assertRaises` (also called `failUnlessRaises`) raised an `AssertionError` because it was expecting `toRoman` to raise an `OutOfRangeError` and it didn't. 

[![3](../images/callouts/3.png)](#roman.stage1.2.3) After the detail, `unittest` displays a summary of how many tests were performed and how long it took. 

[![4](../images/callouts/4.png)](#roman.stage1.2.4) Overall, the unit test failed because at least one test case did not pass. When a test case doesn't pass, `unittest` distinguishes between failures and errors. A failure is a call to an `assertXYZ` method, like `assertEqual` or `assertRaises`, that fails because the asserted condition is not true or the expected exception was not raised. An error is any other sort of exception raised in the code you're testing or the unit test case itself. For instance, the `testFromRomanCase` method (“`fromRoman` should only accept uppercase input”) was an error, because the call to `numeral.upper()` raised an `AttributeError` exception, because `toRoman` was supposed to return a string but didn't. But `testZero` (“`toRoman` should fail with 0 input”) was a failure, because the call to `fromRoman` did not raise the `InvalidRomanNumeral` exception that `assertRaises` was looking for. 

  

