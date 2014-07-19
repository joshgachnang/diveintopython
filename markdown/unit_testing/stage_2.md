

14.2. `roman.py`, stage 2
-------------------------

Now that you have the framework of the `roman` module laid out, it's
time to start writing code and passing test cases.

### Example 14.3. `roman2.py`

This file is available in `py/roman/stage2/` in the examples directory.

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
        result = ""
        for numeral, integer in romanNumeralMap:
            while n >= integer:      
                result += numeral
                n -= integer
        return result

    def fromRoman(s):
        """convert Roman numeral to integer"""
        pass

<table>
<col width="50%" />
<col width="50%" />
<tbody>
<tr class="odd">
<td align="left"><a href="#roman.stage2.1.1"><img src="../images/callouts/1.png" alt="1" /></a></td>
<td align="left"><code class="varname">romanNumeralMap</code> is a tuple of tuples which defines three things:
<ol>
<li>The character representations of the most basic Roman numerals. Note that this is not just the single-character Roman numerals; you're also defining two-character pairs like <code class="literal">CM</code> (“one hundred less than one thousand”); this will make the <code class="function">toRoman</code> code simpler later.</li>
<li>The order of the Roman numerals. They are listed in descending value order, from <code class="literal">M</code> all the way down to <code class="literal">I</code>.</li>
<li>The value of each Roman numeral. Each inner tuple is a pair of <code class="literal">(numeral, value)</code>.</li>
</ol></td>
</tr>
<tr class="even">
<td align="left"><a href="#roman.stage2.1.2"><img src="../images/callouts/2.png" alt="2" /></a></td>
<td align="left">Here's where your rich data structure pays off, because you don't need any special logic to handle the subtraction rule. To convert to Roman numerals, you simply iterate through <code class="varname">romanNumeralMap</code> looking for the largest integer value less than or equal to the input. Once found, you add the Roman numeral representation to the end of the output, subtract the corresponding integer value from the input, lather, rinse, repeat.</td>
</tr>
</tbody>
</table>

### Example 14.4. How `toRoman` works

If you're not clear how `toRoman` works, add a `print` statement to the
end of the `while` loop:

            while n >= integer:
                result += numeral
                n -= integer
                print 'subtracting', integer, 'from input, adding', numeral, 'to output'

    >>> import roman2
    >>> roman2.toRoman(1424)
    subtracting 1000 from input, adding M to output
    subtracting 400 from input, adding CD to output
    subtracting 10 from input, adding X to output
    subtracting 10 from input, adding X to output
    subtracting 4 from input, adding IV to output
    'MCDXXIV'

So `toRoman` appears to work, at least in this manual spot check. But
will it pass the unit testing? Well no, not entirely.

### Example 14.5. Output of `romantest2.py` against `roman2.py`

Remember to run `romantest2.py` with the `-v` command-line flag to
enable verbose mode.

    fromRoman should only accept uppercase input ... FAIL
    toRoman should always return uppercase ... ok                  
    fromRoman should fail with malformed antecedents ... FAIL
    fromRoman should fail with repeated pairs of numerals ... FAIL
    fromRoman should fail with too many repeated numerals ... FAIL
    fromRoman should give known result with known input ... FAIL
    toRoman should give known result with known input ... ok       
    fromRoman(toRoman(n))==n for all n ... FAIL
    toRoman should fail with non-integer input ... FAIL            
    toRoman should fail with negative input ... FAIL
    toRoman should fail with large input ... FAIL
    toRoman should fail with 0 input ... FAIL



[![1](../images/callouts/1.png)](#roman.stage2.2.1) `toRoman` does, in fact, always return uppercase, because `romanNumeralMap` defines the Roman numeral representations as uppercase. So this test passes already. 

[![2](../images/callouts/2.png)](#roman.stage2.2.2) Here's the big news: this version of the `toRoman` function passes the [known values test](testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues"). Remember, it's not comprehensive, but it does put the function through its paces with a variety of good inputs, including inputs that produce every single-character Roman numeral, the largest possible input (`3999`), and the input that produces the longest possible Roman numeral (`3888`). At this point, you can be reasonably confident that the function works for any good input value you could throw at it. 

[![3](../images/callouts/3.png)](#roman.stage2.2.3) However, the function does not “work” for bad values; it fails every single [bad input test](testing_for_failure.html#roman.tobadinput.example "Example 13.3. Testing bad input to toRoman"). That makes sense, because you didn't include any checks for bad input. Those test cases look for specific exceptions to be raised (via `assertRaises`), and you're never raising them. You'll do that in the next stage. 

Here's the rest of the output of the unit test, listing the details of
all the failures. You're down to 10.

    ======================================================================
    FAIL: fromRoman should only accept uppercase input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 156, in testFromRomanCase
        roman2.fromRoman, numeral.lower())
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with malformed antecedents
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 133, in testMalformedAntecedent
        self.assertRaises(roman2.InvalidRomanNumeralError, roman2.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with repeated pairs of numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 127, in testRepeatedPairs
        self.assertRaises(roman2.InvalidRomanNumeralError, roman2.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should fail with too many repeated numerals
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 122, in testTooManyRepeatedNumerals
        self.assertRaises(roman2.InvalidRomanNumeralError, roman2.fromRoman, s)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ======================================================================
    FAIL: fromRoman should give known result with known input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 99, in testFromRomanKnownValues
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ======================================================================
    FAIL: fromRoman(toRoman(n))==n for all n
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 141, in testSanity
        self.assertEqual(integer, result)
      File "c:\python21\lib\unittest.py", line 273, in failUnlessEqual
        raise self.failureException, (msg or '%s != %s' % (first, second))
    AssertionError: 1 != None
    ======================================================================
    FAIL: toRoman should fail with non-integer input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 116, in testNonInteger
        self.assertRaises(roman2.NotIntegerError, roman2.toRoman, 0.5)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: NotIntegerError
    ======================================================================
    FAIL: toRoman should fail with negative input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 112, in testNegative
        self.assertRaises(roman2.OutOfRangeError, roman2.toRoman, -1)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError
    ======================================================================
    FAIL: toRoman should fail with large input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 104, in testTooLarge
        self.assertRaises(roman2.OutOfRangeError, roman2.toRoman, 4000)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError
    ======================================================================
    FAIL: toRoman should fail with 0 input
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage2\romantest2.py", line 108, in testZero
        self.assertRaises(roman2.OutOfRangeError, roman2.toRoman, 0)
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: OutOfRangeError
    ----------------------------------------------------------------------
    Ran 12 tests in 0.320s

    FAILED (failures=10)

  

