

14.5. `roman.py`, stage 5
-------------------------

Now that `fromRoman` works properly with good input, it's time to fit in
the last piece of the puzzle: making it work properly with bad input.
That means finding a way to look at a string and determine if it's a
valid Roman numeral. This is inherently more difficult than [validating
numeric input](stage_3.html "14.3. roman.py, stage 3") in `toRoman`, but
you have a powerful tool at your disposal: regular expressions.

If you're not familiar with regular expressions and didn't read
[Chapter 7, *Regular
Expressions*](../regular_expressions/index.html "Chapter 7. Regular Expressions"),
now would be a good time.

As you saw in [Section 7.3, “Case Study: Roman
Numerals”](../regular_expressions/roman_numerals.html "7.3. Case Study: Roman Numerals"),
there are several simple rules for constructing a Roman numeral, using
the letters `M`, `D`, `C`, `L`, `X`, `V`, and `I`. Let's review the
rules:

1.  Characters are additive. `I` is `1`, `II` is `2`, and `III` is `3`.
    `VI` is `6` (literally, “`5` and `1`”), `VII` is `7`, and `VIII` is
    `8`.
2.  The tens characters (`I`, `X`, `C`, and `M`) can be repeated up to
    three times. At `4`, you need to subtract from the next highest
    fives character. You can't represent `4` as `IIII`; instead, it is
    represented as `IV` (“`1` less than `5`”). `40` is written as `XL`
    (“`10` less than `50`”), `41` as `XLI`, `42` as `XLII`, `43` as
    `XLIII`, and then `44` as `XLIV` (“`10` less than `50`, then `1`
    less than `5`”).
3.  Similarly, at `9`, you need to subtract from the next highest tens
    character: `8` is `VIII`, but `9` is `IX` (“`1` less than `10`”),
    not `VIIII` (since the `I` character can not be repeated four
    times). `90` is `XC`, `900` is `CM`.
4.  The fives characters can not be repeated. `10` is always represented
    as `X`, never as `VV`. `100` is always `C`, never `LL`.
5.  Roman numerals are always written highest to lowest, and read left
    to right, so order of characters matters very much. `DC` is `600`;
    `CD` is a completely different number (`400`, “`100` less than
    `500`”). `CI` is `101`; `IC` is not even a valid Roman numeral
    (because you can't subtract `1` directly from `100`; you would need
    to write it as `XCIX`, “`10` less than `100`, then `1` less than
    `10`”).

### Example 14.12. `roman5.py`

This file is available in `py/roman/stage5/` in the examples directory.

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

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

    #Define pattern to detect valid Roman numerals
    romanNumeralPattern = '^M?M?M?(CM CD D?C?C?C?)(XC XL L?X?X?X?)(IX IV V?I?I?I?)$' 

    def fromRoman(s):
        """convert Roman numeral to integer"""
        if not re.search(romanNumeralPattern, s):                                    
            raise InvalidRomanNumeralError, 'Invalid Roman numeral: %s' % s

        result = 0
        index = 0
        for numeral, integer in romanNumeralMap:
            while s[index:index+len(numeral)] == numeral:
                result += integer
                index += len(numeral)
        return result



[![1](../images/callouts/1.png)](#roman.stage5.3.1) This is just a continuation of the pattern you discussed in [Section 7.3, “Case Study: Roman Numerals”](../regular_expressions/roman_numerals.html "7.3. Case Study: Roman Numerals"). The tens places is either `XC` (`90`), `XL` (`40`), or an optional `L` followed by 0 to 3 optional `X` characters. The ones place is either `IX` (`9`), `IV` (`4`), or an optional `V` followed by 0 to 3 optional `I` characters. 

[![2](../images/callouts/2.png)](#roman.stage5.3.2) Having encoded all that logic into a regular expression, the code to check for invalid Roman numerals becomes trivial. If `re.search` returns an object, then the regular expression matched and the input is valid; otherwise, the input is invalid. 

At this point, you are allowed to be skeptical that that big ugly
regular expression could possibly catch all the types of invalid Roman
numerals. But don't take my word for it, look at the results:

### Example 14.13. Output of `romantest5.py` against `roman5.py`

    fromRoman should only accept uppercase input ... ok          
    toRoman should always return uppercase ... ok
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
    Ran 12 tests in 2.864s

    OK                                                           



[![1](../images/callouts/1.png)](#roman.stage5.4.1) One thing I didn't mention about regular expressions is that, by default, they are case-sensitive. Since the regular expression `romanNumeralPattern` was expressed in uppercase characters, the `re.search` check will reject any input that isn't completely uppercase. So the uppercase input test passes. 

[![2](../images/callouts/2.png)](#roman.stage5.4.2) More importantly, the bad input tests pass. For instance, the malformed antecedents test checks cases like `MCMC`. As you've seen, this does not match the regular expression, so `fromRoman` raises an `InvalidRomanNumeralError` exception, which is what the malformed antecedents test case is looking for, so the test passes. 

[![3](../images/callouts/3.png)](#roman.stage5.4.3) In fact, all the bad input tests pass. This regular expression catches everything you could think of when you made your test cases. 

[![4](../images/callouts/4.png)](#roman.stage5.4.4) And the anticlimax award of the year goes to the word “`OK`”, which is printed by the `unittest` module when all the tests pass. 


![Note](../images/note.png) 
When all of your tests pass, stop coding. 

  

