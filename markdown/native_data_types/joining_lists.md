

-   [3.7.1. Historical Note on String
    Methods](joining_lists.html#d0e7982)

3.7. Joining Lists and Splitting Strings
----------------------------------------

-   [3.7.1. Historical Note on String
    Methods](joining_lists.html#d0e7982)

You have a list of key-value pairs in the form `key=value`, and you want
to join them into a single string. To join any list of strings into a
single string, use the `join` method of a string object.

Here is an example of joining a list from the `buildConnectionString`
function:

        return ";".join(["%s=%s" % (k, v) for k, v in params.items()])

One interesting note before you continue. I keep repeating that
functions are objects, strings are objects... everything is an object.
You might have thought I meant that string *variables* are objects. But
no, look closely at this example and you'll see that the string `";"`
itself is an object, and you are calling its `join` method.

The `join` method joins the elements of the list into a single string,
with each element separated by a semi-colon. The delimiter doesn't need
to be a semi-colon; it doesn't even need to be a single character. It
can be any string.


![Caution](../images/caution.png) 
`join` works only on lists of strings; it does not do any type coercion. Joining a list that has one or more non-string elements will raise an exception. 

### Example 3.27. Output of `odbchelper.py`

    >>> params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
    >>> ["%s=%s" % (k, v) for k, v in params.items()]
    ['server=mpilgrim', 'uid=sa', 'database=master', 'pwd=secret']
    >>> ";".join(["%s=%s" % (k, v) for k, v in params.items()])
    'server=mpilgrim;uid=sa;database=master;pwd=secret'

This string is then returned from the `odbchelper` function and printed
by the calling block, which gives you the output that you marveled at
when you started reading this chapter.

You're probably wondering if there's an analogous method to split a
string into a list. And of course there is, and it's called `split`.

### Example 3.28. Splitting a String

    >>> li = ['server=mpilgrim', 'uid=sa', 'database=master', 'pwd=secret']
    >>> s = ";".join(li)
    >>> s
    'server=mpilgrim;uid=sa;database=master;pwd=secret'
    >>> s.split(";")    
    ['server=mpilgrim', 'uid=sa', 'database=master', 'pwd=secret']
    >>> s.split(";", 1) 
    ['server=mpilgrim', 'uid=sa;database=master;pwd=secret']



[![1](../images/callouts/1.png)](#odbchelper.join.1.1) `split` reverses `join` by splitting a string into a multi-element list. Note that the delimiter (“`;`”) is stripped out completely; it does not appear in any of the elements of the returned list. 

[![2](../images/callouts/2.png)](#odbchelper.join.1.2) `split` takes an optional second argument, which is the number of times to split. (“"Oooooh, optional arguments...” You'll learn how to do this in your own functions in the next chapter.) 


![Tip](../images/tip.png) 
`anystring.split`(*delimiter*, 1) is a useful technique when you want to search a string for a substring and then work with everything before the substring (which ends up in the first element of the returned list) and everything after it (which ends up in the second element). 

### Further Reading on String Methods

-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    answers [common questions about
    strings](http://www.faqts.com/knowledge-base/index.phtml/fid/480)
    and has a lot of [example code using
    strings](http://www.faqts.com/knowledge-base/index.phtml/fid/539).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the string
    methods](http://www.python.org/doc/current/lib/string-methods.html).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the [`string`
    module](http://www.python.org/doc/current/lib/module-string.html).
-   [*The Whole Python FAQ*](http://www.python.org/doc/FAQ.html)
    explains [why `join` is a string
    method](http://www.python.org/cgi-bin/faqw.py?query=4.96&querytype=simple&casefold=yes&req=search)
    instead of a list method.

### 3.7.1. Historical Note on String Methods

When I first learned Python, I expected `join` to be a method of a list,
which would take the delimiter as an argument. Many people feel the same
way, and there's a story behind the `join` method. Prior to Python 1.6,
strings didn't have all these useful methods. There was a separate
`string` module that contained all the string functions; each function
took a string as its first argument. The functions were deemed important
enough to put onto the strings themselves, which made sense for
functions like `lower`, `upper`, and `split`. But many hard-core Python
programmers objected to the new `join` method, arguing that it should be
a method of the list instead, or that it shouldn't move at all but
simply stay a part of the old `string` module (which still has a lot of
useful stuff in it). I use the new `join` method exclusively, but you
will see code written either way, and if it really bothers you, you can
use the old `string.join` function instead.

  

