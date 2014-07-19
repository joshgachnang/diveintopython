

Chapter 15. Refactoring
-----------------------

-   [15.1. Handling bugs](index.html#roman.bugs)
-   [15.2. Handling changing
    requirements](handling_changing_requirements.html)
-   [15.3. Refactoring](refactoring.html)
-   [15.4. Postscript](postscript.html)
-   [15.5. Summary](summary.html)

15.1. Handling bugs
-------------------

Despite your best efforts to write comprehensive unit tests, bugs
happen. What do I mean by “bug”? A bug is a test case you haven't
written yet.

### Example 15.1. The bug

    >>> import roman5
    >>> roman5.fromRoman("") 
    0



[![1](../images/callouts/1.png)](#roman.bugs.1.1) Remember in the [previous section](../unit_testing/stage_5.html "14.5. roman.py, stage 5") when you kept seeing that an empty string would match the regular expression you were using to check for valid Roman numerals? Well, it turns out that this is still true for the final version of the regular expression. And that's a bug; you want an empty string to raise an `InvalidRomanNumeralError` exception just like any other sequence of characters that don't represent a valid Roman numeral. 

After reproducing the bug, and before fixing it, you should write a test
case that fails, thus illustrating the bug.

### Example 15.2. Testing for the bug (`romantest61.py`)

    class FromRomanBadInput(unittest.TestCase):                                      

        # previous test cases omitted for clarity (they haven't changed)

        def testBlank(self):
            """fromRoman should fail with blank string"""
            self.assertRaises(roman.InvalidRomanNumeralError, roman.fromRoman, "") 



[![1](../images/callouts/1.png)](#roman.bugs.2.1) Pretty simple stuff here. Call `fromRoman` with an empty string and make sure it raises an `InvalidRomanNumeralError` exception. The hard part was finding the bug; now that you know about it, testing for it is the easy part. 

Since your code has a bug, and you now have a test case that tests this
bug, the test case will fail:

### Example 15.3. Output of `romantest61.py` against `roman61.py`

    fromRoman should only accept uppercase input ... ok
    toRoman should always return uppercase ... ok
    fromRoman should fail with blank string ... FAIL
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

    ======================================================================
    FAIL: fromRoman should fail with blank string
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "C:\docbook\dip\py\roman\stage6\romantest61.py", line 137, in testBlank
        self.assertRaises(roman61.InvalidRomanNumeralError, roman61.fromRoman, "")
      File "c:\python21\lib\unittest.py", line 266, in failUnlessRaises
        raise self.failureException, excName
    AssertionError: InvalidRomanNumeralError
    ----------------------------------------------------------------------
    Ran 13 tests in 2.864s

    FAILED (failures=1)

*Now* you can fix the bug.

### Example 15.4. Fixing the bug (`roman62.py`)

This file is available in `py/roman/stage6/` in the examples directory.

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



[![1](../images/callouts/1.png)](#roman.bugs.4.1) Only two lines of code are required: an explicit check for an empty string, and a `raise` statement. 

### Example 15.5. Output of `romantest62.py` against `roman62.py`

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
    Ran 13 tests in 2.834s

    OK 



[![1](../images/callouts/1.png)](#roman.bugs.5.1) The blank string test case now passes, so the bug is fixed. 

[![2](../images/callouts/2.png)](#roman.bugs.5.2) All the other test cases still pass, which means that this bug fix didn't break anything else. Stop coding. 

Coding this way does not make fixing bugs any easier. Simple bugs (like
this one) require simple test cases; complex bugs will require complex
test cases. In a testing-centric environment, it may *seem* like it
takes longer to fix a bug, since you need to articulate in code exactly
what the bug is (to write the test case), then fix the bug itself. Then
if the test case doesn't pass right away, you need to figure out whether
the fix was wrong, or whether the test case itself has a bug in it.
However, in the long run, this back-and-forth between test code and code
tested pays for itself, because it makes it more likely that bugs are
fixed correctly the first time. Also, since you can easily re-run *all*
the test cases along with your new one, you are much less likely to
break old code when fixing new code. Today's unit test is tomorrow's
regression test.

  

