

1.5. Python on RedHat Linux
---------------------------

Installing under UNIX-compatible operating systems such as Linux is easy
if you're willing to install a binary package. Pre-built binary packages
are available for most popular Linux distributions. Or you can always
compile from source.

Download the latest Python RPM by going to
[http://www.python.org/ftp/python/](http://www.python.org/ftp/python/)
and selecting the highest version number listed, then selecting the
`rpms/` directory within that. Then download the RPM with the highest
version number. You can install it with the **rpm** command, as shown
here:

### Example 1.2. Installing on RedHat Linux 9

    localhost:~$ su -
    Password: [enter your root password]
    [root@localhost root]# wget http://python.org/ftp/python/2.3/rpms/redhat-9/python2.3-2.3-5pydotorg.i386.rpm
    Resolving python.org... done.
    Connecting to python.org[194.109.137.226]:80... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 7,495,111 [application/octet-stream]
    ...
    [root@localhost root]# rpm -Uvh python2.3-2.3-5pydotorg.i386.rpm
    Preparing...                ########################################### [100%]
       1:python2.3              ########################################### [100%]
    [root@localhost root]# python          
    Python 2.2.2 (#1, Feb 24 2003, 19:13:11)
    [GCC 3.2.2 20030222 (Red Hat Linux 3.2.2-4)] on linux2
    Type "help", "copyright", "credits", or "license" for more information.
    >>> [press Ctrl+D to exit]
    [root@localhost root]# python2.3       
    Python 2.3 (#1, Sep 12 2003, 10:53:56)
    [GCC 3.2.2 20030222 (Red Hat Linux 3.2.2-5)] on linux2
    Type "help", "copyright", "credits", or "license" for more information.
    >>> [press Ctrl+D to exit]
    [root@localhost root]# which python2.3 
    /usr/bin/python2.3



[![1](../images/callouts/1.png)](#install.unix.1.1) Whoops! Just typing **`python`** gives you the older version of Python -- the one that was installed by default. That's not the one you want. 

[![2](../images/callouts/2.png)](#install.unix.1.2) At the time of this writing, the newest version is called **`python2.3`**. You'll probably want to change the path on the first line of the sample scripts to point to the newer version. 

[![3](../images/callouts/3.png)](#install.unix.1.3) This is the complete path of the newer version of Python that you just installed. Use this on the `#!` line (the first line of each script) to ensure that scripts are running under the latest version of Python, and be sure to type **`python2.3`** to get into the interactive shell. 

  

