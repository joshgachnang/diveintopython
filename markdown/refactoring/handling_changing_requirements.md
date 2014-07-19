

15.2. Handling changing requirements
------------------------------------

Despite your best efforts to pin your customers to the ground and
extract exact requirements from them on pain of horrible nasty things
involving scissors and hot wax, requirements will change. Most customers
don't know what they want until they see it, and even if they do, they
aren't that good at articulating what they want precisely enough to be
useful. And even if they do, they'll want more in the next release
anyway. So be prepared to update your test cases as requirements change.

Suppose, for instance, that you wanted to expand the range of the Roman
numeral conversion functions. Remember [the
rule](../unit_testing/diving_in.html "13.2. Diving in") that said that
no character could be repeated more than three times? Well, the Romans
were willing to make an exception to that rule by having 4 `M`
characters in a row to represent `4000`. If you make this change, you'll
be able to expand the range of convertible numbers from `1..3999` to
`1..4999`. But first, you need to make some changes to the test cases.

### Example 15.6. Modifying test cases for new requirements (`romantest71.py`)

This file is available in `py/roman/stage7/` in the examples directory.

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    import roman71
    import unittest

    class KnownValues(unittest.TestCase):
        knownValues = ( (1, 'I'),
                        (2, 'II'),
                        (3, 'III'),
                        (4, 'IV'),
                        (5, 'V'),
                        (6, 'VI'),
                        (7, 'VII'),
                        (8, 'VIII'),
                        (9, 'IX'),
                        (10, 'X'),
                        (50, 'L'),
                        (100, 'C'),
                        (500, 'D'),
                        (1000, 'M'),
                        (31, 'XXXI'),
                        (148, 'CXLVIII'),
                        (294, 'CCXCIV'),
                        (312, 'CCCXII'),
                        (421, 'CDXXI'),
                        (528, 'DXXVIII'),
                        (621, 'DCXXI'),
                        (782, 'DCCLXXXII'),
                        (870, 'DCCCLXX'),
                        (941, 'CMXLI'),
                        (1043, 'MXLIII'),
                        (1110, 'MCX'),
                        (1226, 'MCCXXVI'),
                        (1301, 'MCCCI'),
                        (1485, 'MCDLXXXV'),
                        (1509, 'MDIX'),
                        (1607, 'MDCVII'),
                        (1754, 'MDCCLIV'),
                        (1832, 'MDCCCXXXII'),
                        (1993, 'MCMXCIII'),
                        (2074, 'MMLXXIV'),
                        (2152, 'MMCLII'),
                        (2212, 'MMCCXII'),
                        (2343, 'MMCCCXLIII'),
                        (2499, 'MMCDXCIX'),
                        (2574, 'MMDLXXIV'),
                        (2646, 'MMDCXLVI'),
                        (2723, 'MMDCCXXIII'),
                        (2892, 'MMDCCCXCII'),
                        (2975, 'MMCMLXXV'),
                        (3051, 'MMMLI'),
                        (3185, 'MMMCLXXXV'),
                        (3250, 'MMMCCL'),
                        (3313, 'MMMCCCXIII'),
                        (3408, 'MMMCDVIII'),
                        (3501, 'MMMDI'),
                        (3610, 'MMMDCX'),
                        (3743, 'MMMDCCXLIII'),
                        (3844, 'MMMDCCCXLIV'),
                        (3888, 'MMMDCCCLXXXVIII'),
                        (3940, 'MMMCMXL'),
                        (3999, 'MMMCMXCIX'),
                        (4000, 'MMMM'),                                       
                        (4500, 'MMMMD'),
                        (4888, 'MMMMDCCCLXXXVIII'),
                        (4999, 'MMMMCMXCIX'))

        def testToRomanKnownValues(self):
            """toRoman should give known result with known input"""
            for integer, numeral in self.knownValues:
                result = roman71.toRoman(integer)
                self.assertEqual(numeral, result)

        def testFromRomanKnownValues(self):
            """fromRoman should give known result with known input"""
            for integer, numeral in self.knownValues:
                result = roman71.fromRoman(numeral)
                self.assertEqual(integer, result)

    class ToRomanBadInput(unittest.TestCase):
        def testTooLarge(self):
            """toRoman should fail with large input"""
            self.assertRaises(roman71.OutOfRangeError, roman71.toRoman, 5000) 

        def testZero(self):
            """toRoman should fail with 0 input"""
            self.assertRaises(roman71.OutOfRangeError, roman71.toRoman, 0)

        def testNegative(self):
            """toRoman should fail with negative input"""
            self.assertRaises(roman71.OutOfRangeError, roman71.toRoman, -1)

        def testNonInteger(self):
            """toRoman should fail with non-integer input"""
            self.assertRaises(roman71.NotIntegerError, roman71.toRoman, 0.5)

    class FromRomanBadInput(unittest.TestCase):
        def testTooManyRepeatedNumerals(self):
            """fromRoman should fail with too many repeated numerals"""
            for s in ('MMMMM', 'DD', 'CCCC', 'LL', 'XXXX', 'VV', 'IIII'):     
                self.assertRaises(roman71.InvalidRomanNumeralError, roman71.fromRoman, s)

        def testRepeatedPairs(self):
            """fromRoman should fail with repeated pairs of numerals"""
            for s in ('CMCM', 'CDCD', 'XCXC', 'XLXL', 'IXIX', 'IVIV'):
                self.assertRaises(roman71.InvalidRomanNumeralError, roman71.fromRoman, s)

        def testMalformedAntecedent(self):
            """fromRoman should fail with malformed antecedents"""
            for s in ('IIMXCC', 'VX', 'DCM', 'CMM', 'IXIV',
                      'MCMC', 'XCX', 'IVI', 'LM', 'LD', 'LC'):
                self.assertRaises(roman71.InvalidRomanNumeralError, roman71.fromRoman, s)

        def testBlank(self):
            """fromRoman should fail with blank string"""
            self.assertRaises(roman71.InvalidRomanNumeralError, roman71.fromRoman, "")

    class SanityCheck(unittest.TestCase):
        def testSanity(self):
            """fromRoman(toRoman(n))==n for all n"""
            for integer in range(1, 5000):                                    
                numeral = roman71.toRoman(integer)
                result = roman71.fromRoman(numeral)
                self.assertEqual(integer, result)

    class CaseCheck(unittest.TestCase):
        def testToRomanCase(self):
            """toRoman should always return uppercase"""
            for integer in range(1, 5000):
                numeral = roman71.toRoman(integer)
                self.assertEqual(numeral, numeral.upper())

        def testFromRomanCase(self):
            """fromRoman should only accept uppercase input"""
            for integer in range(1, 5000):
                numeral = roman71.toRoman(integer)
                roman71.fromRoman(numeral.upper())
                self.assertRaises(roman71.InvalidRomanNumeralError,
                                  roman71.fromRoman, numeral.lower())

    if __name__ == "__main__":
        unittest.main()



[![1](../images/callouts/1.png)](#roman.change.1.1) The existing known values don't change (they're all still reasonable values to test), but you need to add a few more in the `4000` range. Here I've included `4000` (the shortest), `4500` (the second shortest), `4888` (the longest), and `4999` (the largest). 

[![2](../images/callouts/2.png)](#roman.change.1.2) The definition of “large input” has changed. This test used to call `toRoman` with `4000` and expect an error; now that `4000-4999` are good values, you need to bump this up to `5000`. 

[![3](../images/callouts/3.png)](#roman.change.1.3) The definition of “too many repeated numerals” has also changed. This test used to call `fromRoman` with `'MMMM'` and expect an error; now that `MMMM` is considered a valid Roman numeral, you need to bump this up to `'MMMMM'`. 

[![4](../images/callouts/4.png)](#roman.change.1.4) The sanity check and case checks loop through every number in the range, from `1` to `3999`. Since the range has now expanded, these `for` loops need to be updated as well to go up to `4999`. 

Now your test cases are up to date with the new requirements, but your
code is not, so you expect several of the test cases to fail.

### Example 15.7. Output of `romantest71.py` against `roman71.py`

    fromRoman should only accept uppercase input ... ERROR        
    toRoman should always return uppercase ... ERROR
    fromRoman should fail with blank string ... ok
    fromRoman should fail with malformed antecedents ... ok
    fromRoman should fail with repeated pairs of numerals ... ok
    fromRoman should fail with too many repeated numerals ... ok
    fromRoman should give known result with known input ... ERROR 
    toRoman should give known result with known input ... ERROR   
    fromRoman(toRoman(n))==n for all n ... ERROR                  
    toRoman should fail with non-integer input ... ok
    toRoman should fail with negative input ... ok
    toRoman should fail with large input ... ok
    toRoman should fail with 0 input ... ok



[![1](../images/callouts/1.png)](#roman.change.2.1) Our case checks now fail because they loop from `1` to `4999`, but `toRoman` only accepts numbers from `1` to `3999`, so it will fail as soon the test case hits `4000`. 

[![2](../images/callouts/2.png)](#roman.change.2.2) The `fromRoman` known values test will fail as soon as it hits `'MMMM'`, because `fromRoman` still thinks this is an invalid Roman numeral. 

[![3](../images/callouts/3.png)](#roman.change.2.3) The `toRoman` known values test will fail as soon as it hits `4000`, because `toRoman` still thinks this is out of range. 

[![4](../images/callouts/4.png)](#roman.change.2.4) The sanity check will also fail as soon as it hits `4000`, because `toRoman` still thinks this is out of range. 

    ======================================================================
    ERROR: fromRoman should only accept uppercase input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage7\romantest71.py", line 161, in testFromRomanCase
        numeral = roman71.toRoman(integer)
      File "roman71.py", line 28, in toRoman
        raise OutOfRangeError, "number out of range (must be 1..3999)"
    OutOfRangeError: number out of range (must be 1..3999)
    ======================================================================
    ERROR: toRoman should always return uppercase
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage7\romantest71.py", line 155, in testToRomanCase
        numeral = roman71.toRoman(integer)
      File "roman71.py", line 28, in toRoman
        raise OutOfRangeError, "number out of range (must be 1..3999)"
    OutOfRangeError: number out of range (must be 1..3999)
    ======================================================================
    ERROR: fromRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage7\romantest71.py", line 102, in testFromRomanKnownValues
        result = roman71.fromRoman(numeral)
      File "roman71.py", line 47, in fromRoman
        raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s
    InvalidRomanNumeralError: Invalid Roman numeral: MMMM
    ======================================================================
    ERROR: toRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage7\romantest71.py", line 96, in testToRomanKnownValues
        result = roman71.toRoman(integer)
      File "roman71.py", line 28, in toRoman
        raise OutOfRangeError, "number out of range (must be 1..3999)"
    OutOfRangeError: number out of range (must be 1..3999)
    ======================================================================
    ERROR: fromRoman(toRoman(n))==n for all n
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage7\romantest71.py", line 147, in testSanity
        numeral = roman71.toRoman(integer)
      File "roman71.py", line 28, in toRoman
        raise OutOfRangeError, "number out of range (must be 1..3999)"
    OutOfRangeError: number out of range (must be 1..3999)
    ----------------------------------------------------------------------
    Ran 13 tests in 2.213s

    FAILED (errors=5)

Now that you have test cases that fail due to the new requirements, you
can think about fixing the code to bring it in line with the test cases.
(One thing that takes some getting used to when you first start coding
unit tests is that the code being tested is never “ahead” of the test
cases. While it's behind, you still have some work to do, and as soon as
it catches up to the test cases, you stop coding.)

### Example 15.8. Coding the new requirements (`roman72.py`)

This file is available in `py/roman/stage7/` in the examples directory.

    """Convert to and from Roman numerals"""
    import re

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
        if not (0 < n < 5000):                                                         
            raise OutOfRangeError, "number out of range (must be 1..4999)"
        if int(n) <> n:
            raise NotIntegerError, "non-integers can not be converted"

        result = ""
        for numeral, integer in romanNumeralMap:
            while n >= integer:
                result += numeral
                n -= integer
        return result

    #Define pattern to detect valid Roman numerals
    romanNumeralPattern = '^M?M?M?M?(CM CD D?C?C?C?)(XC XL L?X?X?X?)(IX IV V?I?I?I?)$' 

    def fromRoman(s):
        """convert Roman numeral to integer"""
        if not s:
            raise InvalidRomanNumeralError, 'Input can not be blank'
        if not re.search(romanNumeralPattern, s):
            raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s

        result = 0
        index = 0
        for numeral, integer in romanNumeralMap:
            while s[index:index+len(numeral)] == numeral:
                result += integer
                index += len(numeral)
        return result



[![1](../images/callouts/1.png)](#roman.change.3.1) `toRoman` only needs one small change, in the range check. Where you used to check `0 < n < 4000`, you now check `0 < n < 5000`. And you change the error message that you `raise` to reflect the new acceptable range (`1..4999` instead of `1..3999`). You don't need to make any changes to the rest of the function; it handles the new cases already. (It merrily adds `'M'` for each thousand that it finds; given `4000`, it will spit out `'MMMM'`. The only reason it didn't do this before is that you explicitly stopped it with the range check.) 

[![2](../images/callouts/2.png)](#roman.change.3.2) You don't need to make any changes to `fromRoman` at all. The only change is to `romanNumeralPattern`; if you look closely, you'll notice that you added another optional `M` in the first section of the regular expression. This will allow up to 4 `M` characters instead of 3, meaning you will allow the Roman numeral equivalents of `4999` instead of `3999`. The actual `fromRoman` function is completely general; it just looks for repeated Roman numeral characters and adds them up, without caring how many times they repeat. The only reason it didn't handle `'MMMM'` before is that you explicitly stopped it with the regular expression pattern matching. 

You may be skeptical that these two small changes are all that you need.
Hey, don't take my word for it; see for yourself:

### Example 15.9. Output of `romantest72.py` against `roman72.py`

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

    ----------------------------------------------------------------------
    Ran 13 tests in 3.685s

    OK 



[![1](../images/callouts/1.png)](#roman.change.4.1) All the test cases pass. Stop coding. 

Comprehensive unit testing means never having to rely on a programmer
who says “Trust me.”

  

