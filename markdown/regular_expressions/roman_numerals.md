

-   [7.3.1. Checking for Thousands](roman_numerals.html#d0e17592)
-   [7.3.2. Checking for Hundreds](roman_numerals.html#d0e17785)

7.3. Case Study: Roman Numerals
-------------------------------

-   [7.3.1. Checking for Thousands](roman_numerals.html#d0e17592)
-   [7.3.2. Checking for Hundreds](roman_numerals.html#d0e17785)

You've most likely seen Roman numerals, even if you didn't recognize
them. You may have seen them in copyrights of old movies and television
shows (“Copyright `MCMXLVI`” instead of “Copyright `1946`”), or on the
dedication walls of libraries or universities (“established
`MDCCCLXXXVIII`” instead of “established `1888`”). You may also have
seen them in outlines and bibliographical references. It's a system of
representing numbers that really does date back to the ancient Roman
empire (hence the name).

In Roman numerals, there are seven characters that are repeated and
combined in various ways to represent numbers.

-   `I` = `1`
-   `V` = `5`
-   `X` = `10`
-   `L` = `50`
-   `C` = `100`
-   `D` = `500`
-   `M` = `1000`

The following are some general rules for constructing Roman numerals:

-   Characters are additive. `I` is `1`, `II` is `2`, and `III` is `3`.
    `VI` is `6` (literally, “`5` and `1`”), `VII` is `7`, and `VIII` is
    `8`.
-   The tens characters (`I`, `X`, `C`, and `M`) can be repeated up to
    three times. At `4`, you need to subtract from the next highest
    fives character. You can't represent `4` as `IIII`; instead, it is
    represented as `IV` (“`1` less than `5`”). The number `40` is
    written as `XL` (`10` less than `50`), `41` as `XLI`, `42` as
    `XLII`, `43` as `XLIII`, and then `44` as `XLIV` (`10` less than
    `50`, then `1` less than `5`).
-   Similarly, at `9`, you need to subtract from the next highest tens
    character: `8` is `VIII`, but `9` is `IX` (`1` less than `10`), not
    `VIIII` (since the `I` character can not be repeated four times).
    The number `90` is `XC`, `900` is `CM`.
-   The fives characters can not be repeated. The number `10` is always
    represented as `X`, never as `VV`. The number `100` is always `C`,
    never `LL`.
-   Roman numerals are always written highest to lowest, and read left
    to right, so the order the of characters matters very much. `DC` is
    `600`; `CD` is a completely different number (`400`, `100` less than
    `500`). `CI` is `101`; `IC` is not even a valid Roman numeral
    (because you can't subtract `1` directly from `100`; you would need
    to write it as `XCIX`, for `10` less than `100`, then `1` less than
    `10`).

### 7.3.1. Checking for Thousands

What would it take to validate that an arbitrary string is a valid Roman
numeral? Let's take it one digit at a time. Since Roman numerals are
always written highest to lowest, let's start with the highest: the
thousands place. For numbers 1000 and higher, the thousands are
represented by a series of `M` characters.

### Example 7.3. Checking for Thousands

    >>> import re
    >>> pattern = '^M?M?M?$'       
    >>> re.search(pattern, 'M')    
    <SRE_Match object at 0106FB58>
    >>> re.search(pattern, 'MM')   
    <SRE_Match object at 0106C290>
    >>> re.search(pattern, 'MMM')  
    <SRE_Match object at 0106AA38>
    >>> re.search(pattern, 'MMMM') 
    >>> re.search(pattern, '')     
    <SRE_Match object at 0106F4A8>

<table>
<col width="50%" />
<col width="50%" />
<tbody>
<tr class="odd">
<td align="left"><a href="#re.roman.1.1"><img src="../images/callouts/1.png" alt="1" /></a></td>
<td align="left">This pattern has three parts:
<ul>
<li><code class="literal">^</code> to match what follows only at the beginning of the string. If this were not specified, the pattern would match no matter where the <code class="literal">M</code> characters were, which is not what you want. You want to make sure that the <code class="literal">M</code> characters, if they're there, are at the beginning of the string.</li>
<li><code class="literal">M?</code> to optionally match a single <code class="literal">M</code> character. Since this is repeated three times, you're matching anywhere from zero to three <code class="literal">M</code> characters in a row.</li>
<li><code class="literal">$</code> to match what precedes only at the end of the string. When combined with the <code class="literal">^</code> character at the beginning, this means that the pattern must match the entire string, with no other characters before or after the <code class="literal">M</code> characters.</li>
</ul></td>
</tr>
<tr class="even">
<td align="left"><a href="#re.roman.1.2"><img src="../images/callouts/2.png" alt="2" /></a></td>
<td align="left">The essence of the <code class="filename">re</code> module is the <code class="function">search</code> function, that takes a regular expression (<code class="varname">pattern</code>) and a string (<code class="literal">'M'</code>) to try to match against the regular expression. If a match is found, <code class="function">search</code> returns an object which has various methods to describe the match; if no match is found, <code class="function">search</code> returns <code class="literal">None</code>, the Python null value. All you care about at the moment is whether the pattern matches, which you can tell by just looking at the return value of <code class="function">search</code>. <code class="literal">'M'</code> matches this regular expression, because the first optional <code class="literal">M</code> matches and the second and third optional <code class="literal">M</code> characters are ignored.</td>
</tr>
<tr class="odd">
<td align="left"><a href="#re.roman.1.3"><img src="../images/callouts/3.png" alt="3" /></a></td>
<td align="left"><code class="literal">'MM'</code> matches because the first and second optional <code class="literal">M</code> characters match and the third <code class="literal">M</code> is ignored.</td>
</tr>
<tr class="even">
<td align="left"><a href="#re.roman.1.4"><img src="../images/callouts/4.png" alt="4" /></a></td>
<td align="left"><code class="literal">'MMM'</code> matches because all three <code class="literal">M</code> characters match.</td>
</tr>
<tr class="odd">
<td align="left"><a href="#re.roman.1.5"><img src="../images/callouts/5.png" alt="5" /></a></td>
<td align="left"><code class="literal">'MMMM'</code> does not match. All three <code class="literal">M</code> characters match, but then the regular expression insists on the string ending (because of the <code class="literal">$</code> character), and the string doesn't end yet (because of the fourth <code class="literal">M</code>). So <code class="function">search</code> returns <code class="literal">None</code>.</td>
</tr>
<tr class="even">
<td align="left"><a href="#re.roman.1.6"><img src="../images/callouts/6.png" alt="6" /></a></td>
<td align="left">Interestingly, an empty string also matches this regular expression, since all the <code class="literal">M</code> characters are optional.</td>
</tr>
</tbody>
</table>

### 7.3.2. Checking for Hundreds

The hundreds place is more difficult than the thousands, because there
are several mutually exclusive ways it could be expressed, depending on
its value.

-   `100` = `C`
-   `200` = `CC`
-   `300` = `CCC`
-   `400` = `CD`
-   `500` = `D`
-   `600` = `DC`
-   `700` = `DCC`
-   `800` = `DCCC`
-   `900` = `CM`

So there are four possible patterns:

-   `CM`
-   `CD`
-   Zero to three `C` characters (zero if the hundreds place is 0)
-   `D`, followed by zero to three `C` characters

The last two patterns can be combined:

-   an optional `D`, followed by zero to three `C` characters

This example shows how to validate the hundreds place of a Roman
numeral.

### Example 7.4. Checking for Hundreds

    >>> import re
    >>> pattern = '^M?M?M?(CM CD D?C?C?C?)$' 
    >>> re.search(pattern, 'MCM')            
    <SRE_Match object at 01070390>
    >>> re.search(pattern, 'MD')             
    <SRE_Match object at 01073A50>
    >>> re.search(pattern, 'MMMCCC')         
    <SRE_Match object at 010748A8>
    >>> re.search(pattern, 'MCMC')           
    >>> re.search(pattern, '')               
    <SRE_Match object at 01071D98>



[![1](../images/callouts/1.png)](#re.roman.2.1) This pattern starts out the same as the previous one, checking for the beginning of the string (`^`), then the thousands place (`M?M?M?`). Then it has the new part, in parentheses, which defines a set of three mutually exclusive patterns, separated by vertical bars: `CM`, `CD`, and `D?C?C?C?` (which is an optional `D` followed by zero to three optional `C` characters). The regular expression parser checks for each of these patterns in order (from left to right), takes the first one that matches, and ignores the rest. 

[![2](../images/callouts/2.png)](#re.roman.2.2) `'MCM'` matches because the first `M` matches, the second and third `M` characters are ignored, and the `CM` matches (so the `CD` and `D?C?C?C?` patterns are never even considered). `MCM` is the Roman numeral representation of `1900`. 

[![3](../images/callouts/3.png)](#re.roman.2.3) `'MD'` matches because the first `M` matches, the second and third `M` characters are ignored, and the `D?C?C?C?` pattern matches `D` (each of the three `C` characters are optional and are ignored). `MD` is the Roman numeral representation of `1500`. 

[![4](../images/callouts/4.png)](#re.roman.2.4) `'MMMCCC'` matches because all three `M` characters match, and the `D?C?C?C?` pattern matches `CCC` (the `D` is optional and is ignored). `MMMCCC` is the Roman numeral representation of `3300`. 

[![5](../images/callouts/5.png)](#re.roman.2.5) `'MCMC'` does not match. The first `M` matches, the second and third `M` characters are ignored, and the `CM` matches, but then the `$` does not match because you're not at the end of the string yet (you still have an unmatched `C` character). The `C` does *not* match as part of the `D?C?C?C?` pattern, because the mutually exclusive `CM` pattern has already matched. 

[![6](../images/callouts/6.png)](#re.roman.2.6) Interestingly, an empty string still matches this pattern, because all the `M` characters are optional and ignored, and the empty string matches the `D?C?C?C?` pattern where all the characters are optional and ignored. 

Whew! See how quickly regular expressions can get nasty? And you've only
covered the thousands and hundreds places of Roman numerals. But if you
followed all that, the tens and ones places are easy, because they're
exactly the same pattern. But let's look at another way to express the
pattern.

  

