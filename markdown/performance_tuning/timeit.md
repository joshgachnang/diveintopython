

18.2. Using the `timeit` Module
-------------------------------

The most important thing you need to know about optimizing Python code
is that you shouldn't write your own timing function.

Timing short pieces of code is incredibly complex. How much processor
time is your computer devoting to running this code? Are there things
running in the background? Are you sure? Every modern computer has
background processes running, some all the time, some intermittently.
Cron jobs fire off at consistent intervals; background services
occasionally “wake up” to do useful things like check for new mail,
connect to instant messaging servers, check for application updates,
scan for viruses, check whether a disk has been inserted into your CD
drive in the last 100 nanoseconds, and so on. Before you start your
timing tests, turn everything off and disconnect from the network. Then
turn off all the things you forgot to turn off the first time, then turn
off the service that's incessantly checking whether the network has come
back yet, then ...

And then there's the matter of the variations introduced by the timing
framework itself. Does the Python interpreter cache method name lookups?
Does it cache code block compilations? Regular expressions? Will your
code have side effects if run more than once? Don't forget that you're
dealing with small fractions of a second, so small mistakes in your
timing framework will irreparably skew your results.

The Python community has a saying: “Python comes with batteries
included.” Don't write your own timing framework. Python 2.3 comes with
a perfectly good one called `timeit`.

### Example 18.2. Introducing `timeit`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    >>> import timeit
    >>> t = timeit.Timer("soundex.soundex('Pilgrim')",
    ...     "import soundex")   
    >>> t.timeit()              
    8.21683733547
    >>> t.repeat(3, 2000000)    
    [16.48319309109, 16.46128984923, 16.44203948912]



[![1](../images/callouts/1.png)](#soundex.timeit.1.1) The `timeit` module defines one class, `Timer`, which takes two arguments. Both arguments are strings. The first argument is the statement you wish to time; in this case, you are timing a call to the Soundex function within the `soundex` with an argument of `'Pilgrim'`. The second argument to the `Timer` class is the import statement that sets up the environment for the statement. Internally, `timeit` sets up an isolated virtual environment, manually executes the setup statement (importing the `soundex` module), then manually compiles and executes the timed statement (calling the Soundex function). 

[![2](../images/callouts/2.png)](#soundex.timeit.1.2) Once you have the `Timer` object, the easiest thing to do is call `timeit()`, which calls your function 1 million times and returns the number of seconds it took to do it. 

[![3](../images/callouts/3.png)](#soundex.timeit.1.3) The other major method of the `Timer` object is `repeat()`, which takes two optional arguments. The first argument is the number of times to repeat the entire test, and the second argument is the number of times to call the timed statement within each test. Both arguments are optional, and they default to `3` and `1000000` respectively. The `repeat()` method returns a list of the times each test cycle took, in seconds. 


![Tip](../images/tip.png) 
You can use the `timeit` module on the command line to test an existing Python program, without modifying the code. See [http://docs.python.org/lib/node396.html](http://docs.python.org/lib/node396.html) for documentation on the command-line flags. 

Note that `repeat()` returns a list of times. The times will almost
never be identical, due to slight variations in how much processor time
the Python interpreter is getting (and those pesky background processes
that you can't get rid of). Your first thought might be to say “Let's
take the average and call that The True Number.”

In fact, that's almost certainly wrong. The tests that took longer
didn't take longer because of variations in your code or in the Python
interpreter; they took longer because of those pesky background
processes, or other factors outside of the Python interpreter that you
can't fully eliminate. If the different timing results differ by more
than a few percent, you still have too much variability to trust the
results. Otherwise, take the minimum time and discard the rest.

Python has a handy `min` function that takes a list and returns the
smallest value:

    >>> min(t.repeat(3, 1000000))
    8.22203948912


![Tip](../images/tip.png) 
The `timeit` module only works if you already know what piece of code you need to optimize. If you have a larger Python program and don't know where your performance problems are, check out [the `hotshot` module.](http://docs.python.org/lib/module-hotshot.html) 

  

