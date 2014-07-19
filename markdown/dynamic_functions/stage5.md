

17.6. `plural.py`, stage 5
--------------------------

You've factored out all the duplicate code and added enough abstractions
so that the pluralization rules are defined in a list of strings. The
next logical step is to take these strings and put them in a separate
file, where they can be maintained separately from the code that uses
them.

First, let's create a text file that contains the rules you want. No
fancy data structures, just space- (or tab-)delimited strings in three
columns. You'll call it `rules.en`; “en” stands for English. These are
the rules for pluralizing English nouns. You could add other rule files
for other languages later.

### Example 17.15. `rules.en`

    [sxz]$                  $               es
    [^aeioudgkprt]h$        $               es
    [^aeiou]y$              y$              ies
    $                       $               s

Now let's see how you can use this rules file.

### Example 17.16. `plural5.py`

    import re
    import string                                                                     

    def buildRule((pattern, search, replace)):                                        
        return lambda word: re.search(pattern, word) and re.sub(search, replace, word) 

    def plural(noun, language='en'):                             
        lines = file('rules.%s' % language).readlines()          
        patterns = map(string.split, lines)                      
        rules = map(buildRule, patterns)                         
        for rule in rules:                                      
            result = rule(noun)                                  
            if result: return result                            



[![1](../images/callouts/1.png)](#plural.stage5.1.1) You're still using the closures technique here (building a function dynamically that uses variables defined outside the function), but now you've combined the separate match and apply functions into one. (The reason for this change will become clear in the next section.) This will let you accomplish the same thing as having two functions, but you'll need to call it differently, as you'll see in a minute. 

[![2](../images/callouts/2.png)](#plural.stage5.1.2) Our `plural` function now takes an optional second parameter, `language`, which defaults to `en`. 

[![3](../images/callouts/3.png)](#plural.stage5.1.3) You use the `language` parameter to construct a filename, then open the file and read the contents into a list. If `language` is `en`, then you'll open the `rules.en` file, read the entire thing, break it up by carriage returns, and return a list. Each line of the file will be one element in the list. 

[![4](../images/callouts/4.png)](#plural.stage5.1.4) As you saw, each line in the file really has three values, but they're separated by whitespace (tabs or spaces, it makes no difference). Mapping the `string.split` function onto this list will create a new list where each element is a tuple of three strings. So a line like `[sxz]$ $ es` will be broken up into the tuple `('[sxz]$', '$', 'es')`. This means that `patterns` will end up as a list of tuples, just like you hard-coded it in [stage 4](stage4.html "17.5. plural.py, stage 4"). 

[![5](../images/callouts/5.png)](#plural.stage5.1.5) If `patterns` is a list of tuples, then `rules` will be a list of the functions created dynamically by each call to `buildRule`. Calling `buildRule(('[sxz]$', '$', 'es'))` returns a function that takes a single parameter, `word`. When this returned function is called, it will execute `re.search('[sxz]$', word) and re.sub('$', 'es', word)`. 

[![6](../images/callouts/6.png)](#plural.stage5.1.6) Because you're now building a combined match-and-apply function, you need to call it differently. Just call the function, and if it returns something, then that's the plural; if it returns nothing (`None`), then the rule didn't match and you need to try another rule. 

So the improvement here is that you've completely separated the
pluralization rules into an external file. Not only can the file be
maintained separately from the code, but you've set up a naming scheme
where the same `plural` function can use different rule files, based on
the `language` parameter.

The downside here is that you're reading that file every time you call
the `plural` function. I thought I could get through this entire book
without using the phrase “left as an exercise for the reader”, but here
you go: building a caching mechanism for the language-specific rule
files that auto-refreshes itself if the rule files change between calls
*is left as an exercise for the reader*. Have fun.

  

