

6.7. Summary
------------

The `fileinfo.py` program introduced in [Chapter
5](../object_oriented_framework/index.html) should now make perfect
sense.

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

Before diving into the next chapter, make sure you're comfortable doing
the following things:

-   Catching exceptions with
    [`try...except`](index.html#fileinfo.exception "6.1. Handling Exceptions")
-   Protecting external resources with
    [`try...finally`](file_objects.html#fileinfo.files.incode "Example 6.6. File Objects in MP3FileInfo")
-   Reading from
    [files](file_objects.html "6.2. Working with File Objects")
-   Assigning multiple values at once in a [`for`
    loop](for_loops.html#fileinfo.multiassign.for.example "Example 6.11. for Loop in MP3FileInfo")
-   Using the [`os`](os_module.html "6.5. Working with Directories")
    module for all your cross-platform file manipulation needs
-   Dynamically [instantiating classes of unknown
    type](all_together.html "6.6. Putting It All Together") by treating
    classes as objects and passing them around

  

