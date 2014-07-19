

18.6. Optimizing String Manipulation
------------------------------------

The final step of the Soundex algorithm is padding short results with
zeros, and truncating long results. What is the best way to do this?

This is what we have so far, taken from `soundex/stage2/soundex2c.py`:

        digits3 = re.sub('9', '', digits2)
        while len(digits3) < 4:
            digits3 += "0"
        return digits3[:4]

These are the results for `soundex2c.py`:

    C:\samples\soundex\stage2>python soundex2c.py
    Woo             W000 12.6070768771
    Pilgrim         P426 14.4033353401
    Flingjingwaller F452 19.7774882003

The first thing to consider is replacing that regular expression with a
loop. This code is from `soundex/stage4/soundex4a.py`:

        digits3 = ''
        for d in digits2:
            if d != '9':
                digits3 += d

Is `soundex4a.py` faster? Yes it is:

    C:\samples\soundex\stage4>python soundex4a.py
    Woo             W000 6.62865531792
    Pilgrim         P426 9.02247576158
    Flingjingwaller F452 13.6328416042

But wait a minute. A loop to remove characters from a string? We can use
a simple string method for that. Here's `soundex/stage4/soundex4b.py`:

        digits3 = digits2.replace('9', '')

Is `soundex4b.py` faster? That's an interesting question. It depends on
the input:

    C:\samples\soundex\stage4>python soundex4b.py
    Woo             W000 6.75477414029
    Pilgrim         P426 7.56652144337
    Flingjingwaller F452 10.8727729362

The string method in `soundex4b.py` is faster than the loop for most
names, but it's actually slightly slower than `soundex4a.py` in the
trivial case (of a very short name). Performance optimizations aren't
always uniform; tuning that makes one case faster can sometimes make
other cases slower. In this case, the majority of cases will benefit
from the change, so let's leave it at that, but the principle is an
important one to remember.

Last but not least, let's examine the final two steps of the algorithm:
padding short results with zeros, and truncating long results to four
characters. The code you see in `soundex4b.py` does just that, but it's
horribly inefficient. Take a look at `soundex/stage4/soundex4c.py` to
see why:

        digits3 += '000'
        return digits3[:4]

Why do we need a `while` loop to pad out the result? We know in advance
that we're going to truncate the result to four characters, and we know
that we already have at least one character (the initial letter, which
is passed unchanged from the original `source` variable). That means we
can simply add three zeros to the output, then truncate it. Don't get
stuck in a rut over the exact wording of the problem; looking at the
problem slightly differently can lead to a simpler solution.

How much speed do we gain in `soundex4c.py` by dropping the `while`
loop? It's significant:

    C:\samples\soundex\stage4>python soundex4c.py
    Woo             W000 4.89129791636
    Pilgrim         P426 7.30642134685
    Flingjingwaller F452 10.689832367

Finally, there is still one more thing you can do to these three lines
of code to make them faster: you can combine them into one line. Take a
look at `soundex/stage4/soundex4d.py`:

        return (digits2.replace('9', '') + '000')[:4]

Putting all this code on one line in `soundex4d.py` is barely faster
than `soundex4c.py`:

    C:\samples\soundex\stage4>python soundex4d.py
    Woo             W000 4.93624105857
    Pilgrim         P426 7.19747593619
    Flingjingwaller F452 10.5490700634

It is also significantly less readable, and for not much performance
gain. Is that worth it? I hope you have good comments. Performance isn't
everything. Your optimization efforts must always be balanced against
threats to your program's readability and maintainability.

  

