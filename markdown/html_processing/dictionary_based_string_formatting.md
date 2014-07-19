

8.6. Dictionary-based string formatting
---------------------------------------

Why did you learn about `locals` and `globals`? So you can learn about
dictionary-based string formatting. As you recall, [regular string
formatting](../native_data_types/formatting_strings.html "3.5. Formatting Strings")
provides an easy way to insert values into strings. Values are listed in
a tuple and inserted in order into the string in place of each
formatting marker. While this is efficient, it is not always the easiest
code to read, especially when multiple values are being inserted. You
can't simply scan through the string in one pass and understand what the
result will be; you're constantly switching between reading the string
and reading the tuple of values.

There is an alternative form of string formatting that uses dictionaries
instead of tuples of values.

### Example 8.13. Introducing dictionary-based string formatting

    >>> params = {"server":"mpilgrim", "database":"master", "uid":"sa", "pwd":"secret"}
    >>> "%(pwd)s" % params                                    
    'secret'
    >>> "%(pwd)s is not a good password for %(uid)s" % params 
    'secret is not a good password for sa'
    >>> "%(database)s of mind, %(database)s of body" % params 
    'master of mind, master of body'



[![1](../images/callouts/1.png)](#dialect.dictsub.1.1) Instead of a tuple of explicit values, this form of string formatting uses a dictionary, `params`. And instead of a simple `%s` marker in the string, the marker contains a name in parentheses. This name is used as a key in the `params` dictionary and subsitutes the corresponding value, `secret`, in place of the `%(pwd)s` marker. 

[![2](../images/callouts/2.png)](#dialect.dictsub.1.2) Dictionary-based string formatting works with any number of named keys. Each key must exist in the given dictionary, or the formatting will fail with a `KeyError`. 

[![3](../images/callouts/3.png)](#dialect.dictsub.1.3) You can even specify the same key twice; each occurrence will be replaced with the same value. 

So why would you use dictionary-based string formatting? Well, it does
seem like overkill to set up a dictionary of keys and values simply to
do string formatting in the next line; it's really most useful when you
happen to have a dictionary of meaningful keys and values already. Like
[`locals`](locals_and_globals.html "8.5. locals and globals").

### Example 8.14. Dictionary-based string formatting in `BaseHTMLProcessor.py`

        def handle_comment(self, text):        
            self.pieces.append("<!--%(text)s-->" % locals()) 



[![1](../images/callouts/1.png)](#dialect.dictsub.2.1) Using the built-in `locals` function is the most common use of dictionary-based string formatting. It means that you can use the names of local variables within your string (in this case, `text`, which was passed to the class method as an argument) and each named variable will be replaced by its value. If `text` is `'Begin page footer'`, the string formatting `"<!--%(text)s-->" % locals()` will resolve to the string `'<!--Begin page footer-->'`. 

### Example 8.15. More dictionary-based string formatting

        def unknown_starttag(self, tag, attrs):
            strattrs = "".join([' %s="%s"' % (key, value) for key, value in attrs]) 
            self.pieces.append("<%(tag)s%(strattrs)s>" % locals())                      

<table>
<col width="50%" />
<col width="50%" />
<tbody>
<tr class="odd">
<td align="left"><a href="#dialect.dictsub.3.1"><img src="../images/callouts/1.png" alt="1" /></a></td>
<td align="left">When this method is called, <code class="varname">attrs</code> is a list of key/value tuples, just like the <a href="../native_data_types/mapping_lists.html#odbchelper.items" title="Example 3.25. The keys, values, and items Functions"><code class="function">items</code> of a dictionary</a>, which means you can use <a href="../native_data_types/declaring_variables.html#odbchelper.multiassign" title="3.4.2. Assigning Multiple Values at Once">multi-variable assignment</a> to iterate through it. This should be a familiar pattern by now, but there's a lot going on here, so let's break it down:
<ol>
<li>Suppose <code class="varname">attrs</code> is <code class="literal">[('href', 'index.html'), ('title', 'Go to home page')]</code>.</li>
<li>In the first round of the list comprehension, <code class="varname">key</code> will get <code class="literal">'href'</code>, and <code class="varname">value</code> will get <code class="literal">'index.html'</code>.</li>
<li>The string formatting <code class="literal">' %s=&quot;%s&quot;' % (key, value)</code> will resolve to <code class="literal">' href=&quot;index.html&quot;'</code>. This string becomes the first element of the list comprehension's return value.</li>
<li>In the second round, <code class="varname">key</code> will get <code class="literal">'title'</code>, and <code class="varname">value</code> will get <code class="literal">'Go to home page'</code>.</li>
<li>The string formatting will resolve to <code class="literal">' title=&quot;Go to home page&quot;'</code>.</li>
<li>The list comprehension returns a list of these two resolved strings, and <code class="varname">strattrs</code> will join both elements of this list together to form <code class="literal">' href=&quot;index.html&quot; title=&quot;Go to home page&quot;'</code>.</li>
</ol></td>
</tr>
<tr class="even">
<td align="left"><a href="#dialect.dictsub.3.2"><img src="../images/callouts/2.png" alt="2" /></a></td>
<td align="left">Now, using dictionary-based string formatting, you insert the value of <code class="varname">tag</code> and <code class="varname">strattrs</code> into a string. So if <code class="varname">tag</code> is <code class="literal">'a'</code>, the final result would be <code class="literal">'&lt;a href=&quot;index.html&quot; title=&quot;Go to home page&quot;&gt;'</code>, and that is what gets appended to <code class="varname">self.pieces</code>.</td>
</tr>
</tbody>
</table>


![Important](../images/important.png) 
Using dictionary-based string formatting with `locals` is a convenient way of making complex string formatting expressions more readable, but it comes with a price. There is a slight performance hit in making the call to `locals`, since [`locals` builds a copy](locals_and_globals.html#dialect.locals.readonly.example "Example 8.12. locals is read-only, globals is not") of the local namespace. 

  

