

14.3. `roman.py`, stage 3
-------------------------

Now that `toRoman` behaves correctly with good input (integers from `1`
to `3999`), it's time to make it behave correctly with bad input
(everything else).

### Example 14.6. `roman3.py`

This file is available in `py/roman/stage3/` in the examples directory.

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Convert to and from Roman numerals"""

    #Define exceptions
    class RomanError(Exception): pass
    class OutOfRangeError(RomanError): pass
    class NotIntegerError(RomanError): pass
    class InvalidRomanNumeralError(RomanError): pass

    #Define digit mapping
    romanNumeralMap = (('M',  1000),
                       ('CM', 900),
                       ('D',  500),
                       ('CD', 400),
                       ('C',  100),
                       ('XC', 90),
                       ('L',  50),
                       ('XL', 40),
                       ('X',  10),
                       ('IX', 9),
                       ('V',  5),
                       ('IV', 4),
                       ('I',  1))

    def toRoman(n):
        """convert integer to Roman numeral"""
        if not (0 < n < 4000):                                             
            raise OutOfRangeError, "number out of range (must be 1..3999)" 
        if int(n) <> n:                                                    
            raise NotIntegerError, "non-integers can not be converted"

        result = ""                                                        
        for numeral, integer in romanNumeralMap:
            while n >= integer:
                result += numeral
                n -= integer
        return result

    def fromRoman(s):
        """convert Roman numeral to integer"""
        pass



[![1](../images/callouts/1.png)](#roman.stage3.1.1) This is a nice Pythonic shortcut: multiple comparisons at once. This is equivalent to `if not ((0 < n) and (n < 4000))`, but it's much easier to read. This is the range check, and it should catch inputs that are too large, negative, or zero. 

[![2](../images/callouts/2.png)](#roman.stage3.1.2) You raise exceptions yourself with the `raise` statement. You can raise any of the built-in exceptions, or you can raise any of your custom exceptions that you've defined. The second parameter, the error message, is optional; if given, it is displayed in the traceback that is printed if the exception is never handled. 

[![3](../images/callouts/3.png)](#roman.stage3.1.3) This is the non-integer check. Non-integers can not be converted to Roman numerals. 

[![4](../images/callouts/4.png)](#roman.stage3.1.4) The rest of the function is unchanged. 

### Example 14.7. Watching `toRoman` handle bad input

    >>> import roman3
    >>> roman3.toRoman(4000)
    Traceback (most recent call last):
      File "<interactive input>", line 1, in ?
      File "roman3.py", line 27, in toRoman
        raise OutOfRangeError, "number out of range (must be 1..3999)"
    OutOfRangeError: number out of range (must be 1..3999)
    >>> roman3.toRoman(1.5)
    Traceback (most recent call last):
      File "<interactive input>", line 1, in ?
      File "roman3.py", line 29, in toRoman
        raise NotIntegerError, "non-integers can not be converted"
    NotIntegerError: non-integers can not be converted

### Example 14.8. Output of `romantest3.py` against `roman3.py`

    fromRoman should only accept uppercase input ... FAIL
    toRoman should always return uppercase ... ok
    fromRoman should fail with malformed antecedents ... FAIL
    fromRoman should fail with repeated pairs of numerals ... FAIL
    fromRoman should fail with too many repeated numerals ... FAIL
    fromRoman should give known result with known input ... FAIL
    toRoman should give known result with known input ... ok 
    fromRoman(toRoman(n))==n for all n ... FAIL
    toRoman should fail with non-integer input ... ok        
    toRoman should fail with negative input ... ok           
    toRoman should fail with large input ... ok
    toRoman should fail with 0 input ... ok



[![1](../images/callouts/1.png)](#roman.stage3.2.1) `toRoman` still passes the [known values test](testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues"), which is comforting. All the tests that passed in [stage 2](stage_2.html "14.2. roman.py, stage 2") still pass, so the latest code hasn't broken anything. 

[![2](../images/callouts/2.png)](#roman.stage3.2.2) More exciting is the fact that all of the [bad input tests](testing_for_failure.html#roman.tobadinput.example "Example 13.3. Testing bad input to toRoman") now pass. This test, `testNonInteger`, passes because of the `int(n) <> n` check. When a non-integer is passed to `toRoman`, the `int(n) <> n` check notices it and raises the `NotIntegerError` exception, which is what `testNonInteger` is looking for. 

[![3](../images/callouts/3.png)](#roman.stage3.2.3) This test, `testNegative`, passes because of the `not (0 < n < 4000)` check, which raises an `OutOfRangeError` exception, which is what `testNegative` is looking for. 

    ======================================================================
    FAIL: fromRoman should only accept uppercase input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 156, in testFromRomanCase
        roman3.fromRoman, numeral.lower())
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with malformed antecedents
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 133, in testMalformedAntecedent
        self.assertRaises(roman3.InvalidRomanNumeralError, roman3.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with repeated pairs of numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 127, in testRepeatedPairs
        self.assertRaises(roman3.InvalidRomanNumeralError, roman3.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with too many repeated numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 122, in testTooManyRepeatedNumerals
        self.assertRaises(roman3.InvalidRomanNumeralError, roman3.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 99, in testFromRomanKnownValues
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ======================================================================
    FAIL: fromRoman(toRoman(n))==n for all n
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage3\romantest3.py", line 141, in testSanity
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ----------------------------------------------------------------------
    Ran 12 tests in 0.401s

    FAILED (failures=6) 



[![1](../images/callouts/1.png)](#roman.stage3.3.1) You're down to 6 failures, and all of them involve `fromRoman`: the known values test, the three separate bad input tests, the case check, and the sanity check. That means that `toRoman` has passed all the tests it can pass by itself. (It's involved in the sanity check, but that also requires that `fromRoman` be written, which it isn't yet.) Which means that you must stop coding `toRoman` now. No tweaking, no twiddling, no extra checks “just in case”. Stop. Now. Back away from the keyboard. 


![Note](../images/note.png) 
The most important thing that comprehensive unit testing can tell you is when to stop coding. When all the unit tests for a function pass, stop coding the function. When all the unit tests for an entire module pass, stop coding the module. 

  

