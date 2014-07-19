

6.5. Working with Directories
-----------------------------

The `os.path` module has several functions for manipulating files and
directories. Here, we're looking at handling pathnames and listing the
contents of a directory.

### Example 6.16. Constructing Pathnames

    >>> import os
    >>> os.path.join("c:\\music\\ap\\", "mahadeva.mp3")  
    'c:\\music\\ap\\mahadeva.mp3'
    >>> os.path.join("c:\\music\\ap", "mahadeva.mp3")   
    'c:\\music\\ap\\mahadeva.mp3'
    >>> os.path.expanduser("~")                         
    'c:\\Documents and Settings\\mpilgrim\\My Documents'
    >>> os.path.join(os.path.expanduser("~"), "Python") 
    'c:\\Documents and Settings\\mpilgrim\\My Documents\\Python'



[![1](../images/callouts/1.png)](#fileinfo.os.1.1) `os.path` is a reference to a module -- which module depends on your platform. Just as [`getpass`](index.html#crossplatform.example "Example 6.2. Supporting Platform-Specific Functionality") encapsulates differences between platforms by setting `getpass` to a platform-specific function, `os` encapsulates differences between platforms by setting `path` to a platform-specific module. 

[![2](../images/callouts/2.png)](#fileinfo.os.1.2) The `join` function of `os.path` constructs a pathname out of one or more partial pathnames. In this case, it simply concatenates strings. (Note that dealing with pathnames on Windows is annoying because the backslash character must be escaped.) 

[![3](../images/callouts/3.png)](#fileinfo.os.1.3) In this slightly less trivial case, `join` will add an extra backslash to the pathname before joining it to the filename. I was overjoyed when I discovered this, since `addSlashIfNecessary` is one of the stupid little functions I always need to write when building up my toolbox in a new language. *Do not* write this stupid little function in Python; smart people have already taken care of it for you. 

[![4](../images/callouts/4.png)](#fileinfo.os.1.4) `expanduser` will expand a pathname that uses `~` to represent the current user's home directory. This works on any platform where users have a home directory, like Windows, UNIX, and Mac OS X; it has no effect on Mac OS. 

[![5](../images/callouts/5.png)](#fileinfo.os.1.5) Combining these techniques, you can easily construct pathnames for directories and files under the user's home directory. 

### Example 6.17. Splitting Pathnames

    >>> os.path.split("c:\\music\\ap\\mahadeva.mp3")                        
    ('c:\\music\\ap', 'mahadeva.mp3')
    >>> (filepath, filename) = os.path.split("c:\\music\\ap\\mahadeva.mp3") 
    >>> filepath                                                            
    'c:\\music\\ap'
    >>> filename                                                            
    'mahadeva.mp3'
    >>> (shortname, extension) = os.path.splitext(filename)                 
    >>> shortname
    'mahadeva'
    >>> extension
    '.mp3'



[![1](../images/callouts/1.png)](#fileinfo.os.2.1) The `split` function splits a full pathname and returns a tuple containing the path and filename. Remember when I said you could use [multi-variable assignment](../native_data_types/declaring_variables.html#odbchelper.multiassign "3.4.2. Assigning Multiple Values at Once") to return multiple values from a function? Well, `split` is such a function. 

[![2](../images/callouts/2.png)](#fileinfo.os.2.2) You assign the return value of the `split` function into a tuple of two variables. Each variable receives the value of the corresponding element of the returned tuple. 

[![3](../images/callouts/3.png)](#fileinfo.os.2.3) The first variable, `filepath`, receives the value of the first element of the tuple returned from `split`, the file path. 

[![4](../images/callouts/4.png)](#fileinfo.os.2.4) The second variable, `filename`, receives the value of the second element of the tuple returned from `split`, the filename. 

[![5](../images/callouts/5.png)](#fileinfo.os.2.5) `os.path` also contains a function `splitext`, which splits a filename and returns a tuple containing the filename and the file extension. You use the same technique to assign each of them to separate variables. 

### Example 6.18. Listing Directories

    >>> os.listdir("c:\\music\\_singles\\")              
    ['a_time_long_forgotten_con.mp3', 'hellraiser.mp3',
    'kairo.mp3', 'long_way_home1.mp3', 'sidewinder.mp3', 
    'spinning.mp3']
    >>> dirname = "c:\\"
    >>> os.listdir(dirname)                              
    ['AUTOEXEC.BAT', 'boot.ini', 'CONFIG.SYS', 'cygwin',
    'docbook', 'Documents and Settings', 'Incoming', 'Inetpub', 'IO.SYS',
    'MSDOS.SYS', 'Music', 'NTDETECT.COM', 'ntldr', 'pagefile.sys',
    'Program Files', 'Python20', 'RECYCLER',
    'System Volume Information', 'TEMP', 'WINNT']
    >>> [f for f in os.listdir(dirname)
    ...     if os.path.isfile(os.path.join(dirname, f))] 
    ['AUTOEXEC.BAT', 'boot.ini', 'CONFIG.SYS', 'IO.SYS', 'MSDOS.SYS',
    'NTDETECT.COM', 'ntldr', 'pagefile.sys']
    >>> [f for f in os.listdir(dirname)
    ...     if os.path.isdir(os.path.join(dirname, f))]  
    ['cygwin', 'docbook', 'Documents and Settings', 'Incoming',
    'Inetpub', 'Music', 'Program Files', 'Python20', 'RECYCLER',
    'System Volume Information', 'TEMP', 'WINNT']



[![1](../images/callouts/1.png)](#fileinfo.os.3.1) The `listdir` function takes a pathname and returns a list of the contents of the directory. 

[![2](../images/callouts/2.png)](#fileinfo.os.3.2) `listdir` returns both files and folders, with no indication of which is which. 

[![3](../images/callouts/3.png)](#fileinfo.os.3.3) You can use [list filtering](../power_of_introspection/filtering_lists.html "4.5. Filtering Lists") and the `isfile` function of the `os.path` module to separate the files from the folders. `isfile` takes a pathname and returns 1 if the path represents a file, and 0 otherwise. Here you're using `os.path`.`join` to ensure a full pathname, but `isfile` also works with a partial path, relative to the current working directory. You can use `os.getcwd()` to get the current working directory. 

[![4](../images/callouts/4.png)](#fileinfo.os.3.4) `os.path` also has a `isdir` function which returns 1 if the path represents a directory, and 0 otherwise. You can use this to get a list of the subdirectories within a directory. 

### Example 6.19. Listing Directories in `fileinfo.py`

    def listDirectory(directory, fileExtList):                                        
        "get list of file info objects for files of particular extensions" 
        fileList = [os.path.normcase(f)
                    for f in os.listdir(directory)]             
        fileList = [os.path.join(directory, f) 
                   for f in fileList
                    if os.path.splitext(f)[1] in fileExtList]    



[![1](../images/callouts/1.png)](#fileinfo.os.3a.1) `os.listdir(directory)` returns a list of all the files and folders in `directory`. 

[![2](../images/callouts/2.png)](#fileinfo.os.3a.2) Iterating through the list with `f`, you use `os.path.normcase(f)` to normalize the case according to operating system defaults. `normcase` is a useful little function that compensates for case-insensitive operating systems that think that `mahadeva.mp3` and `mahadeva.MP3` are the same file. For instance, on Windows and Mac OS, `normcase` will convert the entire filename to lowercase; on UNIX-compatible systems, it will return the filename unchanged. 

[![3](../images/callouts/3.png)](#fileinfo.os.3a.3) Iterating through the normalized list with `f` again, you use `os.path.splitext(f)` to split each filename into name and extension. 

[![4](../images/callouts/4.png)](#fileinfo.os.3a.4) For each file, you see if the extension is in the list of file extensions you care about (`fileExtList`, which was passed to the `listDirectory` function). 

[![5](../images/callouts/5.png)](#fileinfo.os.3a.5) For each file you care about, you use `os.path.join(directory, f)` to construct the full pathname of the file, and return a list of the full pathnames. 


![Note](../images/note.png) 
Whenever possible, you should use the functions in `os` and `os.path` for file, directory, and path manipulations. These modules are wrappers for platform-specific modules, so functions like `os.path.split` work on UNIX, Windows, Mac OS, and any other platform supported by Python. 

There is one other way to get the contents of a directory. It's very
powerful, and it uses the sort of wildcards that you may already be
familiar with from working on the command line.

### Example 6.20. Listing Directories with `glob`

    >>> os.listdir("c:\\music\\_singles\\")               
    ['a_time_long_forgotten_con.mp3', 'hellraiser.mp3',
    'kairo.mp3', 'long_way_home1.mp3', 'sidewinder.mp3',
    'spinning.mp3']
    >>> import glob
    >>> glob.glob('c:\\music\\_singles\\*.mp3')           
    ['c:\\music\\_singles\\a_time_long_forgotten_con.mp3',
    'c:\\music\\_singles\\hellraiser.mp3',
    'c:\\music\\_singles\\kairo.mp3',
    'c:\\music\\_singles\\long_way_home1.mp3',
    'c:\\music\\_singles\\sidewinder.mp3',
    'c:\\music\\_singles\\spinning.mp3']
    >>> glob.glob('c:\\music\\_singles\\s*.mp3')          
    ['c:\\music\\_singles\\sidewinder.mp3',
    'c:\\music\\_singles\\spinning.mp3']
    >>> glob.glob('c:\\music\\*\\*.mp3')                  



[![1](../images/callouts/1.png)](#fileinfo.os.4.1) As you saw earlier, `os.listdir` simply takes a directory path and lists all files and directories in that directory. 

[![2](../images/callouts/2.png)](#fileinfo.os.4.2) The `glob` module, on the other hand, takes a wildcard and returns the full path of all files and directories matching the wildcard. Here the wildcard is a directory path plus "\*.mp3", which will match all `.mp3` files. Note that each element of the returned list already includes the full path of the file. 

[![3](../images/callouts/3.png)](#fileinfo.os.4.3) If you want to find all the files in a specific directory that start with "s" and end with ".mp3", you can do that too. 

[![4](../images/callouts/4.png)](#fileinfo.os.4.4) Now consider this scenario: you have a `music` directory, with several subdirectories within it, with `.mp3` files within each subdirectory. You can get a list of all of those with a single call to `glob`, by using two wildcards at once. One wildcard is the `"*.mp3"` (to match `.mp3` files), and one wildcard is *within the directory path itself*, to match any subdirectory within `c:\music`. That's a crazy amount of power packed into one deceptively simple-looking function! 

### Further Reading on the `os` Module

-   [Python Knowledge
    Base](http://www.faqts.com/knowledge-base/index.phtml/fid/199/)
    answers [questions about the `os`
    module](http://www.faqts.com/knowledge-base/index.phtml/fid/240).
-   [*Python Library Reference*](http://www.python.org/doc/current/lib/)
    documents the
    [`os`](http://www.python.org/doc/current/lib/module-os.html) module
    and the
    [`os.path`](http://www.python.org/doc/current/lib/module-os.path.html)
    module.

  

