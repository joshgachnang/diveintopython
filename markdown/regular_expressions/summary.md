

7.7. Summary
------------

This is just the tiniest tip of the iceberg of what regular expressions
can do. In other words, even though you're completely overwhelmed by
them now, believe me, you ain't seen nothing yet.

You should now be familiar with the following techniques:

-   `^` matches the beginning of a string.
-   `$` matches the end of a string.
-   `\b` matches a word boundary.
-   `\d` matches any numeric digit.
-   `\D` matches any non-numeric character.
-   `x?` matches an optional `x` character (in other words, it matches
    an `x` zero or one times).
-   `x*` matches `x` zero or more times.
-   `x+` matches `x` one or more times.
-   `x{n,m}` matches an `x` character at least `n` times, but not more
    than `m` times.
-   `(a b c)` matches either `a` or `b` or `c`.
-   `(x)` in general is a *remembered group*. You can get the value of
    what matched by using the `groups()` method of the object returned
    by `re.search`.

Regular expressions are extremely powerful, but they are not the correct
solution for every problem. You should learn enough about them to know
when they are appropriate, when they will solve your problems, and when
they will cause more problems than they solve.

 

Some people, when confronted with a problem, think “I know, I'll use
regular expressions.” Now they have two problems.

 

--Jamie Zawinski, [in
comp.emacs.xemacs](http://groups.google.com/groups?selm=33F0C496.370D7C45%40netscape.com)

 

  

