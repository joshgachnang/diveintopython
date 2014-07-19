

18.4. Optimizing Dictionary Lookups
-----------------------------------

The second step of the Soundex algorithm is to convert characters to
digits in a specific pattern. What's the best way to do this?

The most obvious solution is to define a dictionary with individual
characters as keys and their corresponding digits as values, and do
dictionary lookups on each character. This is what we have in
`soundex/stage1/soundex1c.py` (the current best result so far):

    charToSoundex = {"A": "9",
                     "B": "1",
                     "C": "2",
                     "D": "3",
                     "E": "9",
                     "F": "1",
                     "G": "2",
                     "H": "9",
                     "I": "9",
                     "J": "2",
                     "K": "2",
                     "L": "4",
                     "M": "5",
                     "N": "5",
                     "O": "9",
                     "P": "1",
                     "Q": "2",
                     "R": "6",
                     "S": "2",
                     "T": "3",
                     "U": "9",
                     "V": "1",
                     "W": "9",
                     "X": "2",
                     "Y": "9",
                     "Z": "2"}

    def soundex(source):
        # ... input check omitted for brevity ...
        source = source[0].upper() + source[1:]
        digits = source[0]
        for s in source[1:]:
            s = s.upper()
            digits += charToSoundex[s]

You timed `soundex1c.py` already; this is how it performs:

    C:\samples\soundex\stage1>python soundex1c.py
    Woo             W000 14.5341678901
    Pilgrim         P426 19.2650071448
    Flingjingwaller F452 30.1003563302

This code is straightforward, but is it the best solution? Calling
`upper()` on each individual character seems inefficient; it would
probably be better to call `upper()` once on the entire string.

Then there's the matter of incrementally building the `digits` string.
Incrementally building strings like this is horribly inefficient;
internally, the Python interpreter needs to create a new string each
time through the loop, then discard the old one.

Python is good at lists, though. It can treat a string as a list of
characters automatically. And lists are easy to combine into strings
again, using the string method `join()`.

Here is `soundex/stage2/soundex2a.py`, which converts letters to digits
by using ↦ and `lambda`:

    def soundex(source):
        # ...
        source = source.upper()
        digits = source[0] + "".join(map(lambda c: charToSoundex[c], source[1:]))

Surprisingly, `soundex2a.py` is not faster:

    C:\samples\soundex\stage2>python soundex2a.py
    Woo             W000 15.0097526362
    Pilgrim         P426 19.254806407
    Flingjingwaller F452 29.3790847719

The overhead of the anonymous `lambda` function kills any performance
you gain by dealing with the string as a list of characters.

`soundex/stage2/soundex2b.py` uses a list comprehension instead of ↦ and
`lambda`:

        source = source.upper()
        digits = source[0] + "".join([charToSoundex[c] for c in source[1:]])

Using a list comprehension in `soundex2b.py` is faster than using ↦ and
`lambda` in `soundex2a.py`, but still not faster than the original code
(incrementally building a string in `soundex1c.py`):

    C:\samples\soundex\stage2>python soundex2b.py
    Woo             W000 13.4221324219
    Pilgrim         P426 16.4901234654
    Flingjingwaller F452 25.8186157738

It's time for a radically different approach. Dictionary lookups are a
general purpose tool. Dictionary keys can be any length string (or many
other data types), but in this case we are only dealing with
single-character keys *and* single-character values. It turns out that
Python has a specialized function for handling exactly this situation:
the `string.maketrans` function.

This is `soundex/stage2/soundex2c.py`:

    allChar = string.uppercase + string.lowercase
    charToSoundex = string.maketrans(allChar, "91239129922455912623919292" * 2)
    def soundex(source):
        # ...
        digits = source[0].upper() + source[1:].translate(charToSoundex)

What the heck is going on here? `string.maketrans` creates a translation
matrix between two strings: the first argument and the second argument.
In this case, the first argument is the string
`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`, and the second
argument is the string
`9123912992245591262391929291239129922455912623919292`. See the pattern?
It's the same conversion pattern we were setting up longhand with a
dictionary. A maps to 9, B maps to 1, C maps to 2, and so forth. But
it's not a dictionary; it's a specialized data structure that you can
access using the string method `translate`, which translates each
character into the corresponding digit, according to the matrix defined
by `string.maketrans`.

`timeit` shows that `soundex2c.py` is significantly faster than defining
a dictionary and looping through the input and building the output
incrementally:

    C:\samples\soundex\stage2>python soundex2c.py
    Woo             W000 11.437645008
    Pilgrim         P426 13.2825062962
    Flingjingwaller F452 18.5570110168

You're not going to get much better than that. Python has a specialized
function that does exactly what you want to do; use it and move on.

### Example 18.4. Best Result So Far: `soundex/stage2/soundex2c.py`

    import string, re

    allChar = string.uppercase + string.lowercase
    charToSoundex = string.maketrans(allChar, "91239129922455912623919292" * 2)
    isOnlyChars = re.compile('^[A-Za-z]+$').search

    def soundex(source):
        if not isOnlyChars(source):
            return "0000"
        digits = source[0].upper() + source[1:].translate(charToSoundex)
        digits2 = digits[0]
        for d in digits[1:]:
            if digits2[-1] != d:
                digits2 += d
        digits3 = re.sub('9', '', digits2)
        while len(digits3) < 4:
            digits3 += "0"
        return digits3[:4]

    if __name__ == '__main__':
        from timeit import Timer
        names = ('Woo', 'Pilgrim', 'Flingjingwaller')
        for name in names:
            statement = "soundex('%s')" % name
            t = Timer(statement, "from __main__ import soundex")
            print name.ljust(15), soundex(name), min(t.repeat())

  

