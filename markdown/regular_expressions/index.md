

Chapter 7. Regular Expressions
------------------------------

-   [7.1. Diving In](index.html#re.intro)
-   [7.2. Case Study: Street Addresses](street_addresses.html)
-   [7.3. Case Study: Roman Numerals](roman_numerals.html)
    -   [7.3.1. Checking for Thousands](roman_numerals.html#d0e17592)
    -   [7.3.2. Checking for Hundreds](roman_numerals.html#d0e17785)
-   [7.4. Using the {n,m} Syntax](n_m_syntax.html)
    -   [7.4.1. Checking for Tens and Ones](n_m_syntax.html#d0e18326)
-   [7.5. Verbose Regular Expressions](verbose.html)
-   [7.6. Case study: Parsing Phone Numbers](phone_numbers.html)
-   [7.7. Summary](summary.html)

Regular expressions are a powerful and standardized way of searching,
replacing, and parsing text with complex patterns of characters. If
you've used regular expressions in other languages (like Perl), the
syntax will be very familiar, and you get by just reading the summary of
the [`re` module](http://www.python.org/doc/current/lib/module-re.html)
to get an overview of the available functions and their arguments.

7.1. Diving In
--------------

Strings have methods for searching (`index`, `find`, and `count`),
replacing (`replace`), and parsing (`split`), but they are limited to
the simplest of cases. The search methods look for a single, hard-coded
substring, and they are always case-sensitive. To do case-insensitive
searches of a string `s`, you must call `s.lower()` or `s.upper()` and
make sure your search strings are the appropriate case to match. The
`replace` and `split` methods have the same limitations.

If what you're trying to do can be accomplished with string functions,
you should use them. They're fast and simple and easy to read, and
there's a lot to be said for fast, simple, readable code. But if you
find yourself using a lot of different string functions with `if`
statements to handle special cases, or if you're combining them with
`split` and `join` and list comprehensions in weird unreadable ways, you
may need to move up to regular expressions.

Although the regular expression syntax is tight and unlike normal code,
the result can end up being *more* readable than a hand-rolled solution
that uses a long chain of string functions. There are even ways of
embedding comments within regular expressions to make them practically
self-documenting.

  

