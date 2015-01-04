1. In chapter 6.1: Exceptions and File Handling,
   it would be good to mention the *with* statement. 
   https://docs.python.org/2/reference/compound_stmts.html#the-with-statement
2. In chapter 6.2: Working with File Objects, an example uses
   `f.seek(offset, whence)` where *whence* is a digit instead of
   [os module constant]
   (https://docs.python.org/2/library/stdtypes.html?highlight=seek#file.seek).
   It should be `os.SEEK_END` in this particular case.
   It has to be corrected in the chapter and the examples source files.
