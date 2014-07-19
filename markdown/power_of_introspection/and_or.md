

4.6. The Peculiar Nature of `and` and `or`
------------------------------------------

-   [4.6.1. Using the and-or Trick](and_or.html#d0e9975)

In Python, `and` and `or` perform boolean logic as you would expect, but
they do not return boolean values; instead, they return one of the
actual values they are comparing.

### Example 4.15. Introducing `and`

    >>> 'a' and 'b'         
    'b'
    >>> '' and 'b'          
    ''
    >>> 'a' and 'b' and 'c' 
    'c'



[![1](../images/callouts/1.png)](#apihelper.andor.1.1) When using `and`, values are evaluated in a boolean context from left to right. `0`, `''`, `[]`, `()`, `{}`, and `None` are false in a boolean context; everything else is true. Well, almost everything. By default, instances of classes are true in a boolean context, but you can define special methods in your class to make an instance evaluate to false. You'll learn all about classes and special methods in [Chapter 5](../object_oriented_framework/index.html). If all values are true in a boolean context, `and` returns the last value. In this case, `and` evaluates `'a'`, which is true, then `'b'`, which is true, and returns `'b'`. 

[![2](../images/callouts/2.png)](#apihelper.andor.1.2) If any value is false in a boolean context, `and` returns the first false value. In this case, `''` is the first false value. 

[![3](../images/callouts/3.png)](#apihelper.andor.1.3) All values are true, so `and` returns the last value, `'c'`. 

### Example 4.16. Introducing `or`

    >>> 'a' or 'b'          
    'a'
    >>> '' or 'b'           
    'b'
    >>> '' or [] or {}      
    {}
    >>> def sidefx():
    ...     print "in sidefx()"
    ...     return 1
    >>> 'a' or sidefx()     
    'a'



[![1](../images/callouts/1.png)](#apihelper.andor.2.1) When using `or`, values are evaluated in a boolean context from left to right, just like `and`. If any value is true, `or` returns that value immediately. In this case, `'a'` is the first true value. 

[![2](../images/callouts/2.png)](#apihelper.andor.2.2) `or` evaluates `''`, which is false, then `'b'`, which is true, and returns `'b'`. 

[![3](../images/callouts/3.png)](#apihelper.andor.2.3) If all values are false, `or` returns the last value. `or` evaluates `''`, which is false, then `[]`, which is false, then `{}`, which is false, and returns `{}`. 

[![4](../images/callouts/4.png)](#apihelper.andor.2.4) Note that `or` evaluates values only until it finds one that is true in a boolean context, and then it ignores the rest. This distinction is important if some values can have side effects. Here, the function `sidefx` is never called, because `or` evaluates `'a'`, which is true, and returns `'a'` immediately. 

If you're a C hacker, you are certainly familiar with the `bool ? a` :
`b` expression, which evaluates to `a` if *`bool`* is true, and `b`
otherwise. Because of the way `and` and `or` work in Python, you can
accomplish the same thing.

### 4.6.1. Using the `and-or` Trick

### Example 4.17. Introducing the `and-or` Trick

    >>> a = "first"
    >>> b = "second"
    >>> 1 and a or b 
    'first'
    >>> 0 and a or b 
    'second'



[![1](../images/callouts/1.png)](#apihelper.andor.3.1) This syntax looks similar to the `bool ? a` : `b` expression in C. The entire expression is evaluated from left to right, so the `and` is evaluated first. `1 and 'first'` evalutes to `'first'`, then `'first' or 'second'` evalutes to `'first'`. 

[![2](../images/callouts/2.png)](#apihelper.andor.3.2) `0 and 'first'` evalutes to `False`, and then `0 or 'second'` evaluates to `'second'`. 

However, since this Python expression is simply boolean logic, and not a
special construct of the language, there is one extremely important
difference between this `and-or` trick in Python and the `bool ? a` :
`b` syntax in C. If the value of `a` is false, the expression will not
work as you would expect it to. (Can you tell I was bitten by this? More
than once?)

### Example 4.18. When the `and-or` Trick Fails

    >>> a = ""
    >>> b = "second"
    >>> 1 and a or b         
    'second'



[![1](../images/callouts/1.png)](#apihelper.andor.4.1) Since `a` is an empty string, which Python considers false in a boolean context, `1 and ''` evalutes to `''`, and then `'' or 'second'` evalutes to `'second'`. Oops! That's not what you wanted. 

The `and-or` trick, `bool and a` or `b`, will not work like the C
expression `bool ? a` : `b` when `a` is false in a boolean context.

The real trick behind the `and-or` trick, then, is to make sure that the
value of `a` is never false. One common way of doing this is to turn `a`
into `[a`] and `b` into `[b`], then taking the first element of the
returned list, which will be either `a` or `b`.

### Example 4.19. Using the `and-or` Trick Safely

    >>> a = ""
    >>> b = "second"
    >>> (1 and [a] or [b])[0] 
    ''



[![1](../images/callouts/1.png)](#apihelper.andor.5.1) Since `[a`] is a non-empty list, it is never false. Even if `a` is `0` or `''` or some other false value, the list `[a`] is true because it has one element. 

By now, this trick may seem like more trouble than it's worth. You
could, after all, accomplish the same thing with an `if` statement, so
why go through all this fuss? Well, in many cases, you are choosing
between two constant values, so you can use the simpler syntax and not
worry, because you know that the `a` value will always be true. And even
if you need to use the more complicated safe form, there are good
reasons to do so. For example, there are some cases in Python where `if`
statements are not allowed, such as in `lambda` functions.

### Further Reading on the `and-or` Trick

-   [Python
    Cookbook](http://www.activestate.com/ASPN/Python/Cookbook/ "growing archive of annotated code samples")
    discusses [alternatives to the `and-or`
    trick](http://www.activestate.com/ASPN/Python/Cookbook/Recipe/52310).

  

