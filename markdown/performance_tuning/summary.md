

18.7. Summary
-------------

This chapter has illustrated several important aspects of performance
tuning in Python, and performance tuning in general.

-   If you need to choose between regular expressions and writing a
    loop, choose regular expressions. The regular expression engine is
    compiled in C and runs natively on your computer; your loop is
    written in Python and runs through the Python interpreter.
-   If you need to choose between regular expressions and string
    methods, choose string methods. Both are compiled in C, so choose
    the simpler one.
-   General-purpose dictionary lookups are fast, but specialtiy
    functions such as `string.maketrans` and string methods such as
    `isalpha()` are faster. If Python has a custom-tailored function for
    you, use it.
-   Don't be too clever. Sometimes the most obvious algorithm is also
    the fastest.
-   Don't sweat it too much. Performance isn't everything.

I can't emphasize that last point strongly enough. Over the course of
this chapter, you made this function three times faster and saved 20
seconds over 1 million function calls. Great. Now think: over the course
of those million function calls, how many seconds will your surrounding
application wait for a database connection? Or wait for disk I/O? Or
wait for user input? Don't spend too much time over-optimizing one
algorithm, or you'll ignore obvious improvements somewhere else. Develop
an instinct for the sort of code that Python runs well, correct obvious
blunders if you find them, and leave the rest alone.

  

