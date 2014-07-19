

8.8. Introducing `dialect.py`
-----------------------------

`Dialectizer` is a simple (and silly) descendant of `BaseHTMLProcessor`.
It runs blocks of text through a series of substitutions, but it makes
sure that anything within a `<pre>`...`</pre>` block passes through
unaltered.

To handle the `<pre>` blocks, you define two methods in `Dialectizer`:
`start_pre` and `end_pre`.

### Example 8.17. Handling specific tags

        def start_pre(self, attrs):             
            self.verbatim += 1                  
            self.unknown_starttag("pre", attrs) 

        def end_pre(self):                      
            self.unknown_endtag("pre")          
            self.verbatim -= 1                  



[![1](../images/callouts/1.png)](#dialect.dialectizer.1.1) `start_pre` is called every time `SGMLParser` finds a `<pre>` tag in the HTML source. (In a minute, you'll see exactly how this happens.) The method takes a single parameter, `attrs`, which contains the attributes of the tag (if any). `attrs` is a list of key/value tuples, just like [`unknown_starttag`](dictionary_based_string_formatting.html#dialect.unknownstarttag "Example 8.14. Dictionary-based string formatting in BaseHTMLProcessor.py") takes. 

[![2](../images/callouts/2.png)](#dialect.dialectizer.1.2) In the `reset` method, you initialize a data attribute that serves as a counter for `<pre>` tags. Every time you hit a `<pre>` tag, you increment the counter; every time you hit a `</pre>` tag, you'll decrement the counter. (You could just use this as a flag and set it to `1` and reset it to `0`, but it's just as easy to do it this way, and this handles the odd (but possible) case of nested `<pre>` tags.) In a minute, you'll see how this counter is put to good use. 

[![3](../images/callouts/3.png)](#dialect.dialectizer.1.3) That's it, that's the only special processing you do for `<pre>` tags. Now you pass the list of attributes along to `unknown_starttag` so it can do the default processing. 

[![4](../images/callouts/4.png)](#dialect.dialectizer.1.4) `end_pre` is called every time `SGMLParser` finds a `</pre>` tag. Since end tags can not contain attributes, the method takes no parameters. 

[![5](../images/callouts/5.png)](#dialect.dialectizer.1.5) First, you want to do the default processing, just like any other end tag. 

[![6](../images/callouts/6.png)](#dialect.dialectizer.1.6) Second, you decrement your counter to signal that this `<pre>` block has been closed. 

At this point, it's worth digging a little further into `SGMLParser`.
I've claimed repeatedly (and you've taken it on faith so far) that
`SGMLParser` looks for and calls specific methods for each tag, if they
exist. For instance, you just saw the definition of `start_pre` and
`end_pre` to handle `<pre>` and `</pre>`. But how does this happen?
Well, it's not magic, it's just good Python coding.

### Example 8.18. `SGMLParser`

        def finish_starttag(self, tag, attrs):               
            try:                                            
                method = getattr(self, 'start_' + tag)       
            except AttributeError:                           
                try:                                        
                    method = getattr(self, 'do_' + tag)      
                except AttributeError:                      
                    self.unknown_starttag(tag, attrs)        
                    return -1                               
                else:                                       
                    self.handle_starttag(tag, method, attrs) 
                    return 0                                
            else:                                           
                self.stack.append(tag)                      
                self.handle_starttag(tag, method, attrs)    
                return 1                                     

        def handle_starttag(self, tag, method, attrs):      
            method(attrs)                                    



[![1](../images/callouts/1.png)](#dialect.dialectizer.2.1) At this point, `SGMLParser` has already found a start tag and parsed the attribute list. The only thing left to do is figure out whether there is a specific handler method for this tag, or whether you should fall back on the default method (`unknown_starttag`). 

[![2](../images/callouts/2.png)](#dialect.dialectizer.2.2) The “magic” of `SGMLParser` is nothing more than your old friend, [`getattr`](../power_of_introspection/getattr.html "4.4. Getting Object References With getattr"). What you may not have realized before is that `getattr` will find methods defined in descendants of an object as well as the object itself. Here the object is `self`, the current instance. So if `tag` is `'pre'`, this call to `getattr` will look for a `start_pre` method on the current instance, which is an instance of the `Dialectizer` class. 

[![3](../images/callouts/3.png)](#dialect.dialectizer.2.3) `getattr` raises an `AttributeError` if the method it's looking for doesn't exist in the object (or any of its descendants), but that's okay, because you wrapped the call to `getattr` inside a [`try...except`](../file_handling/index.html#fileinfo.exception "6.1. Handling Exceptions") block and explicitly caught the `AttributeError`. 

[![4](../images/callouts/4.png)](#dialect.dialectizer.2.4) Since you didn't find a `start_xxx` method, you'll also look for a `do_xxx` method before giving up. This alternate naming scheme is generally used for standalone tags, like `<br>`, which have no corresponding end tag. But you can use either naming scheme; as you can see, `SGMLParser` tries both for every tag. (You shouldn't define both a `start_xxx` and `do_xxx` handler method for the same tag, though; only the `start_xxx` method will get called.) 

[![5](../images/callouts/5.png)](#dialect.dialectizer.2.5) Another `AttributeError`, which means that the call to `getattr` failed with `do_xxx`. Since you found neither a `start_xxx` nor a `do_xxx` method for this tag, you catch the exception and fall back on the default method, `unknown_starttag`. 

[![6](../images/callouts/6.png)](#dialect.dialectizer.2.6) Remember, `try...except` blocks can have an `else` clause, which is called if [no exception is raised](../file_handling/index.html#crossplatform.example "Example 6.2. Supporting Platform-Specific Functionality") during the `try...except` block. Logically, that means that you *did* find a `do_xxx` method for this tag, so you're going to call it. 

[![7](../images/callouts/7.png)](#dialect.dialectizer.2.7) By the way, don't worry about these different return values; in theory they mean something, but they're never actually used. Don't worry about the `self.stack.append(tag)` either; `SGMLParser` keeps track internally of whether your start tags are balanced by appropriate end tags, but it doesn't do anything with this information either. In theory, you could use this module to validate that your tags were fully balanced, but it's probably not worth it, and it's beyond the scope of this chapter. You have better things to worry about right now. 

[![8](../images/callouts/8.png)](#dialect.dialectizer.2.8) `start_xxx` and `do_xxx` methods are not called directly; the tag, method, and attributes are passed to this function, `handle_starttag`, so that descendants can override it and change the way *all* start tags are dispatched. You don't need that level of control, so you just let this method do its thing, which is to call the method (`start_xxx` or `do_xxx`) with the list of attributes. Remember, `method` is a function, returned from `getattr`, and functions are objects. (I know you're getting tired of hearing it, and I promise I'll stop saying it as soon as I run out of ways to use it to my advantage.) Here, the function object is passed into this dispatch method as an argument, and this method turns around and calls the function. At this point, you don't need to know what the function is, what it's named, or where it's defined; the only thing you need to know about the function is that it is called with one argument, `attrs`. 

Now back to our regularly scheduled program: `Dialectizer`. When you
left, you were in the process of defining specific handler methods for
`<pre>` and `</pre>` tags. There's only one thing left to do, and that
is to process text blocks with the pre-defined substitutions. For that,
you need to override the `handle_data` method.

### Example 8.19. Overriding the `handle_data` method

        def handle_data(self, text):                                         
            self.pieces.append(self.verbatim and text or self.process(text)) 



[![1](../images/callouts/1.png)](#dialect.dialectizer.3.1) `handle_data` is called with only one argument, the text to process. 

[![2](../images/callouts/2.png)](#dialect.dialectizer.3.2) In the ancestor [`BaseHTMLProcessor`](basehtmlprocessor.html#dialect.basehtml.intro "Example 8.8. Introducing BaseHTMLProcessor"), the `handle_data` method simply appended the text to the output buffer, `self.pieces`. Here the logic is only slightly more complicated. If you're in the middle of a `<pre>`...`</pre>` block, `self.verbatim` will be some value greater than `0`, and you want to put the text in the output buffer unaltered. Otherwise, you will call a separate method to process the substitutions, then put the result of that into the output buffer. In Python, this is a one-liner, using [the `and-or` trick](../power_of_introspection/and_or.html#apihelper.andortrick.intro "Example 4.17. Introducing the and-or Trick"). 

You're close to completely understanding `Dialectizer`. The only missing
link is the nature of the text substitutions themselves. If you know any
Perl, you know that when complex text substitutions are required, the
only real solution is regular expressions. The classes later in
`dialect.py` define a series of regular expressions that operate on the
text between the HTML tags. But you just had [a whole chapter on regular
expressions](../regular_expressions/index.html "Chapter 7. Regular Expressions").
You don't really want to slog through regular expressions again, do you?
God knows I don't. I think you've learned enough for one chapter.

  

