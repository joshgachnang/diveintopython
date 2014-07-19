

12.2. Installing the SOAP Libraries
-----------------------------------

-   [12.2.1. Installing PyXML](install.html#d0e29967)
-   [12.2.2. Installing fpconst](install.html#d0e30070)
-   [12.2.3. Installing SOAPpy](install.html#d0e30171)

Unlike the other code in this book, this chapter relies on libraries
that do not come pre-installed with Python.

Before you can dive into SOAP web services, you'll need to install three
libraries: PyXML, fpconst, and SOAPpy.

### 12.2.1. Installing PyXML

The first library you need is PyXML, an advanced set of XML libraries
that provide more functionality than the built-in XML libraries we
studied in [Chapter 9](../xml_processing/index.html).

### Procedure 12.1. 

Here is the procedure for installing PyXML:

1.  Go to
    [http://pyxml.sourceforge.net/](http://pyxml.sourceforge.net/),
    click Downloads, and download the latest version for your operating
    system.

2.  If you are using Windows, there are several choices. Make sure to
    download the version of PyXML that matches the version of Python you
    are using.

3.  Double-click the installer. If you download PyXML 0.8.3 for Windows
    and Python 2.3, the installer program will be
    `PyXML-0.8.3.win32-py2.3.exe`.

4.  Step through the installer program.

5.  After the installation is complete, close the installer. There will
    not be any visible indication of success (no programs installed on
    the Start Menu or shortcuts installed on the desktop). PyXML is
    simply a collection of XML libraries used by other programs.

To verify that you installed PyXML correctly, run your Python IDE and
check the version of the XML libraries you have installed, as shown
here.

### Example 12.3. Verifying PyXML Installation

    >>> import xml
    >>> xml.__version__
    '0.8.3'

This version number should match the version number of the PyXML
installer program you downloaded and ran.

### 12.2.2. Installing fpconst

The second library you need is fpconst, a set of constants and functions
for working with IEEE754 double-precision special values. This provides
support for the special values Not-a-Number (NaN), Positive Infinity
(Inf), and Negative Infinity (-Inf), which are part of the SOAP datatype
specification.

### Procedure 12.2. 

Here is the procedure for installing fpconst:

1.  Download the latest version of fpconst from
    [http://www.analytics.washington.edu/statcomp/projects/rzope/fpconst/](http://www.analytics.washington.edu/statcomp/projects/rzope/fpconst/).

2.  There are two downloads available, one in `.tar.gz` format, the
    other in `.zip` format. If you are using Windows, download the
    `.zip` file; otherwise, download the `.tar.gz` file.

3.  Decompress the downloaded file. On Windows XP, you can right-click
    on the file and choose Extract All; on earlier versions of Windows,
    you will need a third-party program such as WinZip. On Mac OS X, you
    can double-click the compressed file to decompress it with Stuffit
    Expander.

4.  Open a command prompt and navigate to the directory where you
    decompressed the fpconst files.

5.  Type **`python setup.py install`** to run the installation program.

To verify that you installed fpconst correctly, run your Python IDE and
check the version number.

### Example 12.4. Verifying fpconst Installation

    >>> import fpconst
    >>> fpconst.__version__
    '0.6.0'

This version number should match the version number of the fpconst
archive you downloaded and installed.

### 12.2.3. Installing SOAPpy

The third and final requirement is the SOAP library itself: SOAPpy.

### Procedure 12.3. 

Here is the procedure for installing SOAPpy:

1.  Go to
    [http://pywebsvcs.sourceforge.net/](http://pywebsvcs.sourceforge.net/)
    and select Latest Official Release under the SOAPpy section.

2.  There are two downloads available. If you are using Windows,
    download the `.zip` file; otherwise, download the `.tar.gz` file.

3.  Decompress the downloaded file, just as you did with fpconst.

4.  Open a command prompt and navigate to the directory where you
    decompressed the SOAPpy files.

5.  Type **`python setup.py install`** to run the installation program.

To verify that you installed SOAPpy correctly, run your Python IDE and
check the version number.

### Example 12.5. Verifying SOAPpy Installation

    >>> import SOAPpy
    >>> SOAPpy.__version__
    '0.11.4'

This version number should match the version number of the SOAPpy
archive you downloaded and installed.

  

