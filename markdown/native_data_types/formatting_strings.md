

3.5. Formatting Strings
-----------------------

Python supports formatting values into strings. Although this can
include very complicated expressions, the most basic usage is to insert
values into a string with the `%s` placeholder.


![Note](../images/note.png) 
String formatting in Python uses the same syntax as the `sprintf` function in C. 

### Example 3.21. Introducing String Formatting

    >>> k = "uid"
    >>> v = "sa"
    >>> "%s=%s" % (k, v) 
    'uid=sa'



[![1](../images/callouts/1.png)](#odbchelper.stringformatting.1.1) The whole expression evaluates to a string. The first `%s` is replaced by the value of `k`; the second `%s` is replaced by the value of `v`. All other characters in the string (in this case, the equal sign) stay as they are. 

Note that `(k, v)` is a tuple. I told you they were good for something.

You might be thinking that this is a lot of work just to do simple
string concatentation, and you would be right, except that string
formatting isn't just concatenation. It's not even just formatting. It's
also type coercion.

### Example 3.22. String Formatting vs. Concatenating

    >>> uid = "sa"
    >>> pwd = "secret"
    >>> print pwd + " is not a good password for " + uid      
    secret is not a good password for sa
    >>> print "%s is not a good password for %s" % (pwd, uid) 
    secret is not a good password for sa
    >>> userCount = 6
    >>> print "Users connected: %d" % (userCount, )            
    Users connected: 6
    >>> print "Users connected: " + userCount                 
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    TypeError: cannot concatenate 'str' and 'int' objects



[![1](../images/callouts/1.png)](#odbchelper.stringformatting.2.1) `+` is the string concatenation operator. 

[![2](../images/callouts/2.png)](#odbchelper.stringformatting.2.2) In this trivial case, string formatting accomplishes the same result as concatentation. 

[![3](../images/callouts/3.png)](#odbchelper.stringformatting.2.3) `(userCount, )` is a tuple with one element. Yes, the syntax is a little strange, but there's a good reason for it: it's unambiguously a tuple. In fact, you can always include a comma after the last element when defining a list, tuple, or dictionary, but the comma is required when defining a tuple with one element. If the comma weren't required, Python wouldn't know whether `(userCount)` was a tuple with one element or just the value of `userCount`. 

[![4](../images/callouts/4.png)](#odbchelper.stringformatting.2.4) String formatting works with integers by specifying `%d` instead of `%s`. 

[![5](../images/callouts/5.png)](#odbchelper.stringformatting.2.5) Trying to concatenate a string with a non-string raises an exception. Unlike string formatting, string concatenation works only when everything is already a string. 

As with `printf` in C, string formatting in Python is like a Swiss Army
knife. There are options galore, and modifier strings to specially
format many different types of values.

### Example 3.23. Formatting Numbers

    >>> print "Today's stock price: %f" % 50.4625   
    50.462500
    >>> print "Today's stock price: %.2f" % 50.4625 
    50.46
    >>> print "Change since yesterday: %+.2f" % 1.5 
    +1.50



[![1](../images/callouts/1.png)](#odbchelper.stringformatting.3.1) The `%f` string formatting option treats the value as a decimal, and prints it to six decimal places. 

[![2](../images/callouts/2.png)](#odbchelper.stringformatting.3.2) The ".2" modifier of the `%f` option truncates the value to two decimal places. 

[![3](../images/callouts/3.png)](#odbchelper.stringformatting.3.3) You can even combine modifiers. Adding the `+` modifier displays a plus or minus sign before the value. Note that the ".2" modifier is still in place, and is padding the value to exactly two decimal places. 

### Further Reading on String Formatting

-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the string formatting format
    characters](http://www.python.org/doc/current/lib/typesseq-strings.html).
-   [*Effective AWK
    Programming*](http://www-gnats.gnu.org:8080/cgi-bin/info2www?(gawk)Top)
    discusses [all the format
    characters](http://www-gnats.gnu.org:8080/cgi-bin/info2www?(gawk)Control+Letters)
    and advanced string formatting techniques like [specifying width,
    precision, and
    zero-padding](http://www-gnats.gnu.org:8080/cgi-bin/info2www?(gawk)Format+Modifiers).

  

