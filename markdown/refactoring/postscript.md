

15.4. Postscript
----------------

A clever reader read the [previous
section](refactoring.html "15.3. Refactoring") and took it to the next
level. The biggest headache (and performance drain) in the program as it
is currently written is the regular expression, which is required
because you have no other way of breaking down a Roman numeral. But
there's only 5000 of them; why don't you just build a lookup table once,
then simply read that? This idea gets even better when you realize that
you don't need to use regular expressions at all. As you build the
lookup table for converting integers to Roman numerals, you can build
the reverse lookup table to convert Roman numerals to integers.

And best of all, he already had a complete set of unit tests. He changed
over half the code in the module, but the unit tests stayed the same, so
he could prove that his code worked just as well as the original.

### Example 15.17. `roman9.py`

This file is available in `py/roman/stage9/` in the examples directory.

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    #Define exceptions
    class RomanError(Exception): pass
    class OutOfRangeError(RomanError): pass
    class NotIntegerError(RomanError): pass
    class InvalidRomanNumeralError(RomanError): pass

    #Roman numerals must be less than 5000
    MAX_ROMAN_NUMERAL = 4999

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

    #Create tables for fast conversion of roman numerals.
    #See fillLookupTables() below.
    toRomanTable = [ None ]  # Skip an index since Roman numerals have no zero
    fromRomanTable = {}

    def toRoman(n):
        """convert integer to Roman numeral"""
        if not (0 < n <= MAX_ROMAN_NUMERAL):
            raise OutOfRangeError, "number out of range (must be 1..%s)" % MAX_ROMAN_NUMERAL
        if int(n) <> n:
            raise NotIntegerError, "non-integers can not be converted"
        return toRomanTable[n]

    def fromRoman(s):
        """convert Roman numeral to integer"""
        if not s:
            raise InvalidRomanNumeralError, "Input can not be blank"
        if not fromRomanTable.has_key(s):
            raise InvalidRomanNumeralError, "Invalid Roman numeral: %s" % s
        return fromRomanTable[s]

    def toRomanDynamic(n):
        """convert integer to Roman numeral using dynamic programming"""
        result = ""
        for numeral, integer in romanNumeralMap:
            if n >= integer:
                result = numeral
                n -= integer
                break
        if n > 0:
            result += toRomanTable[n]
        return result

    def fillLookupTables():
        """compute all the possible roman numerals"""
        #Save the values in two global tables to convert to and from integers.
        for integer in range(1, MAX_ROMAN_NUMERAL + 1):
            romanNumber = toRomanDynamic(integer)
            toRomanTable.append(romanNumber)
            fromRomanTable[romanNumber] = integer

    fillLookupTables()

So how fast is it?

### Example 15.18. Output of `romantest9.py` against `roman9.py`


    .............
    ----------------------------------------------------------------------
    Ran 13 tests in 0.791s

    OK

Remember, the best performance you ever got in the original version was
13 tests in 3.315 seconds. Of course, it's not entirely a fair
comparison, because this version will take longer to import (when it
fills the lookup tables). But since import is only done once, this is
negligible in the long run.

The moral of the story?

-   Simplicity is a virtue.
-   Especially when regular expressions are involved.
-   And unit tests can give you the confidence to do large-scale
    refactoring... even if you didn't write the original code.

  

