

14.4. `roman.py`, stage 4
-------------------------

Now that `toRoman` is done, it's time to start coding `fromRoman`.
Thanks to the rich data structure that maps individual Roman numerals to
integer values, this is no more difficult than the `toRoman` function.

### Example 14.9. `roman4.py`

This file is available in `py/roman/stage4/` in the examples directory.

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

    # toRoman function omitted for clarity (it hasn't changed)

    def fromRoman(s):
        """convert Roman numeral to integer"""
        result = 0
        index = 0
        for numeral, integer in romanNumeralMap:
            while s[index:index+len(numeral)] == numeral: 
                result += integer
                index += len(numeral)
        return result



[![1](../images/callouts/1.png)](#roman.stage4.1.1) The pattern here is the same as [`toRoman`](stage_2.html#roman.stage2.example "Example 14.3. roman2.py"). You iterate through your Roman numeral data structure (a tuple of tuples), and instead of matching the highest integer values as often as possible, you match the “highest” Roman numeral character strings as often as possible. 

### Example 14.10. How `fromRoman` works

If you're not clear how `fromRoman` works, add a `print` statement to
the end of the `while` loop:

            while s[index:index+len(numeral)] == numeral:
                result += integer
                index += len(numeral)
                print 'found', numeral, 'of length', len(numeral), ', adding', integer

    >>> import roman4
    >>> roman4.fromRoman('MCMLXXII')
    found M , of length 1, adding 1000
    found CM , of length 2, adding 900
    found L , of length 1, adding 50
    found X , of length 1, adding 10
    found X , of length 1, adding 10
    found I , of length 1, adding 1
    found I , of length 1, adding 1
    1972

### Example 14.11. Output of `romantest4.py` against `roman4.py`

    fromRoman should only accept uppercase input ... FAIL
    toRoman should always return uppercase ... ok
    fromRoman should fail with malformed antecedents ... FAIL
    fromRoman should fail with repeated pairs of numerals ... FAIL
    fromRoman should fail with too many repeated numerals ... FAIL
    fromRoman should give known result with known input ... ok 
    toRoman should give known result with known input ... ok
    fromRoman(toRoman(n))==n for all n ... ok                  
    toRoman should fail with non-integer input ... ok
    toRoman should fail with negative input ... ok
    toRoman should fail with large input ... ok
    toRoman should fail with 0 input ... ok



[![1](../images/callouts/1.png)](#roman.stage4.2.1) Two pieces of exciting news here. The first is that `fromRoman` works for good input, at least for all the [known values](testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues") you test. 

[![2](../images/callouts/2.png)](#roman.stage4.2.2) The second is that the [sanity check](testing_for_sanity.html#roman.sanity.example "Example 13.5. Testing toRoman against fromRoman") also passed. Combined with the known values tests, you can be reasonably sure that both `toRoman` and `fromRoman` work properly for all possible good values. (This is not guaranteed; it is theoretically possible that `toRoman` has a bug that produces the wrong Roman numeral for some particular set of inputs, *and* that `fromRoman` has a reciprocal bug that produces the same wrong integer values for exactly that set of Roman numerals that `toRoman` generated incorrectly. Depending on your application and your requirements, this possibility may bother you; if so, write more comprehensive test cases until it doesn't bother you.) 

    ======================================================================
    FAIL: fromRoman should only accept uppercase input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage4\romantest4.py", line 156, in testFromRomanCase
        roman4.fromRoman, numeral.lower())
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with malformed antecedents
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage4\romantest4.py", line 133, in testMalformedAntecedent
        self.assertRaises(roman4.InvalidRomanNumeralError, roman4.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with repeated pairs of numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage4\romantest4.py", line 127, in testRepeatedPairs
        self.assertRaises(roman4.InvalidRomanNumeralError, roman4.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with too many repeated numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage4\romantest4.py", line 122, in testTooManyRepeatedNumerals
        self.assertRaises(roman4.InvalidRomanNumeralError, roman4.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ----------------------------------------------------------------------
    Ran 12 tests in 1.222s

    FAILED (failures=4)

  

