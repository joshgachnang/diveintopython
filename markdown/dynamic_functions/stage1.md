

17.2. `plural.py`, stage 1
--------------------------

So you're looking at words, which at least in English are strings of
characters. And you have rules that say you need to find different
combinations of characters, and then do different things to them. This
sounds like a job for regular expressions.

### Example 17.1. `plural1.py`

    import re

    def plural(noun):                            
        if re.search('[sxz]$', noun):             
            return re.sub('$', 'es', noun)        
        elif re.search('[^aeioudgkprt]h$', noun):
            return re.sub('$', 'es', noun)       
        elif re.search('[^aeiou]y$', noun):      
            return re.sub('y$', 'ies', noun)     
        else:                                    
            return noun + 's'                    



[![1](../images/callouts/1.png)](#plural.stage1.1.1) OK, this is a regular expression, but it uses a syntax you didn't see in [Chapter 7, *Regular Expressions*](../regular_expressions/index.html "Chapter 7. Regular Expressions"). The square brackets mean “match exactly one of these characters”. So `[sxz]` means “`s`, or `x`, or `z`”, but only one of them. The `$` should be familiar; it matches the end of string. So you're checking to see if `noun` ends with `s`, `x`, or `z`. 

[![2](../images/callouts/2.png)](#plural.stage1.1.2) This `re.sub` function performs regular expression-based string substitutions. Let's look at it in more detail. 

### Example 17.2. Introducing `re.sub`

    >>> import re
    >>> re.search('[abc]', 'Mark')   
    <_sre.SRE_Match object at 0x001C1FA8>
    >>> re.sub('[abc]', 'o', 'Mark') 
    'Mork'
    >>> re.sub('[abc]', 'o', 'rock') 
    'rook'
    >>> re.sub('[abc]', 'o', 'caps') 
    'oops'



[![1](../images/callouts/1.png)](#plural.stage1.2.1) Does the string `Mark` contain `a`, `b`, or `c`? Yes, it contains `a`. 

[![2](../images/callouts/2.png)](#plural.stage1.2.2) OK, now find `a`, `b`, or `c`, and replace it with `o`. `Mark` becomes `Mork`. 

[![3](../images/callouts/3.png)](#plural.stage1.2.3) The same function turns `rock` into `rook`. 

[![4](../images/callouts/4.png)](#plural.stage1.2.4) You might think this would turn `caps` into `oaps`, but it doesn't. `re.sub` replaces *all* of the matches, not just the first one. So this regular expression turns `caps` into `oops`, because both the `c` and the `a` get turned into `o`. 

### Example 17.3. Back to `plural1.py`

    import re

    def plural(noun):                            
        if re.search('[sxz]$', noun):            
            return re.sub('$', 'es', noun)        
        elif re.search('[^aeioudgkprt]h$', noun): 
            return re.sub('$', 'es', noun)        
        elif re.search('[^aeiou]y$', noun):      
            return re.sub('y$', 'ies', noun)     
        else:                                    
            return noun + 's'                    



[![1](../images/callouts/1.png)](#plural.stage1.3.1) Back to the `plural` function. What are you doing? You're replacing the end of string with `es`. In other words, adding `es` to the string. You could accomplish the same thing with string concatenation, for example `noun + 'es'`, but I'm using regular expressions for everything, for consistency, for reasons that will become clear later in the chapter. 

[![2](../images/callouts/2.png)](#plural.stage1.3.2) Look closely, this is another new variation. The `^` as the first character inside the square brackets means something special: negation. `[^abc]` means “any single character *except* `a`, `b`, or `c`”. So `[^aeioudgkprt]` means any character except `a`, `e`, `i`, `o`, `u`, `d`, `g`, `k`, `p`, `r`, or `t`. Then that character needs to be followed by `h`, followed by end of string. You're looking for words that end in H where the H can be heard. 

[![3](../images/callouts/3.png)](#plural.stage1.3.3) Same pattern here: match words that end in Y, where the character before the Y is *not* `a`, `e`, `i`, `o`, or `u`. You're looking for words that end in Y that sounds like I. 

### Example 17.4. More on negation regular expressions

    >>> import re
    >>> re.search('[^aeiou]y$', 'vacancy') 
    <_sre.SRE_Match object at 0x001C1FA8>
    >>> re.search('[^aeiou]y$', 'boy')     
    >>> 
    >>> re.search('[^aeiou]y$', 'day')
    >>> 
    >>> re.search('[^aeiou]y$', 'pita')    
    >>> 



[![1](../images/callouts/1.png)](#plural.stage1.4.1) `vacancy` matches this regular expression, because it ends in `cy`, and `c` is not `a`, `e`, `i`, `o`, or `u`. 

[![2](../images/callouts/2.png)](#plural.stage1.4.2) `boy` does not match, because it ends in `oy`, and you specifically said that the character before the `y` could not be `o`. `day` does not match, because it ends in `ay`. 

[![3](../images/callouts/3.png)](#plural.stage1.4.3) `pita` does not match, because it does not end in `y`. 

### Example 17.5. More on `re.sub`

    >>> re.sub('y$', 'ies', 'vacancy')              
    'vacancies'
    >>> re.sub('y$', 'ies', 'agency')
    'agencies'
    >>> re.sub('([^aeiou])y$', r'\1ies', 'vacancy') 
    'vacancies'



[![1](../images/callouts/1.png)](#plural.stage1.5.1) This regular expression turns `vacancy` into `vacancies` and `agency` into `agencies`, which is what you wanted. Note that it would also turn `boy` into `boies`, but that will never happen in the function because you did that `re.search` first to find out whether you should do this `re.sub`. 

[![2](../images/callouts/2.png)](#plural.stage1.5.2) Just in passing, I want to point out that it is possible to combine these two regular expressions (one to find out if the rule applies, and another to actually apply it) into a single regular expression. Here's what that would look like. Most of it should look familiar: you're using a remembered group, which you learned in [Section 7.6, “Case study: Parsing Phone Numbers”](../regular_expressions/phone_numbers.html "7.6. Case study: Parsing Phone Numbers"), to remember the character before the `y`. Then in the substitution string, you use a new syntax, `\1`, which means “hey, that first group you remembered? put it here”. In this case, you remember the `c` before the `y`, and then when you do the substitution, you substitute `c` in place of `c`, and `ies` in place of `y`. (If you have more than one remembered group, you can use `\2` and `\3` and so on.) 

Regular expression substitutions are extremely powerful, and the `\1`
syntax makes them even more powerful. But combining the entire operation
into one regular expression is also much harder to read, and it doesn't
directly map to the way you first described the pluralizing rules. You
originally laid out rules like “if the word ends in S, X, or Z, then add
ES”. And if you look at this function, you have two lines of code that
say “if the word ends in S, X, or Z, then add ES”. It doesn't get much
more direct than that.

  

