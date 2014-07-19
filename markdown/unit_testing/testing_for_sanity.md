

13.6. Testing for sanity
------------------------

Often, you will find that a unit of code contains a set of reciprocal
functions, usually in the form of conversion functions where one
converts A to B and the other converts B to A. In these cases, it is
useful to create a “sanity check” to make sure that you can convert A to
B and back to A without losing precision, incurring rounding errors, or
triggering any other sort of bug.

Consider this [requirement](index.html#roman.requirements):

1.  If you take a number, convert it to Roman numerals, then convert
    that back to a number, you should end up with the number you started
    with. So `fromRoman(toRoman(n)) == n` for all `n` in `1..3999`.

### Example 13.5. Testing `toRoman` against `fromRoman`

    class SanityCheck(unittest.TestCase):        
        def testSanity(self):                    
            """fromRoman(toRoman(n))==n for all n"""
            for integer in range(1, 4000):         
                numeral = roman.toRoman(integer) 
                result = roman.fromRoman(numeral)
                self.assertEqual(integer, result) 



[![1](../images/callouts/1.png)](#roman.sanity.1.1) You've seen [the `range` function](../native_data_types/declaring_variables.html#odbchelper.multiassign.range "Example 3.20. Assigning Consecutive Values") before, but here it is called with two arguments, which returns a list of integers starting at the first argument (`1`) and counting consecutively up to *but not including* the second argument (`4000`). Thus, `1..3999`, which is the valid range for converting to Roman numerals. 

[![2](../images/callouts/2.png)](#roman.sanity.1.2) I just wanted to mention in passing that `integer` is not a keyword in Python; here it's just a variable name like any other. 

[![3](../images/callouts/3.png)](#roman.sanity.1.3) The actual testing logic here is straightforward: take a number (`integer`), convert it to a Roman numeral (`numeral`), then convert it back to a number (`result`) and make sure you end up with the same number you started with. If not, `assertEqual` will raise an exception and the test will immediately be considered failed. If all the numbers match, `assertEqual` will always return silently, the entire `testSanity` method will eventually return silently, and the test will be considered passed. 

The [last two requirements](index.html#roman.requirements) are different
from the others because they seem both arbitrary and trivial:

1.  `toRoman` should always return a Roman numeral using uppercase
    letters.
2.  `fromRoman` should only accept uppercase Roman numerals (*i.e.* it
    should fail when given lowercase input).

In fact, they are somewhat arbitrary. You could, for instance, have
stipulated that `fromRoman` accept lowercase and mixed case input. But
they are not completely arbitrary; if `toRoman` is always returning
uppercase output, then `fromRoman` must at least accept uppercase input,
or the “sanity check” (requirement \#6) would fail. The fact that it
*only* accepts uppercase input is arbitrary, but as any systems
integrator will tell you, case always matters, so it's worth specifying
the behavior up front. And if it's worth specifying, it's worth testing.

### Example 13.6. Testing for case

    class CaseCheck(unittest.TestCase):                   
        def testToRomanCase(self):                        
            """toRoman should always return uppercase"""  
            for integer in range(1, 4000):                
                numeral = roman.toRoman(integer)          
                self.assertEqual(numeral, numeral.upper())         

        def testFromRomanCase(self):                      
            """fromRoman should only accept uppercase input"""
            for integer in range(1, 4000):                
                numeral = roman.toRoman(integer)          
                roman.fromRoman(numeral.upper())                    
                self.assertRaises(roman.InvalidRomanNumeralError,
                                  roman.fromRoman, numeral.lower())   



[![1](../images/callouts/1.png)](#roman.sanity.2.1) The most interesting thing about this test case is all the things it doesn't test. It doesn't test that the value returned from `toRoman` is [right](testing_for_success.html#roman.testtoromanknownvalues.example "Example 13.2. testToRomanKnownValues") or even [consistent](testing_for_sanity.html#roman.sanity.example "Example 13.5. Testing toRoman against fromRoman"); those questions are answered by separate test cases. You have a whole test case just to test for uppercase-ness. You might be tempted to combine this with the [sanity check](testing_for_sanity.html#roman.sanity.example "Example 13.5. Testing toRoman against fromRoman"), since both run through the entire range of values and call `toRoman`.<sup>[[6](#ftn.d0e32781)]</sup> But that would violate one of the [fundamental rules](testing_for_success.html "13.4. Testing for success"): each test case should answer only a single question. Imagine that you combined this case check with the sanity check, and then that test case failed. You would need to do further analysis to figure out which part of the test case failed to determine what the problem was. If you need to analyze the results of your unit testing just to figure out what they mean, it's a sure sign that you've mis-designed your test cases. 

[![2](../images/callouts/2.png)](#roman.sanity.2.2) There's a similar lesson to be learned here: even though “you know” that `toRoman` always returns uppercase, you are explicitly converting its return value to uppercase here to test that `fromRoman` accepts uppercase input. Why? Because the fact that `toRoman` always returns uppercase is an independent requirement. If you changed that requirement so that, for instance, it always returned lowercase, the `testToRomanCase` test case would need to change, but this test case would still work. This was another of the [fundamental rules](testing_for_success.html "13.4. Testing for success"): each test case must be able to work in isolation from any of the others. Every test case is an island. 

[![3](../images/callouts/3.png)](#roman.sanity.2.3) Note that you're not assigning the return value of `fromRoman` to anything. This is legal syntax in Python; if a function returns a value but nobody's listening, Python just throws away the return value. In this case, that's what you want. This test case doesn't test anything about the return value; it just tests that `fromRoman` accepts the uppercase input without raising an exception. 

[![4](../images/callouts/4.png)](#roman.sanity.2.4) This is a complicated line, but it's very similar to what you did in the `ToRomanBadInput` and `FromRomanBadInput` tests. You are testing to make sure that calling a particular function (`roman.fromRoman`) with a particular value (`numeral.lower()`, the lowercase version of the current Roman numeral in the loop) raises a particular exception (`roman.InvalidRomanNumeralError`). If it does (each time through the loop), the test passes; if even one time it does something else (like raises a different exception, or returning a value without raising an exception at all), the test fails. 

In the next chapter, you'll see how to write code that passes these
tests.

### Footnotes

<sup>[[6](#d0e32781)]</sup>“I can resist everything except temptation.”
--Oscar Wilde

  

