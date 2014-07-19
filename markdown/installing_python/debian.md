

1.6. Python on Debian GNU/Linux
-------------------------------

If you are lucky enough to be running Debian GNU/Linux, you install
Python through the **apt** command.

### Example 1.3. Installing on Debian GNU/Linux

    localhost:~$ su -
    Password: [enter your root password]
    localhost:~# apt-get install python
    Reading Package Lists... Done
    Building Dependency Tree... Done
    The following extra packages will be installed:
      python2.3
    Suggested packages:
      python-tk python2.3-doc
    The following NEW packages will be installed:
      python python2.3
    0 upgraded, 2 newly installed, 0 to remove and 3 not upgraded.
    Need to get 0B/2880kB of archives.
    After unpacking 9351kB of additional disk space will be used.
    Do you want to continue? [Y/n] Y
    Selecting previously deselected package python2.3.
    (Reading database ... 22848 files and directories currently installed.)
    Unpacking python2.3 (from .../python2.3_2.3.1-1_i386.deb) ...
    Selecting previously deselected package python.
    Unpacking python (from .../python_2.3.1-1_all.deb) ...
    Setting up python (2.3.1-1) ...
    Setting up python2.3 (2.3.1-1) ...
    Compiling python modules in /usr/lib/python2.3 ...
    Compiling optimized python modules in /usr/lib/python2.3 ...
    localhost:~# exit
    logout
    localhost:~$ python
    Python 2.3.1 (#2, Sep 24 2003, 11:39:14)
    [GCC 3.3.2 20030908 (Debian prerelease)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> [press Ctrl+D to exit]

  

