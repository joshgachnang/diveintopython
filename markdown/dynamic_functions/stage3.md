

17.4. `plural.py`, stage 3
--------------------------

Defining separate named functions for each match and apply rule isn't
really necessary. You never call them directly; you define them in the
`rules` list and call them through there. Let's streamline the rules
definition by anonymizing those functions.

### Example 17.8. `plural3.py`

    import re

    rules = \
      (
        (
         lambda word: re.search('[sxz]$', word),
         lambda word: re.sub('$', 'es', word)
        ),
        (
         lambda word: re.search('[^aeioudgkprt]h$', word),
         lambda word: re.sub('$', 'es', word)
        ),
        (
         lambda word: re.search('[^aeiou]y$', word),
         lambda word: re.sub('y$', 'ies', word)
        ),
        (
         lambda word: re.search('$', word),
         lambda word: re.sub('$', 's', word)
        )
       )                                           

    def plural(noun):                             
        for matchesRule, applyRule in rules:       
            if matchesRule(noun):                 
                return applyRule(noun)            



[![1](../images/callouts/1.png)](#plural.stage3.1.1) This is the same set of rules as you defined in stage 2. The only difference is that instead of defining named functions like `match_sxz` and `apply_sxz`, you have “inlined” those function definitions directly into the `rules` list itself, using [lambda functions](../power_of_introspection/lambda_functions.html "4.7. Using lambda Functions"). 

[![2](../images/callouts/2.png)](#plural.stage3.1.2) Note that the `plural` function hasn't changed at all. It iterates through a set of rule functions, checks the first rule, and if it returns a true value, calls the second rule and returns the value. Same as above, word for word. The only difference is that the rule functions were defined inline, anonymously, using lambda functions. But the `plural` function doesn't care how they were defined; it just gets a list of rules and blindly works through them. 

Now to add a new rule, all you need to do is define the functions
directly in the `rules` list itself: one match rule, and one apply rule.
But defining the rule functions inline like this makes it very clear
that you have some unnecessary duplication here. You have four pairs of
functions, and they all follow the same pattern. The match function is a
single call to `re.search`, and the apply function is a single call to
`re.sub`. Let's factor out these similarities.

  

