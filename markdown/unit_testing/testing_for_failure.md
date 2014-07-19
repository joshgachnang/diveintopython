

13.5. Testing for failure
-------------------------

It is not enough to test that functions succeed when given good input;
you must also test that they fail when given bad input. And not just any
sort of failure; they must fail in the way you expect.

Remember the [other requirements](index.html#roman.requirements) for
`toRoman`:

1.  `toRoman` should fail when given an integer outside the range `1` to
    `3999`.
2.  `toRoman` should fail when given a non-integer number.

In Python, functions indicate failure by raising
[exceptions](../file_handling/index.html#fileinfo.exception "6.1. Handling Exceptions"),
and the `unittest` module provides methods for testing whether a
function raises a particular exception when given bad input.

### Example 13.3. Testing bad input to `toRoman`

    class ToRomanBadInput(unittest.TestCase):                            
        def testTooLarge(self):                                          
            """toRoman should fail with large input"""                   
            self.assertRaises(roman.OutOfRangeError, roman.toRoman, 4000) 

        def testZero(self):                                              
            """toRoman should fail with 0 input"""                       
            self.assertRaises(roman.OutOfRangeError, roman.toRoman, 0)    

        def testNegative(self):                                          
            """toRoman should fail with negative input"""                
            self.assertRaises(roman.OutOfRangeError, roman.toRoman, -1)  

        def testNonInteger(self):                                        
            """toRoman should fail with non-integer input"""             
            self.assertRaises(roman.NotIntegerError, roman.toRoman, 0.5)  



[![1](../images/callouts/1.png)](#roman.failure.1.1) The `TestCase` class of the `unittest` provides the `assertRaises` method, which takes the following arguments: the exception you're expecting, the function you're testing, and the arguments you're passing that function. (If the function you're testing takes more than one argument, pass them all to `assertRaises`, in order, and it will pass them right along to the function you're testing.) Pay close attention to what you're doing here: instead of calling `toRoman` directly and manually checking that it raises a particular exception (by wrapping it in a [`try...except` block](../file_handling/index.html#fileinfo.exception "6.1. Handling Exceptions")), `assertRaises` has encapsulated all of that for us. All you do is give it the exception (`roman.OutOfRangeError`), the function (`toRoman`), and `toRoman`'s arguments (`4000`), and `assertRaises` takes care of calling `toRoman` and checking to make sure that it raises `roman.OutOfRangeError`. (Also note that you're passing the `toRoman` function itself as an argument; you're not calling it, and you're not passing the name of it as a string. Have I mentioned recently how handy it is that [everything in Python is an object](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object"), including functions and exceptions?) 

[![2](../images/callouts/2.png)](#roman.failure.1.2) Along with testing numbers that are too large, you need to test numbers that are too small. Remember, Roman numerals cannot express `0` or negative numbers, so you have a test case for each of those (`testZero` and `testNegative`). In `testZero`, you are testing that `toRoman` raises a `roman.OutOfRangeError` exception when called with `0`; if it does *not* raise a `roman.OutOfRangeError` (either because it returns an actual value, or because it raises some other exception), this test is considered failed. 

[![3](../images/callouts/3.png)](#roman.failure.1.3) [Requirement \#3](index.html#roman.requirements) specifies that `toRoman` cannot accept a non-integer number, so here you test to make sure that `toRoman` raises a `roman.NotIntegerError` exception when called with `0.5`. If `toRoman` does not raise a `roman.NotIntegerError`, this test is considered failed. 

The next two [requirements](index.html#roman.requirements) are similar
to the first three, except they apply to `fromRoman` instead of
`toRoman`:

1.  `fromRoman` should take a valid Roman numeral and return the number
    that it represents.
2.  `fromRoman` should fail when given an invalid Roman numeral.

Requirement \#4 is handled in the same way as [requirement
\#1](testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues"),
iterating through a sampling of known values and testing each in turn.
Requirement \#5 is handled in the same way as requirements \#2 and \#3,
by testing a series of bad inputs and making sure `fromRoman` raises the
appropriate exception.

### Example 13.4. Testing bad input to `fromRoman`

    class FromRomanBadInput(unittest.TestCase):                                      
        def testTooManyRepeatedNumerals(self):                                       
            """fromRoman should fail with too many repeated numerals"""              
            for s in ('MMMM', 'DD', 'CCCC', 'LL', 'XXXX', 'VV', 'IIII'):             
                self.assertRaises(roman.InvalidRomanNumeralError, roman.fromRoman, s) 

        def testRepeatedPairs(self):                                                 
            """fromRoman should fail with repeated pairs of numerals"""              
            for s in ('CMCM', 'CDCD', 'XCXC', 'XLXL', 'IXIX', 'IVIV'):               
                self.assertRaises(roman.InvalidRomanNumeralError, roman.fromRoman, s)

        def testMalformedAntecedent(self):                                           
            """fromRoman should fail with malformed antecedents"""                   
            for s in ('IIMXCC', 'VX', 'DCM', 'CMM', 'IXIV',
                      'MCMC', 'XCX', 'IVI', 'LM', 'LD', 'LC'):                       
                self.assertRaises(roman.InvalidRomanNumeralError, roman.fromRoman, s)



[![1](../images/callouts/1.png)](#roman.failure.2.1) Not much new to say about these; the pattern is exactly the same as the one you used to test bad input to `toRoman`. I will briefly note that you have another exception: `roman.InvalidRomanNumeralError`. That makes a total of three custom exceptions that will need to be defined in `roman.py` (along with `roman.OutOfRangeError` and `roman.NotIntegerError`). You'll see how to define these custom exceptions when you actually start writing `roman.py`, later in this chapter. 

  

