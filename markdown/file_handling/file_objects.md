

6.2. Working with File Objects
------------------------------

-   [6.2.1. Reading Files](file_objects.html#d0e14670)
-   [6.2.2. Closing Files](file_objects.html#d0e14800)
-   [6.2.3. Handling I/O Errors](file_objects.html#d0e14928)
-   [6.2.4. Writing to Files](file_objects.html#d0e15055)

Python has a built-in function, `open`, for opening a file on disk.
`open` returns a file object, which has methods and attributes for
getting information about and manipulating the opened file.

### Example 6.3. Opening a File

    >>> f = open("/music/_singles/kairo.mp3", "rb") 
    >>> f                                           
    <open file '/music/_singles/kairo.mp3', mode 'rb' at 010E3988>
    >>> f.mode                                      
    'rb'
    >>> f.name                                      
    '/music/_singles/kairo.mp3'



[![1](../images/callouts/1.png)](#fileinfo.files.1.1) The `open` method can take up to three parameters: a filename, a mode, and a buffering parameter. Only the first one, the filename, is required; the other two are [optional](../power_of_introspection/optional_arguments.html "4.2. Using Optional and Named Arguments"). If not specified, the file is opened for reading in text mode. Here you are opening the file for reading in binary mode. (`print open.__doc__` displays a great explanation of all the possible modes.) 

[![2](../images/callouts/2.png)](#fileinfo.files.1.2) The `open` function returns an object (by now, [this should not surprise you](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object")). A file object has several useful attributes. 

[![3](../images/callouts/3.png)](#fileinfo.files.1.3) The `mode` attribute of a file object tells you in which mode the file was opened. 

[![4](../images/callouts/4.png)](#fileinfo.files.1.4) The `name` attribute of a file object tells you the name of the file that the file object has open. 

### 6.2.1. Reading Files

After you open a file, the first thing you'll want to do is read from
it, as shown in the next example.

### Example 6.4. Reading a File

    >>> f
    <open file '/music/_singles/kairo.mp3', mode 'rb' at 010E3988>
    >>> f.tell()              
    0
    >>> f.seek(-128, 2)       
    >>> f.tell()              
    7542909
    >>> tagData = f.read(128) 
    >>> tagData
    'TAGKAIRO****THE BEST GOA         ***DJ MARY-JANE***            
    Rave Mix                      2000http://mp3.com/DJMARYJANE     \037'
    >>> f.tell()              
    7543037



[![1](../images/callouts/1.png)](#fileinfo.files.2.1) A file object maintains state about the file it has open. The `tell` method of a file object tells you your current position in the open file. Since you haven't done anything with this file yet, the current position is `0`, which is the beginning of the file. 

[![2](../images/callouts/2.png)](#fileinfo.files.2.2) The `seek` method of a file object moves to another position in the open file. The second parameter specifies what the first one means; `0` means move to an absolute position (counting from the start of the file), `1` means move to a relative position (counting from the current position), and `2` means move to a position relative to the end of the file. Since the MP3 tags you're looking for are stored at the end of the file, you use `2` and tell the file object to move to a position `128` bytes from the end of the file. 

[![3](../images/callouts/3.png)](#fileinfo.files.2.3) The `tell` method confirms that the current file position has moved. 

[![4](../images/callouts/4.png)](#fileinfo.files.2.4) The `read` method reads a specified number of bytes from the open file and returns a string with the data that was read. The optional parameter specifies the maximum number of bytes to read. If no parameter is specified, `read` will read until the end of the file. (You could have simply said `read()` here, since you know exactly where you are in the file and you are, in fact, reading the last 128 bytes.) The read data is assigned to the `tagData` variable, and the current position is updated based on how many bytes were read. 

[![5](../images/callouts/5.png)](#fileinfo.files.2.5) The `tell` method confirms that the current position has moved. If you do the math, you'll see that after reading 128 bytes, the position has been incremented by 128. 

### 6.2.2. Closing Files

Open files consume system resources, and depending on the file mode,
other programs may not be able to access them. It's important to close
files as soon as you're finished with them.

### Example 6.5. Closing a File

    >>> f
    <open file '/music/_singles/kairo.mp3', mode 'rb' at 010E3988>
    >>> f.closed       
    False
    >>> f.close()      
    >>> f
    <closed file '/music/_singles/kairo.mp3', mode 'rb' at 010E3988>
    >>> f.closed       
    True
    >>> f.seek(0)      
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    ValueError: I/O operation on closed file
    >>> f.tell()
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    ValueError: I/O operation on closed file
    >>> f.read()
    Traceback (innermost last):
      File "<interactive input>", line 1, in ?
    ValueError: I/O operation on closed file
    >>> f.close()      



[![1](../images/callouts/1.png)](#fileinfo.files.3.1) The `closed` attribute of a file object indicates whether the object has a file open or not. In this case, the file is still open (`closed` is `False`). 

[![2](../images/callouts/2.png)](#fileinfo.files.3.2) To close a file, call the `close` method of the file object. This frees the lock (if any) that you were holding on the file, flushes buffered writes (if any) that the system hadn't gotten around to actually writing yet, and releases the system resources. 

[![3](../images/callouts/3.png)](#fileinfo.files.3.3) The `closed` attribute confirms that the file is closed. 

[![4](../images/callouts/4.png)](#fileinfo.files.3.4) Just because a file is closed doesn't mean that the file object ceases to exist. The variable `f` will continue to exist until it [goes out of scope](../object_oriented_framework/instantiating_classes.html#fileinfo.scope "Example 5.8. Trying to Implement a Memory Leak") or gets manually deleted. However, none of the methods that manipulate an open file will work once the file has been closed; they all raise an exception. 

[![5](../images/callouts/5.png)](#fileinfo.files.3.5) Calling `close` on a file object whose file is already closed does *not* raise an exception; it fails silently. 

### 6.2.3. Handling I/O Errors

Now you've seen enough to understand the file handling code in the
`fileinfo.py` sample code from teh previous chapter. This example shows
how to safely open and read from a file and gracefully handle errors.

### Example 6.6. File Objects in `MP3FileInfo`

            try:                                
                fsock = open(filename, "rb", 0) 
                try:                           
                    fsock.seek(-128, 2)         
                    tagdata = fsock.read(128)   
                finally:                        
                    fsock.close()              
                .
                .
                .
            except IOError:                     
                pass                           



[![1](../images/callouts/1.png)](#fileinfo.files.4.1) Because opening and reading files is risky and may raise an exception, all of this code is wrapped in a `try...except` block. (Hey, isn't [standardized indentation](../getting_to_know_python/indenting_code.html "2.5. Indenting Code") great? This is where you start to appreciate it.) 

[![2](../images/callouts/2.png)](#fileinfo.files.4.2) The `open` function may raise an `IOError`. (Maybe the file doesn't exist.) 

[![3](../images/callouts/3.png)](#fileinfo.files.4.3) The `seek` method may raise an `IOError`. (Maybe the file is smaller than 128 bytes.) 

[![4](../images/callouts/4.png)](#fileinfo.files.4.4) The `read` method may raise an `IOError`. (Maybe the disk has a bad sector, or it's on a network drive and the network just went down.) 

[![5](../images/callouts/5.png)](#fileinfo.files.4.5) This is new: a `try...finally` block. Once the file has been opened successfully by the `open` function, you want to make absolutely sure that you close it, even if an exception is raised by the `seek` or `read` methods. That's what a `try...finally` block is for: code in the `finally` block will *always* be executed, even if something in the `try` block raises an exception. Think of it as code that gets executed on the way out, regardless of what happened before. 

[![6](../images/callouts/6.png)](#fileinfo.files.4.6) At last, you handle your `IOError` exception. This could be the `IOError` exception raised by the call to `open`, `seek`, or `read`. Here, you really don't care, because all you're going to do is ignore it silently and continue. (Remember, `pass` is a Python statement that [does nothing](../object_oriented_framework/defining_classes.html#fileinfo.class.simplest "Example 5.3. The Simplest Python Class").) That's perfectly legal; “handling” an exception can mean explicitly doing nothing. It still counts as handled, and processing will continue normally on the next line of code after the `try...except` block. 

### 6.2.4. Writing to Files

As you would expect, you can also write to files in much the same way
that you read from them. There are two basic file modes:

-   "Append" mode will add data to the end of the file.
-   "write" mode will overwrite the file.

Either mode will create the file automatically if it doesn't already
exist, so there's never a need for any sort of fiddly "if the log file
doesn't exist yet, create a new empty file just so you can open it for
the first time" logic. Just open it and start writing.

### Example 6.7. Writing to Files

    >>> logfile = open('test.log', 'w') 
    >>> logfile.write('test succeeded') 
    >>> logfile.close()
    >>> print file('test.log').read()   
    test succeeded
    >>> logfile = open('test.log', 'a') 
    >>> logfile.write('line 2')
    >>> logfile.close()
    >>> print file('test.log').read()   
    test succeededline 2



[![1](../images/callouts/1.png)](#fileinfo.files.5.1) You start boldly by creating either the new file `test.log` or overwrites the existing file, and opening the file for writing. (The second parameter `"w"` means open the file for writing.) Yes, that's all as dangerous as it sounds. I hope you didn't care about the previous contents of that file, because it's gone now. 

[![2](../images/callouts/2.png)](#fileinfo.files.5.2) You can add data to the newly opened file with the `write` method of the file object returned by `open`. 

[![3](../images/callouts/3.png)](#fileinfo.files.5.3) `file` is a synonym for `open`. This one-liner opens the file, reads its contents, and prints them. 

[![4](../images/callouts/4.png)](#fileinfo.files.5.4) You happen to know that `test.log` exists (since you just finished writing to it), so you can open it and append to it. (The `"a"` parameter means open the file for appending.) Actually you could do this even if the file didn't exist, because opening the file for appending will create the file if necessary. But appending will *never* harm the existing contents of the file. 

[![5](../images/callouts/5.png)](#fileinfo.files.5.5) As you can see, both the original line you wrote and the second line you appended are now in `test.log`. Also note that carriage returns are not included. Since you didn't write them explicitly to the file either time, the file doesn't include them. You can write a carriage return with the `"\n"` character. Since you didn't do this, everything you wrote to the file ended up smooshed together on the same line. 

### Further Reading on File Handling

-   [*Python Tutorial*](http://www.python.org/doc/current/tut/tut.html)
    discusses reading and writing files, including how to [read a file
    one line at a time into a
    list](http://www.python.org/doc/current/tut/node9.html#SECTION009210000000000000000).
-   [eff-bot](http://www.effbot.org/guides/) discusses efficiency and
    performance of [various ways of reading a
    file](http://www.effbot.org/guides/readline-performance.htm).
-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    answers [common questions about
    files](http://www.faqts.com/knowledge-base/index.phtml/fid/552).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    summarizes [all the file object
    methods](http://www.python.org/doc/current/lib/bltin-file-objects.html).

  

