

8.5. `locals` and `globals`
---------------------------

Let's digress from HTML processing for a minute and talk about how
Python handles variables. Python has two built-in functions, `locals`
and `globals`, which provide dictionary-based access to local and global
variables.

Remember `locals`? You first saw it here:

        def unknown_starttag(self, tag, attrs):
            strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs])
            self.pieces.append("<%(tag)s%(strattrs)s>" % locals())

No, wait, you can't learn about `locals` yet. First, you need to learn
about namespaces. This is dry stuff, but it's important, so pay
attention.

Python uses what are called namespaces to keep track of variables. A
namespace is just like a dictionary where the keys are names of
variables and the dictionary values are the values of those variables.
In fact, you can access a namespace as a Python dictionary, as you'll
see in a minute.

At any particular point in a Python program, there are several
namespaces available. Each function has its own namespace, called the
local namespace, which keeps track of the function's variables,
including function arguments and locally defined variables. Each module
has its own namespace, called the global namespace, which keeps track of
the module's variables, including functions, classes, any other imported
modules, and module-level variables and constants. And there is the
built-in namespace, accessible from any module, which holds built-in
functions and exceptions.

When a line of code asks for the value of a variable `x`, Python will
search for that variable in all the available namespaces, in order:

1.  local namespace - specific to the current function or class method.
    If the function defines a local variable `x`, or has an argument
    `x`, Python will use this and stop searching.
2.  global namespace - specific to the current module. If the module has
    defined a variable, function, or class called `x`, Python will use
    that and stop searching.
3.  built-in namespace - global to all modules. As a last resort, Python
    will assume that `x` is the name of built-in function or variable.

If Python doesn't find `x` in any of these namespaces, it gives up and
raises a `NameError` with the message `There is no variable named 'x'`,
which you saw back in [Example 3.18, “Referencing an Unbound
Variable”](../native_data_types/declaring_variables.html#odbchelper.unboundvariable "Example 3.18. Referencing an Unbound Variable"),
but you didn't appreciate how much work Python was doing before giving
you that error.

<table>
<col width="100%" />
<tbody>
<tr class="odd">
<td align="left"><img src="../images/important.png" alt="Important" /></td>
</tr>
<tr class="even">
<td align="left">Python 2.2 introduced a subtle but important change that affects the namespace search order: nested scopes. In versions of Python prior to 2.2, when you reference a variable within a <a href="../file_handling/all_together.html#fileinfo.nested" title="Example 6.21. listDirectory">nested function</a> or <a href="../power_of_introspection/lambda_functions.html" title="4.7. Using lambda Functions"><code class="literal">lambda</code> function</a>, Python will search for that variable in the current (nested or <code class="literal">lambda</code>) function's namespace, then in the module's namespace. Python 2.2 will search for the variable in the current (nested or <code class="literal">lambda</code>) function's namespace, <em>then in the parent function's namespace</em>, then in the module's namespace. Python 2.1 can work either way; by default, it works like Python 2.0, but you can add the following line of code at the top of your module to make your module work like Python 2.2:
<pre class="programlisting"><code>from __future__ import nested_scopes</code></pre></td>
</tr>
</tbody>
</table>

Are you confused yet? Don't despair! This is really cool, I promise.
Like many things in Python, namespaces are *directly accessible at
run-time*. How? Well, the local namespace is accessible via the built-in
`locals` function, and the global (module level) namespace is accessible
via the built-in `globals` function.

### Example 8.10. Introducing `locals`

    >>> def foo(arg): 
    ...     x = 1
    ...     print locals()
    ...     
    >>> foo(7)        
    {'arg': 7, 'x': 1}
    >>> foo('bar')    
    {'arg': 'bar', 'x': 1}



[![1](../images/callouts/1.png)](#dialect.locals.1.1) The function `foo` has two variables in its local namespace: `arg`, whose value is passed in to the function, and `x`, which is defined within the function. 

[![2](../images/callouts/2.png)](#dialect.locals.1.2) `locals` returns a dictionary of name/value pairs. The keys of this dictionary are the names of the variables as strings; the values of the dictionary are the actual values of the variables. So calling `foo` with `7` prints the dictionary containing the function's two local variables: `arg` (`7`) and `x` (`1`). 

[![3](../images/callouts/3.png)](#dialect.locals.1.3) Remember, Python has dynamic typing, so you could just as easily pass a string in for `arg`; the function (and the call to `locals`) would still work just as well. `locals` works with all variables of all datatypes. 

What `locals` does for the local (function) namespace, `globals` does
for the global (module) namespace. `globals` is more exciting, though,
because a module's namespace is more
exciting.<sup>[[3](#ftn.d0e21226)]</sup> Not only does the module's
namespace include module-level variables and constants, it includes all
the functions and classes defined in the module. Plus, it includes
anything that was imported into the module.

Remember the difference between
[`from module import`](../object_oriented_framework/importing_modules.html "5.2. Importing Modules Using from module import")
and
[`import module`](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string")?
With `import module`, the module itself is imported, but it retains its
own namespace, which is why you need to use the module name to access
any of its functions or attributes: `module.function`. But with
`from module import`, you're actually importing specific functions and
attributes from another module into your own namespace, which is why you
access them directly without referencing the original module they came
from. With the `globals` function, you can actually see this happen.

### Example 8.11. Introducing `globals`

Look at the following block of code at the bottom of
`BaseHTMLProcessor.py`:

    if __name__ == "__main__":
        for k, v in globals().items():             
            print k, "=", v



[![1](../images/callouts/1.png)](#dialect.locals.2.1) Just so you don't get intimidated, remember that you've seen all this before. The `globals` function returns a dictionary, and you're [iterating through the dictionary](../file_handling/for_loops.html#dictionaryiter.example "Example 6.10. Iterating Through a Dictionary") using the `items` method and [multi-variable assignment](../native_data_types/declaring_variables.html#odbchelper.multiassign "3.4.2. Assigning Multiple Values at Once"). The only thing new here is the `globals` function. 

Now running the script from the command line gives this output (note
that your output may be slightly different, depending on your platform
and where you installed Python):

    c:\docbook\dip\py> python BaseHTMLProcessor.py

    SGMLParser = sgmllib.SGMLParser                
    htmlentitydefs = <module 'htmlentitydefs' from 'C:\Python23\lib\htmlentitydefs.py'> 
    BaseHTMLProcessor = __main__.BaseHTMLProcessor 
    __name__ = __main__                            
    ... rest of output omitted for brevity...



[![1](../images/callouts/1.png)](#dialect.locals.3.1) `SGMLParser` was imported from `sgmllib`, using `from module import`. That means that it was imported directly into the module's namespace, and here it is. 

[![2](../images/callouts/2.png)](#dialect.locals.3.2) Contrast this with `htmlentitydefs`, which was imported using `import`. That means that the `htmlentitydefs` module itself is in the namespace, but the `entitydefs` variable defined within `htmlentitydefs` is not. 

[![3](../images/callouts/3.png)](#dialect.locals.3.3) This module only defines one class, `BaseHTMLProcessor`, and here it is. Note that the value here is [the class itself](../object_oriented_framework/class_attributes.html#fileinfo.classattributes.intro "Example 5.17. Introducing Class Attributes"), not a specific instance of the class. 

[![4](../images/callouts/4.png)](#dialect.locals.3.4) Remember the [`if __name__` trick](../getting_to_know_python/testing_modules.html#odbchelper.ifnametrick)? When running a module (as opposed to importing it from another module), the built-in `__name__` attribute is a special value, `__main__`. Since you ran this module as a script from the command line, `__name__` is `__main__`, which is why the little test code to print the `globals` got executed. 


![Note](../images/note.png) 
Using the `locals` and `globals` functions, you can get the value of arbitrary variables dynamically, providing the variable name as a string. This mirrors the functionality of the [`getattr`](../power_of_introspection/getattr.html "4.4. Getting Object References With getattr") function, which allows you to access arbitrary functions dynamically by providing the function name as a string. 

There is one other important difference between the `locals` and
`globals` functions, which you should learn now before it bites you. It
will bite you anyway, but at least then you'll remember learning it.

### Example 8.12. `locals` is read-only, `globals` is not

    def foo(arg):
        x = 1
        print locals()    
        locals()["x"] = 2 
        print "x=",x      

    z = 7
    print "z=",z
    foo(3)
    globals()["z"] = 8    
    print "z=",z          



[![1](../images/callouts/1.png)](#dialect.locals.4.1) Since `foo` is called with `3`, this will print `{'arg': 3, 'x': 1}`. This should not be a surprise. 

[![2](../images/callouts/2.png)](#dialect.locals.4.2) `locals` is a function that returns a dictionary, and here you are setting a value in that dictionary. You might think that this would change the value of the local variable `x` to `2`, but it doesn't. `locals` does not actually return the local namespace, it returns a copy. So changing it does nothing to the value of the variables in the local namespace. 

[![3](../images/callouts/3.png)](#dialect.locals.4.3) This prints `x= 1`, not `x= 2`. 

[![4](../images/callouts/4.png)](#dialect.locals.4.4) After being burned by `locals`, you might think that this *wouldn't* change the value of `z`, but it does. Due to internal differences in how Python is implemented (which I'd rather not go into, since I don't fully understand them myself), `globals` returns the actual global namespace, not a copy: the exact opposite behavior of `locals`. So any changes to the dictionary returned by `globals` directly affect your global variables. 

[![5](../images/callouts/5.png)](#dialect.locals.4.5) This prints `z= 8`, not `z= 7`. 

### Footnotes

<sup>[[3](#d0e21226)]</sup>I don't get out much.

  

