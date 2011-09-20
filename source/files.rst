..  Copyright (C) Peter Wentworth, Jeffrey Elkner, Allen B. Downey and Chris Meyers.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with Invariant Sections being Foreword, Preface, and Contributor List, no
    Front-Cover Texts, and no Back-Cover Texts.  A copy of the license is
    included in the section entitled "GNU Free Documentation License".
 
|    
    
Files
=====

.. index:: file, handle, file handle   
    
Reading and writing files
-------------------------

While a program is running, its data is stored in *random access memory* (RAM).
RAM is fast and inexpensive, but it is also **volatile**, which means that when
the program ends, or the computer shuts down, data in RAM disappears. To make
data available the next time you turn on your computer and start your program,
you have to write it to a **non-volatile** storage medium, such a hard drive,
usb drive, or CD-RW.

Data on non-volatile storage media is stored in named locations on the media
called **files**. By reading and writing files, programs can save information
between program runs.

Working with files is a lot like working with a notebook. To use a notebook,
you have to open it. When you're done, you have to close it.  While the
notebook is open, you can either write in it or read from it. In either case,
you know where you are in the notebook. You can read the whole notebook in its
natural order or you can skip around.

All of this applies to files as well. To open a file, you specify its name and
indicate whether you want to read or write. 

Opening a file creates what we call a file **handle**. In this example, the variable ``myfile``
refers to the new handle object.  Our program calls methods on the handle, and this makes
changes to the actual file which is usually located on our disk.    

.. sourcecode:: python
    
    myfile = open('test.dat', 'w')

The open function takes two arguments. The first is the name of the file, and
the second is the **mode**. Mode ``'w'`` means that we are opening the file for
writing.

If there is no file named ``test.dat`` on the disk, it will be created. If there already is
one, it will be replaced by the file we are writing.

To put data in the file we invoke the ``write`` method on the handle:

.. sourcecode:: python
    
    myfile.write("Now is the time")
    myfile.write("to close the file")

Closing the file handle tells the system that we are done writing and makes
the disk file available for reading by other programs (or by ourselves):

.. sourcecode:: python
    
    myfile.close()

Now we can open the file again, this time for reading, and read the
contents into a string. This time, the mode argument is ``'r'`` for reading:

.. sourcecode:: python
    
    >>> mynewhandle = open('test.dat', 'r')

If we try to open a file that doesn't exist, we get an error:

.. sourcecode:: python
    
    >>> mynewhandle = open('test.cat', 'r')
    IOError: [Errno 2] No such file or directory: 'test.cat'

Not surprisingly, the ``read`` method reads data from the file. With no
arguments, it reads the entire contents of the file into a single
string:

.. sourcecode:: python
    
    >>> text = mynewhandle.read()
    >>> print(text)
    Now is the timeto close the file

There is no space between time and to because we did not write a space
between the strings.

``read`` can also take an argument that indicates how many characters to read:

.. sourcecode:: python
    
    >>> myfile = open('test.dat', 'r')
    >>> print(myfile.read(5))
    Now i

If not enough characters are left in the file, ``read`` returns the remaining
characters. When we get to the end of the file, ``read`` returns the empty
string:

.. sourcecode:: python
    
    >>> print(myfile.read(1000006))
    s the timeto close the file
    >>> print(myfile.read())
       
    >>>

The following function copies a file, reading and writing up to fifty
characters at a time. The first argument is the name of the original file; the
second is the name of the new file:

.. sourcecode:: python
    
    def copy_file(oldfile, newfile):
        h_infile = open(oldfile, 'r')
        h_outfile = open(newfile, 'w')
        while True:
            text = h_infile.read(50)
            if text == "":
                break
            h_outfile.write(text)
        h_infile.close()
        h_outfile.close()

This functions continues looping, reading 50 characters from ``infile`` and
writing the same 50 characters to ``outfile`` until the end of ``infile`` is
reached, at which point ``text`` is empty and the ``break`` statement is
executed.

.. admonition:: A handle is somewhat like a TV remote control

    We're all familiar with a remote control for a TV.  You perform operations on
    the remote control --- switch channels, change the volume, etc.  But the real action
    happens on the TV.  So, by simple analogy, we'd call the remote control your `handle`
    to the underlying TV.
    
    Sometimes we want to emphasize the difference --- the file handle is not the same
    as the file, and the remote control is not the same as the TV it controls.  
    But at other times we prefer to treat them as a single mental chunk, or abstraction, 
    and we'll just say "close the file", or "flip the TV channel". 

.. index:: file; text,  text file

Text files
----------

A **text file** is a file that contains printable characters and whitespace,
organized into lines separated by newline characters.  One of the Python
design goals was to provide methods that made text file processing easy. 

Notice the subtle difference in abstraction here: in the previous section, we
simply regarded a file as containing many characters, and could read them one
at a time, many at a time, or all at once.  In this section, particularly for
reading data, we're interested in files that are organized into lines, 
and we will process them line-at-a-time.

To demonstrate, we'll create a text file with three lines of text separated by
newlines:

.. sourcecode:: python
    
    >>> h_outfile = open("test.dat","w")
    >>> h_outfile.write("line one\nline two\nline three\n")
    >>> h_outfile.close()

The ``readline`` method reads all the characters up to and including the
next newline character:

.. sourcecode:: python
    
    >>> h_infile = open("test.dat","r")
    >>> print(h_infile.readline())
    line one
       
    >>>


``readlines`` returns all of the remaining lines as a list of strings:

.. sourcecode:: python

    
    >>> print(h_infile.readlines())
    ['line two\n', 'line three\n']


In this case, the output is in list format, which means that the
strings appear with quotation marks and the newline character appears
at the end of each.

At the end of the file, ``readline`` returns the empty string and
``readlines`` returns the empty list:

.. sourcecode:: python
    
    >>> print(h_infile.readline())
       
    >>> print(h_infile.readlines())
    []

The following is an example of a line-processing program. ``filter`` makes a
copy of ``oldfile``, omitting any lines that begin with ``#``:

.. sourcecode:: python
   :linenos:
    
    def filter(oldfile, newfile):
        infile = open(oldfile, 'r')
        outfile = open(newfile, 'w')
        while True:
            text = infile.readline()
            if text == "":
               break
            if text[0] == '#':
               continue
            outfile.write(text)
        infile.close()
        outfile.close()

The **continue statement** ends the current iteration of the loop, but
continues looping. The flow of execution moves to the top of the loop, checks
the condition, and proceeds accordingly.

Thus, if ``text`` is the empty string, the loop exits. If the first character
of ``text`` is a hash mark, the flow of execution goes to the top of the loop.
Only if both conditions fail do we copy ``text`` into the new file.

Let's consider one more case: suppose your original file contained empty
lines.  At line 6 above, would this program not find the first empty line in the
file, and terminate immediately?   No!  Recall that ``readline`` always 
includes the newline character in the string it returns, so even an empty line in
your file would arrive in the ``text`` variable on line 5 containing its newline
character.  It is only when we try to read `beyond` the end of the file that we
we get back the empty string.  

.. index:: directory

Directories
-----------

Files on non-volatile storage media are organized by a set of rules known as a
**file system**. File systems are made up of files and **directories**, which
are containers for both files and other directories.

When you create a new file by opening it and writing, the new file goes in the
current directory (wherever you were when you ran the program). Similarly, when
you open a file for reading, Python looks for it in the current directory.

If you want to open a file somewhere else, you have to specify the **path** to
the file, which is the name of the directory (or folder) where the file is
located:

.. sourcecode:: python
    
    >>> wordsfile = open('/usr/share/dict/words', 'r')
    >>> wordlist = wordsfile.readlines()
    >>> print(wordlist[:6])
    ['\n', 'A\n', "A's\n", 'AOL\n', "AOL's\n", 'Aachen\n']

This (unix) example opens a file named ``words`` that resides in a directory named
``dict``, which resides in ``share``, which resides in ``usr``, which resides
in the top-level directory of the system, called ``/``. It then reads in each
line into a list using ``readlines``, and prints out the first 5 elements from
that list.  

A Windows path might be ``"c:/temp/words.txt"`` or ``"c:\\temp\\words.txt"``.
Because backslashes are used to escape things like newlines and tabs, you need 
to write two backslashes in a literal string to get one!  So the length of these two
strings is the same!

You cannot use ``/`` or ``\`` as part of a filename; they are reserved as a **delimiter**
between directory and filenames.

The file ``/usr/share/dict/words`` should exist on unix-based systems, and
contains a list of words in alphabetical order.


What about fetching something from the web?
-------------------------------------------

The Python libraries are pretty messy in places.  But here is a very
simple example that copies the contents at some web URL to a local file.

.. sourcecode:: python
    :linenos:
    
    import urllib.request

    url = 'http://xml.resource.org/public/rfc/txt/rfc793.txt' 
    destination_filename = 'rfc793.txt'
    
    urllib.request.urlretrieve(url, destination_filename)

The ``urlretrieve`` function --- just one call --- could be used
to download any kind of content from the Internet.
   
We'll need to get a few things right before this works:  
 * The resource we're trying to fetch must exist!  Check this using a browser.
 * We'll need permission to write to the destination filename, and the file will
   be created in the "current directory" - i.e. the same folder that the Python program is saved in.
 * If we are behind a proxy server that requires authentication, 
   (as some students are), this may require some more special handling to work around our proxy.  
   Use a local resource for the purpose of this demonstration! 
  
Here is a slightly different example.  Rather than save the web resource to
our local disk, we read it directly into a string, and return it:

.. sourcecode:: python
    :linenos:
    
    import urllib.request

    def retrieve_page(url):
        ''' Retrieve the contents of a web page.
            The contents is converted to a string before returning it.
        '''
        my_socket = urllib.request.urlopen(url)
        dta = str(my_socket.readall())  
        my_socket.close()
        return dta        

    the_text = retrieve_page("http://xml.resource.org/public/rfc/txt/rfc793.txt")
    print(the_text)
        
Opening the remote url returns what we call a **socket**.  This is a handle to 
our end of the connection between 
our program and the remote web server.  We can call read, write, and close methods on
the socket object in much the same way as we can work with a file handle.


Glossary
--------

.. glossary::


    delimiter
        A sequence of one or more characters used to specify the boundary
        between separate parts of text.

    directory
        A named collection of files, also called a folder.  Directories can
        contain files and other directories, which are refered to as
        *subdirectories* of the directory that contains them.

    file
        A named entity, usually stored on a hard drive, floppy disk, or CD-ROM,
        that contains a stream of characters.

    file system
        A method for naming, accessing, and organizing files and the data they
        contain. 
        
    handle
        An object in our program that is connected to an underlying resource (e.g. a file).
        The file handle lets our program manipulate / read/ write / close the actual 
        file that is on our disk.
            
    fully qualified name
        A name that is prefixed by some namespace identifier and the dot operator, or
        by an instance object, e.g. ``math.sqrt`` or ``tess.forward(10)``.

    mode
        A distinct method of operation within a computer program.  Files in
        Python can be openned in one of three modes: read (``'r'``), write
        (``'w'``), and append (``'a'``).
     
    non-volatile memory
        Memory that can maintain its state without power. Hard drives, flash
        drives, and rewritable compact disks (CD-RW) are each examples of
        non-volatile memory.

    path
        A sequence of directory names that specifies the exact location of a
        file.
        
    text file
        A file that contains printable characters organized into lines
        separated by newline characters.
        
    socket
        One end of a connection allowing one to read and write 
        information to or from another computer.  

    volatile memory
        Memory which requires an electrical current to maintain state. The
        *main memory* or RAM of a computer is volatile.  Information stored in
        RAM is lost when the computer is turned off.
 
Exercises
---------
      
#. `unsorted_fruits.txt <resources/ch10/unsorted_fruits.txt>`__ contains a
   list of 26 fruits, each one with a name that begins with a different letter
   of the alphabet. Write a program named ``sort_fruits.py`` that reads in the
   fruits from ``unsorted_fruits.txt`` and writes them out in alphabetical
   order to a file named ``sorted_fruits.txt``.
   
