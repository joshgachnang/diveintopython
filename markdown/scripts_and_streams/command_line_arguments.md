

10.6. Handling command-line arguments
-------------------------------------

Python fully supports creating programs that can be run on the command
line, complete with command-line arguments and either short- or
long-style flags to specify various options. None of this is
XML-specific, but this script makes good use of command-line processing,
so it seemed like a good time to mention it.

It's difficult to talk about command-line processing without
understanding how command-line arguments are exposed to your Python
program, so let's write a simple program to see them.

### Example 10.20. Introducing `sys.argv`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    #argecho.py
    import sys

    for arg in sys.argv: 
        print arg



[![1](../images/callouts/1.png)](#kgp.commandline.0.1) Each command-line argument passed to the program will be in `sys.argv`, which is just a list. Here you are printing each argument on a separate line. 

### Example 10.21. The contents of `sys.argv`

    [you@localhost py]$ python argecho.py             
    argecho.py
    [you@localhost py]$ python argecho.py abc def     
    argecho.py
    abc
    def
    [you@localhost py]$ python argecho.py --help      
    argecho.py
    --help
    [you@localhost py]$ python argecho.py -m kant.xml 
    argecho.py
    -m
    kant.xml



[![1](../images/callouts/1.png)](#kgp.commandline.1.1) The first thing to know about `sys.argv` is that it contains the name of the script you're calling. You will actually use this knowledge to your advantage later, in [Chapter 16, *Functional Programming*](../functional_programming/index.html "Chapter 16. Functional Programming"). Don't worry about it for now. 

[![2](../images/callouts/2.png)](#kgp.commandline.1.2) Command-line arguments are separated by spaces, and each shows up as a separate element in the `sys.argv` list. 

[![3](../images/callouts/3.png)](#kgp.commandline.1.3) Command-line flags, like `--help`, also show up as their own element in the `sys.argv` list. 

[![4](../images/callouts/4.png)](#kgp.commandline.1.4) To make things even more interesting, some command-line flags themselves take arguments. For instance, here you have a flag (`-m`) which takes an argument (`kant.xml`). Both the flag itself and the flag's argument are simply sequential elements in the `sys.argv` list. No attempt is made to associate one with the other; all you get is a list. 

So as you can see, you certainly have all the information passed on the
command line, but then again, it doesn't look like it's going to be all
that easy to actually use it. For simple programs that only take a
single argument and have no flags, you can simply use `sys.argv[1]` to
access the argument. There's no shame in this; I do it all the time. For
more complex programs, you need the `getopt` module.

### Example 10.22. Introducing `getopt`

    def main(argv):                         
        grammar = "kant.xml"                 
        try:                                
            opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="]) 
        except getopt.GetoptError:           
            usage()                          
            sys.exit(2)                     

    ...

    if __name__ == "__main__":
        main(sys.argv[1:])



[![1](../images/callouts/1.png)](#kgp.commandline.2.1) First off, look at the bottom of the example and notice that you're calling the `main` function with `sys.argv[1:]`. Remember, `sys.argv[0]` is the name of the script that you're running; you don't care about that for command-line processing, so you chop it off and pass the rest of the list. 

[![2](../images/callouts/2.png)](#kgp.commandline.2.2) This is where all the interesting processing happens. The `getopt` function of the `getopt` module takes three parameters: the argument list (which you got from `sys.argv[1:]`), a string containing all the possible single-character command-line flags that this program accepts, and a list of longer command-line flags that are equivalent to the single-character versions. This is quite confusing at first glance, and is explained in more detail below. 

[![3](../images/callouts/3.png)](#kgp.commandline.2.3) If anything goes wrong trying to parse these command-line flags, `getopt` will raise an exception, which you catch. You told `getopt` all the flags you understand, so this probably means that the end user passed some command-line flag that you don't understand. 

[![4](../images/callouts/4.png)](#kgp.commandline.2.4) As is standard practice in the UNIX world, when the script is passed flags it doesn't understand, you print out a summary of proper usage and exit gracefully. Note that I haven't shown the `usage` function here. You would still need to code that somewhere and have it print out the appropriate summary; it's not automatic. 

So what are all those parameters you pass to the `getopt` function?
Well, the first one is simply the raw list of command-line flags and
arguments (not including the first element, the script name, which you
already chopped off before calling the `main` function). The second is
the list of short command-line flags that the script accepts.

### `"hg:d"`

`-h`
:   print usage summary
`-g ...`
:   use specified grammar file or URL
`-d`
:   show debugging information while parsing

The first and third flags are simply standalone flags; you specify them
or you don't, and they do things (print help) or change state (turn on
debugging). However, the second flag (`-g`) *must* be followed by an
argument, which is the name of the grammar file to read from. In fact it
can be a filename or a web address, and you don't know which yet (you'll
figure it out later), but you know it has to be *something*. So you tell
`getopt` this by putting a colon after the `g` in that second parameter
to the `getopt` function.

To further complicate things, the script accepts either short flags
(like `-h`) or long flags (like `--help`), and you want them to do the
same thing. This is what the third parameter to `getopt` is for, to
specify a list of the long flags that correspond to the short flags you
specified in the second parameter.

### `["help", "grammar="]`

`--help`
:   print usage summary
`--grammar ...`
:   use specified grammar file or URL

Three things of note here:

1.  All long flags are preceded by two dashes on the command line, but
    you don't include those dashes when calling `getopt`. They are
    understood.
2.  The `--grammar` flag must always be followed by an additional
    argument, just like the `-g` flag. This is notated by an equals
    sign, `"grammar="`.
3.  The list of long flags is shorter than the list of short flags,
    because the `-d` flag does not have a corresponding long version.
    This is fine; only `-d` will turn on debugging. But the order of
    short and long flags needs to be the same, so you'll need to specify
    all the short flags that *do* have corresponding long flags first,
    then all the rest of the short flags.

Confused yet? Let's look at the actual code and see if it makes sense in
context.

### Example 10.23. Handling command-line arguments in `kgp.py`

    def main(argv):                          
        grammar = "kant.xml"                
        try:                                
            opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
        except getopt.GetoptError:          
            usage()                         
            sys.exit(2)                     
        for opt, arg in opts:                
            if opt in ("-h", "--help"):      
                usage()                     
                sys.exit()                  
            elif opt == '-d':                
                global _debug               
                _debug = 1                  
            elif opt in ("-g", "--grammar"): 
                grammar = arg               

        source = "".join(args)               

        k = KantGenerator(grammar, source)
        print k.output()



[![1](../images/callouts/1.png)](#kgp.commandline.3.0) The `grammar` variable will keep track of the grammar file you're using. You initialize it here in case it's not specified on the command line (using either the `-g` or the `--grammar` flag). 

[![2](../images/callouts/2.png)](#kgp.commandline.3.1) The `opts` variable that you get back from `getopt` contains a list of tuples: `flag` and `argument`. If the flag doesn't take an argument, then `arg` will simply be `None`. This makes it easier to loop through the flags. 

[![3](../images/callouts/3.png)](#kgp.commandline.3.2) `getopt` validates that the command-line flags are acceptable, but it doesn't do any sort of conversion between short and long flags. If you specify the `-h` flag, `opt` will contain `"-h"`; if you specify the `--help` flag, `opt` will contain `"--help"`. So you need to check for both. 

[![4](../images/callouts/4.png)](#kgp.commandline.3.3) Remember, the `-d` flag didn't have a corresponding long flag, so you only need to check for the short form. If you find it, you set a global variable that you'll refer to later to print out debugging information. (I used this during the development of the script. What, you thought all these examples worked on the first try?) 

[![5](../images/callouts/5.png)](#kgp.commandline.3.4) If you find a grammar file, either with a `-g` flag or a `--grammar` flag, you save the argument that followed it (stored in `arg`) into the `grammar` variable, overwriting the default that you initialized at the top of the `main` function. 

[![6](../images/callouts/6.png)](#kgp.commandline.3.5) That's it. You've looped through and dealt with all the command-line flags. That means that anything left must be command-line arguments. These come back from the `getopt` function in the `args` variable. In this case, you're treating them as source material for the parser. If there are no command-line arguments specified, `args` will be an empty list, and `source` will end up as the empty string. 

  

