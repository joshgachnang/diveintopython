

6.6. Putting It All Together
----------------------------

Once again, all the dominoes are in place. You've seen how each line of
code works. Now let's step back and see how it all fits together.

### Example 6.21. `listDirectory`

    def listDirectory(directory, fileExtList):                                         
        "get list of file info objects for files of particular extensions"
        fileList = [os.path.normcase(f)
                    for f in os.listdir(directory)]           
        fileList = [os.path.join(directory, f) 
                   for f in fileList
                    if os.path.splitext(f)[1] in fileExtList]                          
        def getFileInfoClass(filename, module=sys.modules[FileInfo.__module__]):       
            "get file info class from filename extension"                             
            subclass = "%sFileInfo" % os.path.splitext(filename)[1].upper()[1:]        
            return hasattr(module, subclass) and getattr(module, subclass) or FileInfo 
        return [getFileInfoClass(f)(f) for f in fileList]                              



[![1](../images/callouts/1.png)](#fileinfo.alltogether.1.1) `listDirectory` is the main attraction of this entire module. It takes a directory (like `c:\music\_singles\` in my case) and a list of interesting file extensions (like `['.mp3']`), and it returns a list of class instances that act like dictionaries that contain metadata about each interesting file in that directory. And it does it in just a few straightforward lines of code. 

[![2](../images/callouts/2.png)](#fileinfo.alltogether.1.2) As you saw in the [previous section](os_module.html "6.5. Working with Directories"), this line of code gets a list of the full pathnames of all the files in `directory` that have an interesting file extension (as specified by `fileExtList`). 

[![3](../images/callouts/3.png)](#fileinfo.alltogether.1.3) Old-school Pascal programmers may be familiar with them, but most people give me a blank stare when I tell them that Python supports *nested functions* -- literally, a function within a function. The nested function `getFileInfoClass` can be called only from the function in which it is defined, `listDirectory`. As with any other function, you don't need an interface declaration or anything fancy; just define the function and code it. 

[![4](../images/callouts/4.png)](#fileinfo.alltogether.1.4) Now that you've seen the [`os`](os_module.html "6.5. Working with Directories") module, this line should make more sense. It gets the extension of the file (`os.path.splitext(filename)[1]`), forces it to uppercase (`.upper()`), slices off the dot (`[1:]`), and constructs a class name out of it with string formatting. So `c:\music\ap\mahadeva.mp3` becomes `.mp3` becomes `.MP3` becomes `MP3` becomes `MP3FileInfo`. 

[![5](../images/callouts/5.png)](#fileinfo.alltogether.1.5) Having constructed the name of the handler class that would handle this file, you check to see if that handler class actually exists in this module. If it does, you return the class, otherwise you return the base class `FileInfo`. This is a very important point: *this function returns a class*. Not an instance of a class, but the class itself. 

[![6](../images/callouts/6.png)](#fileinfo.alltogether.1.6) For each file in the “interesting files” list (`fileList`), you call `getFileInfoClass` with the filename (`f`). Calling `getFileInfoClass(f)` returns a class; you don't know exactly which class, but you don't care. You then create an instance of this class (whatever it is) and pass the filename (`f` again), to the `__init__` method. As you saw [earlier in this chapter](../object_oriented_framework/special_class_methods.html#fileinfo.specialmethods.setname "Example 5.15. Setting an MP3FileInfo's name"), the `__init__` method of `FileInfo` sets `self["name"]`, which triggers `__setitem__`, which is overridden in the descendant (`MP3FileInfo`) to parse the file appropriately to pull out the file's metadata. You do all that for each interesting file and return a list of the resulting instances. 

Note that `listDirectory` is completely generic. It doesn't know ahead
of time which types of files it will be getting, or which classes are
defined that could potentially handle those files. It inspects the
directory for the files to process, and then introspects its own module
to see what special handler classes (like `MP3FileInfo`) are defined.
You can extend this program to handle other types of files simply by
defining an appropriately-named class: `HTMLFileInfo` for HTML files,
`DOCFileInfo` for Word `.doc` files, and so forth. `listDirectory` will
handle them all, without modification, by handing off the real work to
the appropriate classes and collating the results.

  

