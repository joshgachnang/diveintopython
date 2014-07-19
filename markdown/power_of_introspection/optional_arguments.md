

4.2. Using Optional and Named Arguments
---------------------------------------

Python allows function arguments to have default values; if the function
is called without the argument, the argument gets its default value.
Futhermore, arguments can be specified in any order by using named
arguments. Stored procedures in SQL Server Transact/SQL can do this, so
if you're a SQL Server scripting guru, you can skim this part.

Here is an example of `info`, a function with two optional arguments:

    def info(object, spacing=10, collapse=1):

`spacing` and `collapse` are optional, because they have default values
defined. `object` is required, because it has no default value. If
`info` is called with only one argument, `spacing` defaults to `10` and
`collapse` defaults to `1`. If `info` is called with two arguments,
`collapse` still defaults to `1`.

Say you want to specify a value for `collapse` but want to accept the
default value for `spacing`. In most languages, you would be out of
luck, because you would need to call the function with three arguments.
But in Python, arguments can be specified by name, in any order.

### Example 4.4. Valid Calls of `info`

    info(odbchelper)                    
    info(odbchelper, 12)                
    info(odbchelper, collapse=0)        
    info(spacing=15, object=odbchelper) 



[![1](../images/callouts/1.png)](#apihelper_args.1.1) With only one argument, `spacing` gets its default value of `10` and `collapse` gets its default value of `1`. 

[![2](../images/callouts/2.png)](#apihelper_args.1.2) With two arguments, `collapse` gets its default value of `1`. 

[![3](../images/callouts/3.png)](#apihelper_args.1.3) Here you are naming the `collapse` argument explicitly and specifying its value. `spacing` still gets its default value of `10`. 

[![4](../images/callouts/4.png)](#apihelper_args.1.4) Even required arguments (like `object`, which has no default value) can be named, and named arguments can appear in any order. 

This looks totally whacked until you realize that arguments are simply a
dictionary. The “normal” method of calling functions without argument
names is actually just a shorthand where Python matches up the values
with the argument names in the order they're specified in the function
declaration. And most of the time, you'll call functions the “normal”
way, but you always have the additional flexibility if you need it.


![Note](../images/note.png) 
The only thing you need to do to call a function is specify a value (somehow) for each required argument; the manner and order in which you do that is up to you. 

### Further Reading on Optional Arguments

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses exactly [when and how default arguments are
    evaluated](http://www.python.org/doc/current/tut/node6.html#SECTION006710000000000000000),
    which matters when the default value is a list or an expression with
    side effects.

  

