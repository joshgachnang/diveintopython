

Chapter 5. Objects and Object-Orientation
-----------------------------------------

-   [5.1. Diving In](index.html#fileinfo.divein)
-   [5.2. Importing Modules Using from module
    import](importing_modules.html)
-   [5.3. Defining Classes](defining_classes.html)
    -   [5.3.1. Initializing and Coding
        Classes](defining_classes.html#d0e11720)
    -   [5.3.2. Knowing When to Use self and
        \_\_init\_\_](defining_classes.html#d0e11896)
-   [5.4. Instantiating Classes](instantiating_classes.html)
    -   [5.4.1. Garbage Collection](instantiating_classes.html#d0e12165)
-   [5.5. Exploring UserDict: A Wrapper Class](userdict.html)
-   [5.6. Special Class Methods](special_class_methods.html)
    -   [5.6.1. Getting and Setting
        Items](special_class_methods.html#d0e12822)
-   [5.7. Advanced Special Class Methods](special_class_methods2.html)
-   [5.8. Introducing Class Attributes](class_attributes.html)
-   [5.9. Private Functions](private_functions.html)
-   [5.10. Summary](summary.html)

This chapter, and pretty much every chapter after this, deals with
object-oriented Python programming.

5.1. Diving In
--------------

Here is a complete, working Python program. Read the
[`doc string`s](../getting_to_know_python/documenting_functions.html "2.3. Documenting Functions")
of the module, the classes, and the functions to get an overview of what
this program does and how it works. As usual, don't worry about the
stuff you don't understand; that's what the rest of the chapter is for.

### Example 5.1. `fileinfo.py`

If you have not already done so, you can [download this and other
examples](http://diveintopython.net/download/diveintopython-examples-5.4.zip "Download example scripts")
used in this book.

    """Framework for getting filetype-specific metadata.

    Instantiate appropriate class with filename.  Returned object acts like a
    dictionary, with key-value pairs for each piece of metadata.
        import fileinfo
        info = fileinfo.MP3FileInfo("/music/ap/mahadeva.mp3")
        print "\\n".join(["%s=%s" % (k, v) for k, v in info.items()])

    Or use listDirectory function to get info on all files in a directory.
        for info in fileinfo.listDirectory("/music/ap/", [".mp3"]):
            ...

    Framework can be extended by adding classes for particular file types, e.g.
    HTMLFileInfo, MPGFileInfo, DOCFileInfo.  Each class is completely responsible for
    parsing its files appropriately; see MP3FileInfo for example.
    """
    import os
    import sys
    from UserDict import UserDict

    def stripnulls(data):
        "strip whitespace and nulls"
        return data.replace("\00", "").strip()

    class FileInfo(UserDict):
        "store file metadata"
        def __init__(self, filename=None):
            UserDict.__init__(self)
            self["name"] = filename

    class MP3FileInfo(FileInfo):
        "store ID3v1.0 MP3 tags"
        tagDataMap = {"title"   : (  3,  33, stripnulls),
                      "artist"  : ( 33,  63, stripnulls),
                      "album"   : ( 63,  93, stripnulls),
                      "year"    : ( 93,  97, stripnulls),
                      "comment" : ( 97, 126, stripnulls),
                      "genre"   : (127, 128, ord)}

        def __parse(self, filename):
            "parse ID3v1.0 tags from MP3 file"
            self.clear()
            try:                               
                fsock = open(filename, "rb", 0)
                try:                           
                    fsock.seek(-128, 2)        
                    tagdata = fsock.read(128)  
                finally:                       
                    fsock.close()              
                if tagdata[:3] == "TAG":
                    for tag, (start, end, parseFunc) in self.tagDataMap.items():
                        self[tag] = parseFunc(tagdata[start:end])               
            except IOError:                    
                pass                           

        def __setitem__(self, key, item):
            if key == "name" and item:
                self.__parse(item)
            FileInfo.__setitem__(self, key, item)

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

    if __name__ == "__main__":
        for info in listDirectory("/music/_singles/", [".mp3"]): 
            print "\n".join(["%s=%s" % (k, v) for k, v in info.items()])
            print



[![1](../images/callouts/1.png)](#fileinfo_divein.1.1) This program's output depends on the files on your hard drive. To get meaningful output, you'll need to change the directory path to point to a directory of MP3 files on your own machine. 

This is the output I got on my machine. Your output will be different,
unless, by some startling coincidence, you share my exact taste in
music.

    album=
    artist=Ghost in the Machine
    title=A Time Long Forgotten (Concept
    genre=31
    name=/music/_singles/a_time_long_forgotten_con.mp3
    year=1999
    comment=http://mp3.com/ghostmachine

    album=Rave Mix
    artist=***DJ MARY-JANE***
    title=HELLRAISER****Trance from Hell
    genre=31
    name=/music/_singles/hellraiser.mp3
    year=2000
    comment=http://mp3.com/DJMARYJANE

    album=Rave Mix
    artist=***DJ MARY-JANE***
    title=KAIRO****THE BEST GOA
    genre=31
    name=/music/_singles/kairo.mp3
    year=2000
    comment=http://mp3.com/DJMARYJANE

    album=Journeys
    artist=Masters of Balance
    title=Long Way Home
    genre=31
    name=/music/_singles/long_way_home1.mp3
    year=2000
    comment=http://mp3.com/MastersofBalan

    album=
    artist=The Cynic Project
    title=Sidewinder
    genre=18
    name=/music/_singles/sidewinder.mp3
    year=2000
    comment=http://mp3.com/cynicproject

    album=Digitosis@128k
    artist=VXpanded
    title=Spinning
    genre=255
    name=/music/_singles/spinning.mp3
    year=2000
    comment=http://mp3.com/artists/95/vxp

  

