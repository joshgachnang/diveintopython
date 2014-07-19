

Chapter 17. Dynamic functions
-----------------------------

-   [17.1. Diving in](index.html#plural.divein)
-   [17.2. plural.py, stage 1](stage1.html)
-   [17.3. plural.py, stage 2](stage2.html)
-   [17.4. plural.py, stage 3](stage3.html)
-   [17.5. plural.py, stage 4](stage4.html)
-   [17.6. plural.py, stage 5](stage5.html)
-   [17.7. plural.py, stage 6](stage6.html)
-   [17.8. Summary](summary.html)

17.1. Diving in
---------------

I want to talk about plural nouns. Also, functions that return other
functions, advanced regular expressions, and generators. Generators are
new in Python 2.3. But first, let's talk about how to make plural nouns.

If you haven't read [Chapter 7, *Regular
Expressions*](../regular_expressions/index.html "Chapter 7. Regular Expressions"),
now would be a good time. This chapter assumes you understand the basics
of regular expressions, and quickly descends into more advanced uses.

English is a schizophrenic language that borrows from a lot of other
languages, and the rules for making singular nouns into plural nouns are
varied and complex. There are rules, and then there are exceptions to
those rules, and then there are exceptions to the exceptions.

If you grew up in an English-speaking country or learned English in a
formal school setting, you're probably familiar with the basic rules:

1.  If a word ends in S, X, or Z, add ES. “Bass” becomes “basses”, “fax”
    becomes “faxes”, and “waltz” becomes “waltzes”.
2.  If a word ends in a noisy H, add ES; if it ends in a silent H, just
    add S. What's a noisy H? One that gets combined with other letters
    to make a sound that you can hear. So “coach” becomes “coaches” and
    “rash” becomes “rashes”, because you can hear the CH and SH sounds
    when you say them. But “cheetah” becomes “cheetahs”, because the H
    is silent.
3.  If a word ends in Y that sounds like I, change the Y to IES; if the
    Y is combined with a vowel to sound like something else, just add S.
    So “vacancy” becomes “vacancies”, but “day” becomes “days”.
4.  If all else fails, just add S and hope for the best.

(I know, there are a lot of exceptions. “Man” becomes “men” and “woman”
becomes “women”, but “human” becomes “humans”. “Mouse” becomes “mice”
and “louse” becomes “lice”, but “house” becomes “houses”. “Knife”
becomes “knives” and “wife” becomes “wives”, but “lowlife” becomes
“lowlifes”. And don't even get me started on words that are their own
plural, like “sheep”, “deer”, and “haiku”.)

Other languages are, of course, completely different.

Let's design a module that pluralizes nouns. Start with just English
nouns, and just these four rules, but keep in mind that you'll
inevitably need to add more rules, and you may eventually need to add
more languages.

  

