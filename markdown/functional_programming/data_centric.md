

16.5. Data-centric programming
------------------------------

By now you're probably scratching your head wondering why this is better
than using `for` loops and straight function calls. And that's a
perfectly valid question. Mostly, it's a matter of perspective. Using
`map` and `filter` forces you to center your thinking around your data.

In this case, you started with no data at all; the first thing you did
was [get the directory
path](finding_the_path.html "16.2. Finding the path") of the current
script, and got a list of files in that directory. That was the
bootstrap, and it gave you real data to work with: a list of filenames.

However, you knew you didn't care about all of those files, only the
ones that were actually test suites. You had *too much data*, so you
needed to `filter` it. How did you know which data to keep? You needed a
test to decide, so you defined one and passed it to the `filter`
function. In this case you used a regular expression to decide, but the
concept would be the same regardless of how you constructed the test.

Now you had the filenames of each of the test suites (and only the test
suites, since everything else had been filtered out), but you really
wanted module names instead. You had the right amount of data, but it
was *in the wrong format*. So you defined a function that would
transform a single filename into a module name, and you mapped that
function onto the entire list. From one filename, you can get a module
name; from a list of filenames, you can get a list of module names.

Instead of `filter`, you could have used a `for` loop with an `if`
statement. Instead of `map`, you could have used a `for` loop with a
function call. But using `for` loops like that is busywork. At best, it
simply wastes time; at worst, it introduces obscure bugs. For instance,
you need to figure out how to test for the condition “is this file a
test suite?” anyway; that's the application-specific logic, and no
language can write that for us. But once you've figured that out, do you
really want go to all the trouble of defining a new empty list and
writing a `for` loop and an `if` statement and manually calling `append`
to add each element to the new list if it passes the condition and then
keeping track of which variable holds the new filtered data and which
one holds the old unfiltered data? Why not just define the test
condition, then let Python do the rest of that work for us?

Oh sure, you could try to be fancy and delete elements in place without
creating a new list. But you've been burned by that before. Trying to
modify a data structure that you're looping through can be tricky. You
delete an element, then loop to the next element, and suddenly you've
skipped one. Is Python one of the languages that works that way? How
long would it take you to figure it out? Would you remember for certain
whether it was safe the next time you tried? Programmers spend so much
time and make so many mistakes dealing with purely technical issues like
this, and it's all pointless. It doesn't advance your program at all;
it's just busywork.

I resisted list comprehensions when I first learned Python, and I
resisted `filter` and `map` even longer. I insisted on making my life
more difficult, sticking to the familiar way of `for` loops and `if`
statements and step-by-step code-centric programming. And my Python
programs looked a lot like Visual Basic programs, detailing every step
of every operation in every function. And they had all the same types of
little problems and obscure bugs. And it was all pointless.

Let it all go. Busywork code is not important. Data is important. And
data is not difficult. It's only data. If you have too much, filter it.
If it's not what you want, map it. Focus on the data; leave the busywork
behind.

  

