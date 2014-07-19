

5.2. Importing Modules Using `from module import`
-------------------------------------------------

Python has two ways of importing modules. Both are useful, and you
should know when to use each. One way, `import module`, you've already
seen in [Section 2.4, “Everything Is an
Object”](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object").
The other way accomplishes the same thing, but it has subtle and
important differences.

Here is the basic `from module import` syntax:

    from UserDict import UserDict

This is similar to the
[`import module`](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string")
syntax that you know and love, but with an important difference: the
attributes and methods of the imported module `types` are imported
directly into the local namespace, so they are available directly,
without qualification by module name. You can import individual items or
use `from module import *` to import everything.


![Note](../images/note.png) 
`from module import *` in Python is like `use module` in Perl; `import module` in Python is like `require module` in Perl. 


![Note](../images/note.png) 
`from module import *` in Python is like `import module.*` in Java; `import module` in Python is like `import module` in Java. 

### Example 5.2. `import module` *vs.* `from module import`

    >>> import types
    >>> types.FunctionType             
    <type 'function'>
    >>> FunctionType                   
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    NameError: There is no variable named 'FunctionType'
    >>> from types import FunctionType 
    >>> FunctionType                   
    <type 'function'>



[![1](../images/callouts/1.png)](#fileinfo.import.1.1) The `types` module contains no methods; it just has attributes for each Python object type. Note that the attribute, `FunctionType`, must be qualified by the module name, `types`. 

[![2](../images/callouts/2.png)](#fileinfo.import.1.2) `FunctionType` by itself has not been defined in this namespace; it exists only in the context of `types`. 

[![3](../images/callouts/3.png)](#fileinfo.import.1.3) This syntax imports the attribute `FunctionType` from the `types` module directly into the local namespace. 

[![4](../images/callouts/4.png)](#fileinfo.import.1.4) Now `FunctionType` can be accessed directly, without reference to `types`. 

When should you use `from module import`?

-   If you will be accessing attributes and methods often and don't want
    to type the module name over and over, use `from module import`.
-   If you want to selectively import some attributes and methods but
    not others, use `from module import`.
-   If the module contains attributes or functions with the same name as
    ones in your module, you must use `import module` to avoid name
    conflicts.

Other than that, it's just a matter of style, and you will see Python
code written both ways.


![Caution](../images/caution.png) 
Use `from module import *` sparingly, because it makes it difficult to determine where a particular function or attribute came from, and that makes debugging and refactoring more difficult. 

### Further Reading on Module Importing Techniques

-   [eff-bot](http://www.effbot.org/guides/) has more to say on
    [`import module` *vs.*
    `from module import`](http://www.effbot.org/guides/import-confusion.htm).
-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses advanced import techniques, including
    [`from module import *`](http://www.python.org/doc/current/tut/node8.html#SECTION008410000000000000000).

  

