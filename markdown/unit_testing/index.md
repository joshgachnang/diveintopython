

Chapter 13. Unit Testing
------------------------

-   [13.1. Introduction to Roman numerals](index.html#roman.intro)
-   [13.2. Diving in](diving_in.html)
-   [13.3. Introducing romantest.py](romantest.html)
-   [13.4. Testing for success](testing_for_success.html)
-   [13.5. Testing for failure](testing_for_failure.html)
-   [13.6. Testing for sanity](testing_for_sanity.html)

13.1. Introduction to Roman numerals
------------------------------------

In previous chapters, you “dived in” by immediately looking at code and
trying to understand it as quickly as possible. Now that you have some
Python under your belt, you're going to step back and look at the steps
that happen *before* the code gets written.

In the next few chapters, you're going to write, debug, and optimize a
set of utility functions to convert to and from Roman numerals. You saw
the mechanics of constructing and validating Roman numerals in
[Section 7.3, “Case Study: Roman
Numerals”](../regular_expressions/roman_numerals.html "7.3. Case Study: Roman Numerals"),
but now let's step back and consider what it would take to expand that
into a two-way utility.

[The rules for Roman
numerals](../regular_expressions/roman_numerals.html "7.3. Case Study: Roman Numerals")
lead to a number of interesting observations:

1.  There is only one correct way to represent a particular number as
    Roman numerals.
2.  The converse is also true: if a string of characters is a valid
    Roman numeral, it represents only one number (*i.e.* it can only be
    read one way).
3.  There is a limited range of numbers that can be expressed as Roman
    numerals, specifically `1` through `3999`. (The Romans did have
    several ways of expressing larger numbers, for instance by having a
    bar over a numeral to represent that its normal value should be
    multiplied by `1000`, but you're not going to deal with that. For
    the purposes of this chapter, let's stipulate that Roman numerals go
    from `1` to `3999`.)
4.  There is no way to represent `0` in Roman numerals. (Amazingly, the
    ancient Romans had no concept of `0` as a number. Numbers were for
    counting things you had; how can you count what you don't have?)
5.  There is no way to represent negative numbers in Roman numerals.
6.  There is no way to represent fractions or non-integer numbers in
    Roman numerals.

Given all of this, what would you expect out of a set of functions to
convert to and from Roman numerals?

### `roman.py` requirements

1.  `toRoman` should return the Roman numeral representation for all
    integers `1` to `3999`.
2.  `toRoman` should fail when given an integer outside the range `1` to
    `3999`.
3.  `toRoman` should fail when given a non-integer number.
4.  `fromRoman` should take a valid Roman numeral and return the number
    that it represents.
5.  `fromRoman` should fail when given an invalid Roman numeral.
6.  If you take a number, convert it to Roman numerals, then convert
    that back to a number, you should end up with the number you started
    with. So `fromRoman(toRoman(n)) == n` for all `n` in `1..3999`.
7.  `toRoman` should always return a Roman numeral using uppercase
    letters.
8.  `fromRoman` should only accept uppercase Roman numerals (*i.e.* it
    should fail when given lowercase input).

### Further reading

-   [This site](http://www.wilkiecollins.demon.co.uk/roman/front.htm)
    has more on Roman numerals, including a fascinating
    [history](http://www.wilkiecollins.demon.co.uk/roman/intro.htm) of
    how Romans and other civilizations really used them (short answer:
    haphazardly and inconsistently).

  

