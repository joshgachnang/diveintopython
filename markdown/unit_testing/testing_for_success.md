

13.4. Testing for success
-------------------------

The most fundamental part of unit testing is constructing individual
test cases. A test case answers a single question about the code it is
testing.

A test case should be able to...

-   ...run completely by itself, without any human input. Unit testing
    is about automation.
-   ...determine by itself whether the function it is testing has passed
    or failed, without a human interpreting the results.
-   ...run in isolation, separate from any other test cases (even if
    they test the same functions). Each test case is an island.

Given that, let's build the first test case. You have the following
[requirement](index.html#roman.requirements):

1.  `toRoman` should return the Roman numeral representation for all
    integers `1` to `3999`.

### Example 13.2. `testToRomanKnownValues`

    class KnownValues(unittest.TestCase):                           
        knownValues = ( (1, 'I'),
                        (2, 'II'),
                        (3, 'III'),
                        (4, 'IV'),
                        (5, 'V'),
                        (6, 'VI'),
                        (7, 'VII'),
                        (8, 'VIII'),
                        (9, 'IX'),
                        (10, 'X'),
                        (50, 'L'),
                        (100, 'C'),
                        (500, 'D'),
                        (1000, 'M'),
                        (31, 'XXXI'),
                        (148, 'CXLVIII'),
                        (294, 'CCXCIV'),
                        (312, 'CCCXII'),
                        (421, 'CDXXI'),
                        (528, 'DXXVIII'),
                        (621, 'DCXXI'),
                        (782, 'DCCLXXXII'),
                        (870, 'DCCCLXX'),
                        (941, 'CMXLI'),
                        (1043, 'MXLIII'),
                        (1110, 'MCX'),
                        (1226, 'MCCXXVI'),
                        (1301, 'MCCCI'),
                        (1485, 'MCDLXXXV'),
                        (1509, 'MDIX'),
                        (1607, 'MDCVII'),
                        (1754, 'MDCCLIV'),
                        (1832, 'MDCCCXXXII'),
                        (1993, 'MCMXCIII'),
                        (2074, 'MMLXXIV'),
                        (2152, 'MMCLII'),
                        (2212, 'MMCCXII'),
                        (2343, 'MMCCCXLIII'),
                        (2499, 'MMCDXCIX'),
                        (2574, 'MMDLXXIV'),
                        (2646, 'MMDCXLVI'),
                        (2723, 'MMDCCXXIII'),
                        (2892, 'MMDCCCXCII'),
                        (2975, 'MMCMLXXV'),
                        (3051, 'MMMLI'),
                        (3185, 'MMMCLXXXV'),
                        (3250, 'MMMCCL'),
                        (3313, 'MMMCCCXIII'),
                        (3408, 'MMMCDVIII'),
                        (3501, 'MMMDI'),
                        (3610, 'MMMDCX'),
                        (3743, 'MMMDCCXLIII'),
                        (3844, 'MMMDCCCXLIV'),
                        (3888, 'MMMDCCCLXXXVIII'),
                        (3940, 'MMMCMXL'),
                        (3999, 'MMMCMXCIX'))                        

        def testToRomanKnownValues(self):                           
            """toRoman should give known result with known input"""
            for integer, numeral in self.knownValues:              
                result = roman.toRoman(integer)                      
                self.assertEqual(numeral, result)                   



[![1](../images/callouts/1.png)](#roman.success.1.0) To write a test case, first subclass the `TestCase` class of the `unittest` module. This class provides many useful methods which you can use in your test case to test specific conditions. 

[![2](../images/callouts/2.png)](#roman.success.1.1) This is a list of integer/numeral pairs that I verified manually. It includes the lowest ten numbers, the highest number, every number that translates to a single-character Roman numeral, and a random sampling of other valid numbers. The point of a unit test is not to test every possible input, but to test a representative sample. 

[![3](../images/callouts/3.png)](#roman.success.1.2) Every individual test is its own method, which must take no parameters and return no value. If the method exits normally without raising an exception, the test is considered passed; if the method raises an exception, the test is considered failed. 

[![4](../images/callouts/4.png)](#roman.success.1.3) Here you call the actual `toRoman` function. (Well, the function hasn't be written yet, but once it is, this is the line that will call it.) Notice that you have now defined the API for the `toRoman` function: it must take an integer (the number to convert) and return a string (the Roman numeral representation). If the API is different than that, this test is considered failed. 

[![5](../images/callouts/5.png)](#roman.success.1.4) Also notice that you are not trapping any exceptions when you call `toRoman`. This is intentional. `toRoman` shouldn't raise an exception when you call it with valid input, and these input values are all valid. If `toRoman` raises an exception, this test is considered failed. 

[![6](../images/callouts/6.png)](#roman.success.1.5) Assuming the `toRoman` function was defined correctly, called correctly, completed successfully, and returned a value, the last step is to check whether it returned the *right* value. This is a common question, and the `TestCase` class provides a method, `assertEqual`, to check whether two values are equal. If the result returned from `toRoman` (`result`) does not match the known value you were expecting (`numeral`), `assertEqual` will raise an exception and the test will fail. If the two values are equal, `assertEqual` will do nothing. If every value returned from `toRoman` matches the known value you expect, `assertEqual` never raises an exception, so `testToRomanKnownValues` eventually exits normally, which means `toRoman` has passed this test. 

  

