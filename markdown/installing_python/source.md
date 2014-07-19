

1.7. Python Installation from Source
------------------------------------

If you prefer to build from source, you can download the Python source
code from
[http://www.python.org/ftp/python/](http://www.python.org/ftp/python/).
Select the highest version number listed, download the `.tgz` file), and
then do the usual **`configure`**, **`make`**, **`make install`** dance.

### Example 1.4. Installing from source

    localhost:~$ su -
    Password: [enter your root password]
    localhost:~# wget http://www.python.org/ftp/python/2.3/Python-2.3.tgz
    Resolving www.python.org... done.
    Connecting to www.python.org[194.109.137.226]:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 8,436,880 [application/x-tar]
    ...
    localhost:~# tar xfz Python-2.3.tgz
    localhost:~# cd Python-2.3
    localhost:~/Python-2.3# ./configure
    checking MACHDEP... linux2
    checking EXTRAPLATDIR...
    checking for --without-gcc... no
    ...
    localhost:~/Python-2.3# make
    gcc -pthread -c -fno-strict-aliasing -DNDEBUG -g -O3 -Wall -Wstrict-prototypes
    -I. -I./Include  -DPy_BUILD_CORE -o Modules/python.o Modules/python.c
    gcc -pthread -c -fno-strict-aliasing -DNDEBUG -g -O3 -Wall -Wstrict-prototypes
    -I. -I./Include  -DPy_BUILD_CORE -o Parser/acceler.o Parser/acceler.c
    gcc -pthread -c -fno-strict-aliasing -DNDEBUG -g -O3 -Wall -Wstrict-prototypes
    -I. -I./Include  -DPy_BUILD_CORE -o Parser/grammar1.o Parser/grammar1.c
    ...
    localhost:~/Python-2.3# make install
    /usr/bin/install -c python /usr/local/bin/python2.3
    ...
    localhost:~/Python-2.3# exit
    logout
    localhost:~$ which python
    /usr/local/bin/python
    localhost:~$ python
    Python 2.3.1 (#2, Sep 24 2003, 11:39:14)
    [GCC 3.3.2 20030908 (Debian prerelease)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> [press Ctrl+D to get back to the command prompt]
    localhost:~$ 

  

