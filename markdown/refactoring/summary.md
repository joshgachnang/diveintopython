

15.5. Summary
-------------

Unit testing is a powerful concept which, if properly implemented, can
both reduce maintenance costs and increase flexibility in any long-term
project. It is also important to understand that unit testing is not a
panacea, a Magic Problem Solver, or a silver bullet. Writing good test
cases is hard, and keeping them up to date takes discipline (especially
when customers are screaming for critical bug fixes). Unit testing is
not a replacement for other forms of testing, including functional
testing, integration testing, and user acceptance testing. But it is
feasible, and it does work, and once you've seen it work, you'll wonder
how you ever got along without it.

This chapter covered a lot of ground, and much of it wasn't even
Python-specific. There are unit testing frameworks for many languages,
all of which require you to understand the same basic concepts:

-   Designing test cases that are specific, automated, and independent
-   Writing test cases *before* the code they are testing
-   Writing tests that [test good
    input](../unit_testing/testing_for_success.html "13.4. Testing for success")
    and check for proper results
-   Writing tests that [test bad
    input](../unit_testing/testing_for_failure.html "13.5. Testing for failure")
    and check for proper failures
-   Writing and updating test cases to [illustrate
    bugs](index.html#roman.bugs "15.1. Handling bugs") or [reflect new
    requirements](handling_changing_requirements.html "15.2. Handling changing requirements")
-   [Refactoring](refactoring.html "15.3. Refactoring") mercilessly to
    improve performance, scalability, readability, maintainability, or
    whatever other -ility you're lacking

Additionally, you should be comfortable doing all of the following
Python-specific things:

-   [Subclassing
    `unittest.TestCase`](../unit_testing/testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues")
    and writing methods for individual test cases
-   Using
    [`assertEqual`](../unit_testing/testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues")
    to check that a function returns a known value
-   Using
    [`assertRaises`](../unit_testing/testing_for_failure.html#roman.tobadinput.example "Example 13.3. Testing bad input to toRoman")
    to check that a function raises a known exception
-   Calling
    [`unittest.main()`](../unit_testing/stage_1.html#roman.stage1.output "Example 14.2. Output of romantest1.py against roman1.py")
    in your `if __name__` clause to run all your test cases at once
-   Running unit tests in
    [verbose](../unit_testing/stage_1.html#roman.stage1.output "Example 14.2. Output of romantest1.py against roman1.py")
    or
    [regular](refactoring.html#roman.stage8.1.output "Example 15.12. Output of romantest81.py against roman81.py")
    mode

### Further reading

-   [XProgramming.com](http://www.xprogramming.com/) has links to
    [download unit testing
    frameworks](http://www.xprogramming.com/software.htm) for many
    different languages.

  

