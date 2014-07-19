

8.9. Putting it all together
----------------------------

It's time to put everything you've learned so far to good use. I hope
you were paying attention.

### Example 8.20. The `translate` function, part 1

    def translate(url, dialectName="chef"): 
        import urllib                       
        sock = urllib.urlopen(url)          
        htmlSource = sock.read()           
        sock.close()                       



[![1](../images/callouts/1.png)](#dialect.alltogether.1.1) The `translate` function has an [optional argument](../power_of_introspection/optional_arguments.html "4.2. Using Optional and Named Arguments") `dialectName`, which is a string that specifies the dialect you'll be using. You'll see how this is used in a minute. 

[![2](../images/callouts/2.png)](#dialect.alltogether.1.2) Hey, wait a minute, there's an [`import`](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string") statement in this function! That's perfectly legal in Python. You're used to seeing `import` statements at the top of a program, which means that the imported module is available anywhere in the program. But you can also import modules within a function, which means that the imported module is only available within the function. If you have a module that is only ever used in one function, this is an easy way to make your code more modular. (When you find that your weekend hack has turned into an 800-line work of art and decide to split it up into a dozen reusable modules, you'll appreciate this.) 

[![3](../images/callouts/3.png)](#dialect.alltogether.1.3) Now you [get the source of the given URL](extracting_data.html#dialect.extract.urllib "Example 8.5. Introducing urllib"). 

### Example 8.21. The `translate` function, part 2: curiouser and curiouser

        parserName = "%sDialectizer" % dialectName.capitalize() 
        parserClass = globals()[parserName]                     
        parser = parserClass()                                  



[![1](../images/callouts/1.png)](#dialect.alltogether.2.1) `capitalize` is a string method you haven't seen before; it simply capitalizes the first letter of a string and forces everything else to lowercase. Combined with some [string formatting](../native_data_types/formatting_strings.html "3.5. Formatting Strings"), you've taken the name of a dialect and transformed it into the name of the corresponding Dialectizer class. If `dialectName` is the string `'chef'`, `parserName` will be the string `'ChefDialectizer'`. 

[![2](../images/callouts/2.png)](#dialect.alltogether.2.2) You have the name of a class as a string (`parserName`), and you have the global namespace as a dictionary (`globals`()). Combined, you can get a reference to the class which the string names. (Remember, [classes are objects](../object_oriented_framework/class_attributes.html "5.8. Introducing Class Attributes"), and they can be assigned to variables just like any other object.) If `parserName` is the string `'ChefDialectizer'`, `parserClass` will be the class `ChefDialectizer`. 

[![3](../images/callouts/3.png)](#dialect.alltogether.2.3) Finally, you have a class object (`parserClass`), and you want an instance of the class. Well, you already know how to do that: [call the class like a function](../object_oriented_framework/instantiating_classes.html "5.4. Instantiating Classes"). The fact that the class is being stored in a local variable makes absolutely no difference; you just call the local variable like a function, and out pops an instance of the class. If `parserClass` is the class `ChefDialectizer`, `parser` will be an instance of the class `ChefDialectizer`. 

Why bother? After all, there are only 3 `Dialectizer` classes; why not
just use a `case` statement? (Well, there's no `case` statement in
Python, but why not just use a series of `if` statements?) One reason:
extensibility. The `translate` function has absolutely no idea how many
Dialectizer classes you've defined. Imagine if you defined a new
`FooDialectizer` tomorrow; `translate` would work by passing `'foo'` as
the `dialectName`.

Even better, imagine putting `FooDialectizer` in a separate module, and
importing it with `from module import`. You've already seen that this
[includes it in
`globals`()](locals_and_globals.html#dialect.globals.example "Example 8.11. Introducing globals"),
so `translate` would still work without modification, even though
`FooDialectizer` was in a separate file.

Now imagine that the name of the dialect is coming from somewhere
outside the program, maybe from a database or from a user-inputted value
on a form. You can use any number of server-side Python scripting
architectures to dynamically generate web pages; this function could
take a URL and a dialect name (both strings) in the query string of a
web page request, and output the “translated” web page.

Finally, imagine a `Dialectizer` framework with a plug-in architecture.
You could put each `Dialectizer` class in a separate file, leaving only
the `translate` function in `dialect.py`. Assuming a consistent naming
scheme, the `translate` function could dynamic import the appropiate
class from the appropriate file, given nothing but the dialect name.
(You haven't seen dynamic importing yet, but I promise to cover it in a
later chapter.) To add a new dialect, you would simply add an
appropriately-named file in the plug-ins directory (like `foodialect.py`
which contains the `FooDialectizer` class). Calling the `translate`
function with the dialect name `'foo'` would find the module
`foodialect.py`, import the class `FooDialectizer`, and away you go.

### Example 8.22. The `translate` function, part 3

        parser.feed(htmlSource) 
        parser.close()          
        return parser.output()  



[![1](../images/callouts/1.png)](#dialect.alltogether.3.1) After all that imagining, this is going to seem pretty boring, but the `feed` function is what [does the entire transformation](extracting_data.html#dialect.feed.example "Example 8.7. Using urllister.py"). You had the entire HTML source in a single string, so you only had to call `feed` once. However, you can call `feed` as often as you want, and the parser will just keep parsing. So if you were worried about memory usage (or you knew you were going to be dealing with very large HTML pages), you could set this up in a loop, where you read a few bytes of HTML and fed it to the parser. The result would be the same. 

[![2](../images/callouts/2.png)](#dialect.alltogether.3.2) Because `feed` maintains an internal buffer, you should always call the parser's `close` method when you're done (even if you fed it all at once, like you did). Otherwise you may find that your output is missing the last few bytes. 

[![3](../images/callouts/3.png)](#dialect.alltogether.3.3) Remember, `output` is the function you defined on `BaseHTMLProcessor` that [joins all the pieces of output you've buffered](basehtmlprocessor.html#dialect.output.example "Example 8.9. BaseHTMLProcessor output") and returns them in a single string. 

And just like that, you've “translated” a web page, given nothing but a
URL and the name of a dialect.

### Further reading

-   You thought I was kidding about the server-side scripting idea. So
    did I, until I found [this web-based
    dialectizer](http://rinkworks.com/dialect/). Unfortunately, source
    code does not appear to be available.

  

