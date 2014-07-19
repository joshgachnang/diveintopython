

1.2. Python on Windows
----------------------

On Windows, you have a couple choices for installing Python.

ActiveState makes a Windows installer for Python called ActivePython,
which includes a complete version of Python, an IDE with a Python-aware
code editor, plus some Windows extensions for Python that allow complete
access to Windows-specific services, APIs, and the Windows Registry.

ActivePython is freely downloadable, although it is not open source. It
is the IDE I used to learn Python, and I recommend you try it unless you
have a specific reason not to. One such reason might be that ActiveState
is generally several months behind in updating their ActivePython
installer when new version of Python are released. If you absolutely
need the latest version of Python and ActivePython is still a version
behind as you read this, you'll want to use the second option for
installing Python on Windows.

The second option is the “official” Python installer, distributed by the
people who develop Python itself. It is freely downloadable and open
source, and it is always current with the latest version of Python.

### Procedure 1.1. Option 1: Installing ActivePython

Here is the procedure for installing ActivePython:

1.  Download ActivePython from
    [http://www.activestate.com/Products/ActivePython/](http://www.activestate.com/Products/ActivePython/).

2.  If you are using Windows 95, Windows 98, or Windows ME, you will
    also need to download and install [Windows Installer
    2.0](http://download.microsoft.com/download/WindowsInstaller/Install/2.0/W9XMe/EN-US/InstMsiA.exe)
    before installing ActivePython.

3.  Double-click the installer, `ActivePython-2.2.2-224-win32-ix86.msi`.

4.  Step through the installer program.

5.  If space is tight, you can do a custom installation and deselect the
    documentation, but I don't recommend this unless you absolutely
    can't spare the 14MB.

6.  After the installation is complete, close the installer and choose
    Start-\>Programs-\>ActiveState ActivePython 2.2-\>PythonWin IDE.
    You'll see something like the following:

<!-- -->

    PythonWin 2.2.2 (#37, Nov 26 2002, 10:24:37) [MSC 32 bit (Intel)] on win32.
    Portions Copyright 1994-2001 Mark Hammond (mhammond@skippinet.com.au) -
    see 'Help/About PythonWin' for further copyright information.
    >>> 

### Procedure 1.2. Option 2: Installing Python from [Python.org](http://www.python.org/ "Python language home page")

1.  Download the latest Python Windows installer by going to
    [http://www.python.org/ftp/python/](http://www.python.org/ftp/python/)
    and selecting the highest version number listed, then downloading
    the `.exe` installer.

2.  Double-click the installer, `Python-2.xxx.yyy.exe`. The name will
    depend on the version of Python available when you read this.

3.  Step through the installer program.

4.  If disk space is tight, you can deselect the HTMLHelp file, the
    utility scripts (`Tools/`), and/or the test suite (`Lib/test/`).

5.  If you do not have administrative rights on your machine, you can
    select Advanced Options, then choose Non-Admin Install. This just
    affects where Registry entries and Start menu shortcuts are created.

6.  After the installation is complete, close the installer and select
    Start-\>Programs-\>Python 2.3-\>IDLE (Python GUI). You'll see
    something like the following:

<!-- -->

    Python 2.3.2 (#49, Oct  2 2003, 20:02:00) [MSC v.1200 32 bit (Intel)] on win32
    Type "copyright", "credits" or "license()" for more information.

        ****************************************************************
        Personal firewall software may warn about the connection IDLE
        makes to its subprocess using this computer's internal loopback
        interface.  This connection is not visible on any external
        interface and no data is sent to or received from the Internet.
        ****************************************************************
        
    IDLE 1.0
    >>> 

  

