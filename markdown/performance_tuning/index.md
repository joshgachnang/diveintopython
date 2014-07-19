

Chapter 18. Performance Tuning
------------------------------

-   [18.1. Diving in](index.html#soundex.divein)
-   [18.2. Using the timeit Module](timeit.html)
-   [18.3. Optimizing Regular Expressions](regular_expressions.html)
-   [18.4. Optimizing Dictionary Lookups](dictionary_lookups.html)
-   [18.5. Optimizing List Operations](list_operations.html)
-   [18.6. Optimizing String Manipulation](string_manipulation.html)
-   [18.7. Summary](summary.html)

Performance tuning is a many-splendored thing. Just because Python is an
interpreted language doesn't mean you shouldn't worry about code
optimization. But don't worry about it *too* much.

18.1. Diving in
---------------

There are so many pitfalls involved in optimizing your code, it's hard
to know where to start.

Let's start here: *are you sure you need to do it at all?* Is your code
really so bad? Is it worth the time to tune it? Over the lifetime of
your application, how much time is going to be spent running that code,
compared to the time spent waiting for a remote database server, or
waiting for user input?

Second, *are you sure you're done coding?* Premature optimization is
like spreading frosting on a half-baked cake. You spend hours or days
(or more) optimizing your code for performance, only to discover it
doesn't do what you need it to do. That's time down the drain.

This is not to say that code optimization is worthless, but you need to
look at the whole system and decide whether it's the best use of your
time. Every minute you spend optimizing code is a minute you're not
spending adding new features, or writing documentation, or playing with
your kids, or writing unit tests.

Oh yes, unit tests. It should go without saying that you need a complete
set of unit tests before you begin performance tuning. The last thing
you need is to introduce new bugs while fiddling with your algorithms.

With these caveats in place, let's look at some techniques for
optimizing Python code. The code in question is an implementation of the
Soundex algorithm. Soundex was a method used in the early 20th century
for categorizing surnames in the United States census. It grouped
similar-sounding names together, so even if a name was misspelled,
researchers had a chance of finding it. Soundex is still used today for
much the same reason, although of course we use computerized database
servers now. Most database servers include a Soundex function.

There are several subtle variations of the Soundex algorithm. This is
the one used in this chapter:

1.  Keep the first letter of the name as-is.
2.  Convert the remaining letters to digits, according to a specific
    table:
    -   B, F, P, and V become 1.
    -   C, G, J, K, Q, S, X, and Z become 2.
    -   D and T become 3.
    -   L becomes 4.
    -   M and N become 5.
    -   R becomes 6.
    -   All other letters become 9.

3.  Remove consecutive duplicates.
4.  Remove all 9s altogether.
5.  If the result is shorter than four characters (the first letter plus
    three digits), pad the result with trailing zeros.
6.  if the result is longer than four characters, discard everything
    after the fourth character.

For example, my name, `Pilgrim`, becomes P942695. That has no
consecutive duplicates, so nothing to do there. Then you remove the 9s,
leaving P4265. That's too long, so you discard the excess character,
leaving P426.

Another example: `Woo` becomes W99, which becomes W9, which becomes W,
which gets padded with zeros to become W000.

Here's a first attempt at a Soundex function:

### Example 18.1. `soundex/stage1/soundex1a.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

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
        "convert string to Soundex equivalent"

        # Soundex requirements:
        # source string must be at least 1 character
        # and must consist entirely of letters
        allChars = string.uppercase + string.lowercase
        if not re.search('^[%s]+$' % allChars, source):
            return "0000"

        # Soundex algorithm:
        # 1. make first character uppercase
        source = source[0].upper() + source[1:]
        
        # 2. translate all other characters to Soundex digits
        digits = source[0]
        for s in source[1:]:
            s = s.upper()
            digits += charToSoundex[s]

        # 3. remove consecutive duplicates
        digits2 = digits[0]
        for d in digits[1:]:
            if digits2[-1] != d:
                digits2 += d
            
        # 4. remove all "9"s
        digits3 = re.sub('9', '', digits2)
        
        # 5. pad end with "0"s to 4 characters
        while len(digits3) < 4:
            digits3 += "0"
            
        # 6. return first 4 characters
        return digits3[:4]

    if __name__ == '__main__':
        from timeit import Timer
        names = ('Woo', 'Pilgrim', 'Flingjingwaller')
        for name in names:
            statement = "soundex('%s')" % name
            t = Timer(statement, "from __main__ import soundex")
            print name.ljust(15), soundex(name), min(t.repeat())

### Further Reading on Soundex

-   [Soundexing and Genealogy](http://www.avotaynu.com/soundex.html)
    gives a chronology of the evolution of the Soundex and its regional
    variations.

  

