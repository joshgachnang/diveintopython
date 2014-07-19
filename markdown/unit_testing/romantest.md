

13.3. Introducing `romantest.py`
--------------------------------

This is the complete test suite for your Roman numeral conversion
functions, which are yet to be written but will eventually be in
`roman.py`. It is not immediately obvious how it all fits together; none
of these classes or methods reference any of the others. There are good
reasons for this, as you'll see shortly.

### Example 13.1. `romantest.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Unit test for roman.py"""

    import roman
    import unittest

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

        def testFromRomanKnownValues(self):                          
            """fromRoman should give known result with known input"""
            for integer, numeral in self.knownValues:                
                result = roman.fromRoman(numeral)                    
                self.assertEqual(integer, result)                    

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

    class SanityCheck(unittest.TestCase):        
        def testSanity(self):                    
            """fromRoman(toRoman(n))==n for all n"""
            for integer in range(1, 4000):       
                numeral = roman.toRoman(integer) 
                result = roman.fromRoman(numeral)
                self.assertEqual(integer, result)

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

    if __name__ == "__main__":
        unittest.main()   

### Further reading

-   [The PyUnit home page](http://pyunit.sourceforge.net/) has an
    in-depth discussion of [using the `unittest`
    framework](http://pyunit.sourceforge.net/pyunit.html), including
    advanced features not covered in this chapter.
-   [The PyUnit FAQ](http://pyunit.sourceforge.net/pyunit.html) explains
    [why test cases are stored
    separately](http://pyunit.sourceforge.net/pyunit.html#WHERE) from
    the code they test.
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes the
    [`unittest`](http://www.python.org/doc/current/lib/module-unittest.html)
    module.
-   [ExtremeProgramming.org](http://www.extremeprogramming.org/)
    discusses [why you should write unit
    tests](http://www.extremeprogramming.org/rules/unittests.html).
-   [The Portland Pattern Repository](http://www.c2.com/cgi/wiki) has an
    ongoing discussion of [unit
    tests](http://www.c2.com/cgi/wiki?UnitTests), including a [standard
    definition](http://www.c2.com/cgi/wiki?StandardDefinitionOfUnitTest),
    why you should [code unit tests
    first](http://www.c2.com/cgi/wiki?CodeUnitTestFirst), and several
    in-depth [case studies](http://www.c2.com/cgi/wiki?UnitTestTrial).

  

