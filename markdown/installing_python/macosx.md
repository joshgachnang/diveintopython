

1.3. Python on Mac OS X
-----------------------

On Mac OS X, you have two choices for installing Python: install it, or
don't install it. You probably want to install it.

Mac OS X 10.2 and later comes with a command-line version of Python
preinstalled. If you are comfortable with the command line, you can use
this version for the first third of the book. However, the preinstalled
version does not come with an XML parser, so when you get to the XML
chapter, you'll need to install the full version.

Rather than using the preinstalled version, you'll probably want to
install the latest version, which also comes with a graphical
interactive shell.

### Procedure 1.3. Running the Preinstalled Version of Python on Mac OS X

To use the preinstalled version of Python, follow these steps:

1.  Open the `/Applications` folder.

2.  Open the `Utilities` folder.

3.  Double-click `Terminal` to open a terminal window and get to a
    command line.

4.  Type **`python`** at the command prompt.

Try it out:

    Welcome to Darwin!
    [localhost:~] you% python
    Python 2.2 (#1, 07/14/02, 23:25:09)
    [GCC Apple cpp-precomp 6.14] on darwin
    Type "help", "copyright", "credits", or "license" for more information.
    >>> [press Ctrl+D to get back to the command prompt]
    [localhost:~] you% 

### Procedure 1.4. Installing the Latest Version of Python on Mac OS X

Follow these steps to download and install the latest version of Python:

1.  Download the `MacPython-OSX` disk image from
    [http://homepages.cwi.nl/\~jack/macpython/download.html](http://homepages.cwi.nl/~jack/macpython/download.html).

2.  If your browser has not already done so, double-click
    `MacPython-OSX-2.3-1.dmg` to mount the disk image on your desktop.

3.  Double-click the installer, `MacPython-OSX.pkg`.

4.  The installer will prompt you for your administrative username and
    password.

5.  Step through the installer program.

6.  After installation is complete, close the installer and open the
    `/Applications` folder.

7.  Open the `MacPython-2.3` folder

8.  Double-click `PythonIDE` to launch Python.

The MacPython IDE should display a splash screen, then take you to the
interactive shell. If the interactive shell does not appear, select
Window-\>Python Interactive (****Cmd**-0**). The opening window will
look something like this:

    Python 2.3 (#2, Jul 30 2003, 11:45:28)
    [GCC 3.1 20020420 (prerelease)]
    Type "copyright", "credits" or "license" for more information.
    MacPython IDE 1.0.1
    >>> 

Note that once you install the latest version, the pre-installed version
is still present. If you are running scripts from the command line, you
need to be aware which version of Python you are using.

### Example 1.1. Two versions of Python

    [localhost:~] you% python
    Python 2.2 (#1, 07/14/02, 23:25:09)
    [GCC Apple cpp-precomp 6.14] on darwin
    Type "help", "copyright", "credits", or "license" for more information.
    >>> [press Ctrl+D to get back to the command prompt]
    [localhost:~] you% /usr/local/bin/python
    Python 2.3 (#2, Jul 30 2003, 11:45:28)
    [GCC 3.1 20020420 (prerelease)] on darwin
    Type "help", "copyright", "credits", or "license" for more information.
    >>> [press Ctrl+D to get back to the command prompt]
    [localhost:~] you% 

  

