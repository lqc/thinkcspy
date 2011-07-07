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

.. index:: file   
    
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

Opening a file creates a file object. In this example, the variable ``myfile``
refers to the new object.

.. sourcecode:: python
    
    myfile = open('test.dat', 'w')

The open function takes two arguments. The first is the name of the file, and
the second is the **mode**. Mode ``'w'`` means that we are opening the file for
writing.

If there is no file named ``test.dat``, it will be created. If there already is
one, it will be replaced by the file we are writing.

To put data in the file we invoke the ``write`` method on the object:

.. sourcecode:: python
    
    myfile.write("Now is the time")
    myfile.write("to close the file")

Closing the file tells the system that we are done writing and makes
the file available for reading:

.. sourcecode:: python
    
    myfile.close()

Now we can open the file again, this time for reading, and read the
contents into a string. This time, the mode argument is ``'r'`` for reading:

.. sourcecode:: python
    
    >>> myfile = open('test.dat', 'r')

If we try to open a file that doesn't exist, we get an error:

.. sourcecode:: python
    
    >>> myfile = open('test.cat', 'r')
    IOError: [Errno 2] No such file or directory: 'test.cat'

Not surprisingly, the ``read`` method reads data from the file. With no
arguments, it reads the entire contents of the file into a single
string:

.. sourcecode:: python
    
    >>> text = myfile.read()
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
        infile = open(oldfile, 'r')
        outfile = open(newfile, 'w')
        while True:
            text = infile.read(50)
            if text == "":
                break
            outfile.write(text)
        infile.close()
        outfile.close()

This functions continues looping, reading 50 characters from ``infile`` and
writing the same 50 charaters to ``outfile`` until the end of ``infile`` is
reached, at which point ``text`` is empty and the ``break`` statement is
executed.

.. index:: file; text,  text file

Text files
----------

A **text file** is a file that contains printable characters and whitespace,
organized into lines separated by newline characters.  Since Python is
specifically designed to process text files, it provides methods that make the
job easy.

Notice the subtle difference in abstraction here: in the previous section, we
simply regarded a file as containing many characters, and could read them one
at a time, many at a time, or all at once.  In this section, specifically for
reading data, we're interested in files that are organized into lines, 
and will process them line-at-a-time.

To demonstrate, we'll create a text file with three lines of text separated by
newlines:

.. sourcecode:: python
    
    >>> outfile = open("test.dat","w")
    >>> outfile.write("line one\nline two\nline three\n")
    >>> outfile.close()

The ``readline`` method reads all the characters up to and including the
next newline character:

.. sourcecode:: python
    
    >>> infile = open("test.dat","r")
    >>> print(infile.readline())
    line one
       
    >>>


``readlines`` returns all of the remaining lines as a list of strings:

.. sourcecode:: python

    
    >>> print(infile.readlines())
    ['line two\n', 'line three\n']


In this case, the output is in list format, which means that the
strings appear with quotation marks and the newline character appears
at the end of each.

At the end of the file, ``readline`` returns the empty string and
``readlines`` returns the empty list:

.. sourcecode:: python
    
    >>> print(infile.readline())
       
    >>> print(infile.readlines())
    []

The following is an example of a line-processing program. ``filter`` makes a
copy of ``oldfile``, omitting any lines that begin with ``#``:

.. sourcecode:: python
    
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
        return

The **continue statement** ends the current iteration of the loop, but
continues looping. The flow of execution moves to the top of the loop, checks
the condition, and proceeds accordingly.

Thus, if ``text`` is the empty string, the loop exits. If the first character
of ``text`` is a hash mark, the flow of execution goes to the top of the loop.
Only if both conditions fail do we copy ``text`` into the new file.

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
simple example that copies a web URL to a local file, and then opens
and prints the file contents using the techniques we've covered above.

.. sourcecode:: python
    :linenos:
    
    import urllib.request

    url = 'http://www.cs.ru.ac.za/courses/CSc102/pythons.txt' 
    destination_filename = 'c:\\temp\\tempfile.txt'
    
    wf = urllib.request.urlretrieve(url, destination_filename)

    f = open(destination_filename)
    s = f.read()
    f.close()
    print(s)
    
The ``urlretrieve`` function collects the resource at the url, and
saves it to a local file.  You could use this to download any kind
of content from Internet.
   
You'll need to get a few things right before this works:  
 * The page you're trying to fetch must exist!  Check this using a browser.
 * You'll need permission to write to the destination filename.
 * If you are behind a proxy server, (as many students are), this may
   require some more special handling to work around your proxy. 
   Use a local text resource for the purpose of this demonstration! 
  

Counting Letters
----------------

The ``ord`` function returns the integer representation of a character:

.. sourcecode:: python
    
    >>> ord('a')
    97
    >>> ord('A')
    65
    >>>

This example explains why ``'Apple' < 'apple'`` evaluates to ``True``.

The ``chr`` function is the inverse of ``ord``. It takes an integer as an
argument and returns its character representation:

.. sourcecode:: python
    
    >>> for i in range(65, 71):
    ...     print(chr(i))
    ...
    A
    B
    C
    D
    E
    F
    >>>

The following program, ``countletters.py`` counts the number of times each
character occurs in the book `Alice in Wonderland <./resources/ch10/alice_in_wonderland.txt>`__:

.. sourcecode:: python
    
    #
    # countletters.py
    #
    
    def display(i):
        if i == 10: return 'LF'
        if i == 13: return 'CR' 
        if i == 32: return 'SPACE' 
        return chr(i)
    
    infile = open('alice_in_wonderland.txt', 'r')
    text = infile.read()
    infile.close()
    
    counts = 128 * [0]
    
    for letter in text:
        counts[ord(letter)] += 1
    
    layout = "{0:>12} {1:>5}\n"
    outfile = open('alice_counts.dat', 'w')
    outfile.write(layout.format("Character", "Count"))
    outfile.write("============ =====\n")
    
    for i in range(len(counts)):
        if counts[i] > 0:
            outfile.write(layout.format(display(i), counts[i]))
    
    outfile.close()

Run this program and look at the output file it generates using a text editor.
You will be asked to analyze the program in the exercises below.


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

    volatile memory
        Memory which requires an electrical current to maintain state. The
        *main memory* or RAM of a computer is volatile.  Information stored in
        RAM is lost when the computer is turned off.
 
Exercises
---------
   
#. Give the Python interpreter's response to each of the following from a
   continuous interpreter session:

   .. sourcecode:: python
    
      >>> s = "If we took the bones out, it wouldn't be crunchy, would it?"
      >>> s.split()
      >>> type(s.split())
      >>> s.split('o')
      >>> s.split('i')
      >>> '0'.join(s.split('o'))
          
   Be sure you understand why you get each result. Then apply what you have
   learned to fill in the body of the function below using the ``split`` and
   ``join`` methods of ``str`` objects:

   .. sourcecode:: python
    
        def myreplace(old, new, s):
            """ Replace all occurences of old with new in the string s. """
            ...
            
            
        test(myreplace(',', ';', 'this, that, and some other thing'),
                                 'this; that; and some other thing')
        test(myreplace(' ', '**', 'Words will now      be  separated by stars.'),
                                  'Words**will**now**be**separated**by**stars.')
    
   Your solution should pass the tests.
   
#. Create a module named ``wordtools.py`` with our test scaffolding in place.

   Now add functions to these tests pass::
   
        test(cleanword('what?'),  'what')
        test(cleanword('"now!"'), 'now')
        test(cleanword('?+="w-o-r-d!,@$()"'),  'word')
    
        test(has_dashdash('distance--but'), True)
        test(has_dashdash('several'), False)
        test(has_dashdash('spoke--'), True)
        test(has_dashdash('distance--but'), True)
        test(has_dashdash('-yo-yo-'), False)

        test(extract_words('Now is the time!  "Now", is the time? Yes, now.'),
              ['now', 'is', 'the', 'time', 'now', 'is', 'the', 'time', 'yes', 'now'])
        test(extract_words('she tried to curtsey as she spoke--fancy'),
              ['she', 'tried', 'to', 'curtsey', 'as', 'she', 'spoke', 'fancy'])
    
        test(wordcount('now', ['now', 'is', 'time', 'is', 'now', 'is', 'is']), 2)
        test(wordcount('is', ['now', 'is', 'time', 'is', 'now', 'is', 'the', 'is']), 4)
        test(wordcount('time', ['now', 'is', 'time', 'is', 'now', 'is', 'is']), 1)
        test(wordcount('frog', ['now', 'is', 'time', 'is', 'now', 'is', 'is']), 0)
    
        test(wordset(['now', 'is', 'time', 'is', 'now', 'is', 'is']), 
              ['is', 'now', 'time'])
        test(wordset(['I', 'a', 'a', 'is', 'a', 'is', 'I', 'am']),
              ['I', 'a', 'am', 'is'])
        test(wordset(['or', 'a', 'am', 'is', 'are', 'be', 'but', 'am']),
              ['a', 'am', 'are', 'be', 'but', 'is', 'or'])
       
        test(longestword(['a', 'apple', 'pear', 'grape']), 5)
        test(longestword(['a', 'am', 'I', 'be']), 2)
        test(longestword(['this', 'that', 'supercalifragilisticexpialidocious']), 34)
        test(longestword([ ]), 0)

   Save this module so you can use the tools it contains in future programs.
   
#. `unsorted_fruits.txt <resources/ch10/unsorted_fruits.txt>`__ contains a
   list of 26 fruits, each one with a name that begins with a different letter
   of the alphabet. Write a program named ``sort_fruits.py`` that reads in the
   fruits from ``unsorted_fruits.txt`` and writes them out in alphabetical
   order to a file named ``sorted_fruits.txt``.
   
#. Answer the following questions about ``countletters.py``:

   a. Explain in detail what the three lines do:

      .. sourcecode:: python
        
            infile = open('alice_in_wonderland.txt', 'r')
            text = infile.read()
            infile.close()

      What would ``type(text)`` return after these lines have been executed?
      
   b. What does the expression ``128 * [0]`` evaluate to? Read about `ASCII
      <http://en.wikipedia.org/wiki/ASCII>`__ in Wikipedia and explain why you 
      think the variable, ``counts`` is assigned to ``128 * [0]`` in light of
      what you read.
      
   c. What does

      .. sourcecode:: python
        
            for letter in text:
                counts[ord(letter)] += 1

      do to ``counts``?
      
   d. Explain the purpose of the ``display`` function. Why does it check for
      values ``10``, ``13``, and ``32``? What is special about those values?
      
   e. Describe in detail what the lines

      .. sourcecode:: python
        
            layout = "{0:>9} {1:>5}\n"
            outfile = open('alice_counts.dat', 'w')
            outfile.write(layout.format("Character", "Count"))
                          outfile.write("========= =====\n")

      do. What will be in ``alice_counts.dat`` when they finish executing?
      
   f. Finally, explain in detail what

      .. sourcecode:: python
        
            for i in range(len(counts)):
                if counts[i] > 0:
                    outfile.write(layout.format(display(i), counts[i]))

      does. 

