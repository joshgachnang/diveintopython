

9.2. Packages
-------------

Actually parsing an XML document is very simple: one line of code.
However, before you get to that line of code, you need to take a short
detour to talk about packages.

### Example 9.5. Loading an XML document (a sneak peek)

    >>> from xml.dom import minidom 
    >>> xmldoc = minidom.parse('~/diveintopython/common/py/kgp/binary.xml')



[![1](../images/callouts/1.png)](#kgp.packages.1.1) This is a syntax you haven't seen before. It looks almost like the `from module import` you know and love, but the `"."` gives it away as something above and beyond a simple import. In fact, `xml` is what is known as a package, `dom` is a nested package within `xml`, and `minidom` is a module within `xml.dom`. 

That sounds complicated, but it's really not. Looking at the actual
implementation may help. Packages are little more than directories of
modules; nested packages are subdirectories. The modules within a
package (or a nested package) are still just `.py` files, like always,
except that they're in a subdirectory instead of the main `lib/`
directory of your Python installation.

### Example 9.6. File layout of a package

    Python21/           root Python installation (home of the executable)
     
    +--lib/             library directory (home of the standard library modules)
        
       +-- xml/         xml package (really just a directory with other stuff in it)
            
           +--sax/      xml.sax package (again, just a directory)
            
           +--dom/      xml.dom package (contains minidom.py)
            
           +--parsers/  xml.parsers package (used internally)

So when you say `from xml.dom import minidom`, Python figures out that
that means “look in the `xml` directory for a `dom` directory, and look
in *that* for the `minidom` module, and import it as `minidom`”. But
Python is even smarter than that; not only can you import entire modules
contained within a package, you can selectively import specific classes
or functions from a module contained within a package. You can also
import the package itself as a module. The syntax is all the same;
Python figures out what you mean based on the file layout of the
package, and automatically does the right thing.

### Example 9.7. Packages are modules, too

    >>> from xml.dom import minidom         
    >>> minidom
    <module 'xml.dom.minidom' from 'C:\Python21\lib\xml\dom\minidom.pyc'>
    >>> minidom.Element
    <class xml.dom.minidom.Element at 01095744>
    >>> from xml.dom.minidom import Element 
    >>> Element
    <class xml.dom.minidom.Element at 01095744>
    >>> minidom.Element
    <class xml.dom.minidom.Element at 01095744>
    >>> from xml import dom                 
    >>> dom
    <module 'xml.dom' from 'C:\Python21\lib\xml\dom\__init__.pyc'>
    >>> import xml                          
    >>> xml
    <module 'xml' from 'C:\Python21\lib\xml\__init__.pyc'>



[![1](../images/callouts/1.png)](#kgp.packages.2.1) Here you're importing a module (`minidom`) from a nested package (`xml.dom`). The result is that `minidom` is imported into your [namespace](../html_processing/locals_and_globals.html "8.5. locals and globals"), and in order to reference classes within the `minidom` module (like `Element`), you need to preface them with the module name. 

[![2](../images/callouts/2.png)](#kgp.packages.2.2) Here you are importing a class (`Element`) from a module (`minidom`) from a nested package (`xml.dom`). The result is that `Element` is imported directly into your namespace. Note that this does not interfere with the previous import; the `Element` class can now be referenced in two ways (but it's all still the same class). 

[![3](../images/callouts/3.png)](#kgp.packages.2.3) Here you are importing the `dom` package (a nested package of `xml`) as a module in and of itself. Any level of a package can be treated as a module, as you'll see in a moment. It can even have its own attributes and methods, just the modules you've seen before. 

[![4](../images/callouts/4.png)](#kgp.packages.2.4) Here you are importing the root level `xml` package as a module. 

So how can a package (which is just a directory on disk) be imported and
treated as a module (which is always a file on disk)? The answer is the
magical `__init__.py` file. You see, packages are not simply
directories; they are directories with a specific file, `__init__.py`,
inside. This file defines the attributes and methods of the package. For
instance, `xml.dom` contains a `Node` class, which is defined in
`xml/dom/__init__.py`. When you import a package as a module (like `dom`
from `xml`), you're really importing its `__init__.py` file.


![Note](../images/note.png) 
A package is a directory with the special `__init__.py` file in it. The `__init__.py` file defines the attributes and methods of the package. It doesn't need to define anything; it can just be an empty file, but it has to exist. But if `__init__.py` doesn't exist, the directory is just a directory, not a package, and it can't be imported or contain modules or nested packages. 

So why bother with packages? Well, they provide a way to logically group
related modules. Instead of having an `xml` package with `sax` and `dom`
packages inside, the authors could have chosen to put all the `sax`
functionality in `xmlsax.py` and all the `dom` functionality in
`xmldom.py`, or even put all of it in a single module. But that would
have been unwieldy (as of this writing, the XML package has over 3000
lines of code) and difficult to manage (separate source files mean
multiple people can work on different areas simultaneously).

If you ever find yourself writing a large subsystem in Python (or, more
likely, when you realize that your small subsystem has grown into a
large one), invest some time designing a good package architecture. It's
one of the many things Python is good at, so take advantage of it.

  

