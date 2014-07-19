

13.2. Diving in
---------------

Now that you've completely defined the behavior you expect from your
conversion functions, you're going to do something a little unexpected:
you're going to write a test suite that puts these functions through
their paces and makes sure that they behave the way you want them to.
You read that right: you're going to write code that tests code that you
haven't written yet.

This is called unit testing, since the set of two conversion functions
can be written and tested as a unit, separate from any larger program
they may become part of later. Python has a framework for unit testing,
the appropriately-named `unittest` module.


![Note](../images/note.png) 
`unittest` is included with Python 2.1 and later. Python 2.0 users can download it from [`pyunit.sourceforge.net`](http://pyunit.sourceforge.net/). 

Unit testing is an important part of an overall testing-centric
development strategy. If you write unit tests, it is important to write
them early (preferably before writing the code that they test), and to
keep them updated as code and requirements change. Unit testing is not a
replacement for higher-level functional or system testing, but it is
important in all phases of development:

-   Before writing code, it forces you to detail your requirements in a
    useful fashion.
-   While writing code, it keeps you from over-coding. When all the test
    cases pass, the function is complete.
-   When refactoring code, it assures you that the new version behaves
    the same way as the old version.
-   When maintaining code, it helps you cover your ass when someone
    comes screaming that your latest change broke their old code. (“But
    *sir*, all the unit tests passed when I checked it in...”)
-   When writing code in a team, it increases confidence that the code
    you're about to commit isn't going to break other peoples' code,
    because you can run their unittests first. (I've seen this sort of
    thing in code sprints. A team breaks up the assignment, everybody
    takes the specs for their task, writes unit tests for it, then
    shares their unit tests with the rest of the team. That way, nobody
    goes off too far into developing code that won't play well with
    others.)

  

