

18.3. Optimizing Regular Expressions
------------------------------------

The first thing the Soundex function checks is whether the input is a
non-empty string of letters. What's the best way to do this?

If you answered “regular expressions”, go sit in the corner and
contemplate your bad instincts. Regular expressions are almost never the
right answer; they should be avoided whenever possible. Not only for
performance reasons, but simply because they're difficult to debug and
maintain. Also for performance reasons.

This code fragment from `soundex/stage1/soundex1a.py` checks whether the
function argument `source` is a word made entirely of letters, with at
least one letter (not the empty string):

        allChars = string.uppercase + string.lowercase
        if not re.search('^[%s]+$' % allChars, source):
            return "0000"

How does `soundex1a.py` perform? For convenience, the `__main__` section
of the script contains this code that calls the `timeit` module, sets up
a timing test with three different names, tests each name three times,
and displays the minimum time for each:

    if __name__ == '__main__':
        from timeit import Timer
        names = ('Woo', 'Pilgrim', 'Flingjingwaller')
        for name in names:
            statement = "soundex('%s')" % name
            t = Timer(statement, "from __main__ import soundex")
            print name.ljust(15), soundex(name), min(t.repeat())

So how does `soundex1a.py` perform with this regular expression?

    C:\samples\soundex\stage1>python soundex1a.py
    Woo             W000 19.3356647283
    Pilgrim         P426 24.0772053431
    Flingjingwaller F452 35.0463220884

As you might expect, the algorithm takes significantly longer when
called with longer names. There will be a few things we can do to narrow
that gap (make the function take less relative time for longer input),
but the nature of the algorithm dictates that it will never run in
constant time.

The other thing to keep in mind is that we are testing a representative
sample of names. `Woo` is a kind of trivial case, in that it gets
shorted down to a single letter and then padded with zeros. `Pilgrim` is
a normal case, of average length and a mixture of significant and
ignored letters. `Flingjingwaller` is extraordinarily long and contains
consecutive duplicates. Other tests might also be helpful, but this hits
a good range of different cases.

So what about that regular expression? Well, it's inefficient. Since the
expression is testing for ranges of characters (`A-Z` in uppercase, and
`a-z` in lowercase), we can use a shorthand regular expression syntax.
Here is `soundex/stage1/soundex1b.py`:

        if not re.search('^[A-Za-z]+$', source):
            return "0000"

`timeit` says `soundex1b.py` is slightly faster than `soundex1a.py`, but
nothing to get terribly excited about:

    C:\samples\soundex\stage1>python soundex1b.py
    Woo             W000 17.1361133887
    Pilgrim         P426 21.8201693232
    Flingjingwaller F452 32.7262294509

We saw in [Section 15.3,
“Refactoring”](../refactoring/refactoring.html "15.3. Refactoring") that
regular expressions can be compiled and reused for faster results. Since
this regular expression never changes across function calls, we can
compile it once and use the compiled version. Here is
`soundex/stage1/soundex1c.py`:

    isOnlyChars = re.compile('^[A-Za-z]+$').search
    def soundex(source):
        if not isOnlyChars(source):
            return "0000"

Using a compiled regular expression in `soundex1c.py` is significantly
faster:

    C:\samples\soundex\stage1>python soundex1c.py
    Woo             W000 14.5348347346
    Pilgrim         P426 19.2784703084
    Flingjingwaller F452 30.0893873383

But is this the wrong path? The logic here is simple: the input `source`
needs to be non-empty, and it needs to be composed entirely of letters.
Wouldn't it be faster to write a loop checking each character, and do
away with regular expressions altogether?

Here is `soundex/stage1/soundex1d.py`:

        if not source:
            return "0000"
        for c in source:
            if not ('A' <= c <= 'Z') and not ('a' <= c <= 'z'):
                return "0000"

It turns out that this technique in `soundex1d.py` is *not* faster than
using a compiled regular expression (although it is faster than using a
non-compiled regular expression):

    C:\samples\soundex\stage1>python soundex1d.py
    Woo             W000 15.4065058548
    Pilgrim         P426 22.2753567842
    Flingjingwaller F452 37.5845122774

Why isn't `soundex1d.py` faster? The answer lies in the interpreted
nature of Python. The regular expression engine is written in C, and
compiled to run natively on your computer. On the other hand, this loop
is written in Python, and runs through the Python interpreter. Even
though the loop is relatively simple, it's not simple enough to make up
for the overhead of being interpreted. Regular expressions are never the
right answer... except when they are.

It turns out that Python offers an obscure string method. You can be
excused for not knowing about it, since it's never been mentioned in
this book. The method is called `isalpha()`, and it checks whether a
string contains only letters.

This is `soundex/stage1/soundex1e.py`:

        if (not source) and (not source.isalpha()):
            return "0000"

How much did we gain by using this specific method in `soundex1e.py`?
Quite a bit.

    C:\samples\soundex\stage1>python soundex1e.py
    Woo             W000 13.5069504644
    Pilgrim         P426 18.2199394057
    Flingjingwaller F452 28.9975225902

### Example 18.3. Best Result So Far: `soundex/stage1/soundex1e.py`

    import string, re

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
        if (not source) and (not source.isalpha()):
            return "0000"
        source = source[0].upper() + source[1:]
        digits = source[0]
        for s in source[1:]:
            s = s.upper()
            digits += charToSoundex[s]
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

  

