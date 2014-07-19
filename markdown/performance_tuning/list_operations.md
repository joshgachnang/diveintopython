

18.5. Optimizing List Operations
--------------------------------

The third step in the Soundex algorithm is eliminating consecutive
duplicate digits. What's the best way to do this?

Here's the code we have so far, in `soundex/stage2/soundex2c.py`:

        digits2 = digits[0]
        for d in digits[1:]:
            if digits2[-1] != d:
                digits2 += d

Here are the performance results for `soundex2c.py`:

    C:\samples\soundex\stage2>python soundex2c.py
    Woo             W000 12.6070768771
    Pilgrim         P426 14.4033353401
    Flingjingwaller F452 19.7774882003

The first thing to consider is whether it's efficient to check
`digits[-1]` each time through the loop. Are list indexes expensive?
Would we be better off maintaining the last digit in a separate
variable, and checking that instead?

To answer this question, here is `soundex/stage3/soundex3a.py`:

        digits2 = ''
        last_digit = ''
        for d in digits:
            if d != last_digit:
                digits2 += d
                last_digit = d

`soundex3a.py` does not run any faster than `soundex2c.py`, and may even
be slightly slower (although it's not enough of a difference to say for
sure):

    C:\samples\soundex\stage3>python soundex3a.py
    Woo             W000 11.5346048171
    Pilgrim         P426 13.3950636184
    Flingjingwaller F452 18.6108927252

Why isn't `soundex3a.py` faster? It turns out that list indexes in
Python are extremely efficient. Repeatedly accessing `digits2[-1]` is no
problem at all. On the other hand, manually maintaining the last seen
digit in a separate variable means we have *two* variable assignments
for each digit we're storing, which wipes out any small gains we might
have gotten from eliminating the list lookup.

Let's try something radically different. If it's possible to treat a
string as a list of characters, it should be possible to use a list
comprehension to iterate through the list. The problem is, the code
needs access to the previous character in the list, and that's not easy
to do with a straightforward list comprehension.

However, it is possible to create a list of index numbers using the
built-in `range()` function, and use those index numbers to
progressively search through the list and pull out each character that
is different from the previous character. That will give you a list of
characters, and you can use the string method `join()` to reconstruct a
string from that.

Here is `soundex/stage3/soundex3b.py`:

        digits2 = "".join([digits[i] for i in range(len(digits))
                           if i == 0 or digits[i-1] != digits[i]])

Is this faster? In a word, no.

    C:\samples\soundex\stage3>python soundex3b.py
    Woo             W000 14.2245271396
    Pilgrim         P426 17.8337165757
    Flingjingwaller F452 25.9954005327

It's possible that the techniques so far as have been “string-centric”.
Python can convert a string into a list of characters with a single
command: `list('abc')` returns `['a', 'b', 'c']`. Furthermore, lists can
be *modified in place* very quickly. Instead of incrementally building a
new list (or string) out of the source string, why not move elements
around within a single list?

Here is `soundex/stage3/soundex3c.py`, which modifies a list in place to
remove consecutive duplicate elements:

        digits = list(source[0].upper() + source[1:].translate(charToSoundex))
        i=0
        for item in digits:
            if item==digits[i]: continue
            i+=1
            digits[i]=item
        del digits[i+1:]
        digits2 = "".join(digits)

Is this faster than `soundex3a.py` or `soundex3b.py`? No, in fact it's
the slowest method yet:

    C:\samples\soundex\stage3>python soundex3c.py
    Woo             W000 14.1662554878
    Pilgrim         P426 16.0397885765
    Flingjingwaller F452 22.1789341942

We haven't made any progress here at all, except to try and rule out
several “clever” techniques. The fastest code we've seen so far was the
original, most straightforward method (`soundex2c.py`). Sometimes it
doesn't pay to be clever.

### Example 18.5. Best Result So Far: `soundex/stage2/soundex2c.py`

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

  

