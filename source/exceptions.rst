..  Copyright (C)  Peter Wentworth, Jeffrey Elkner, Allen B. Downey and Chris Meyers.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with Invariant Sections being Foreword, Preface, and Contributor List, no
    Front-Cover Texts, and no Back-Cover Texts.  A copy of the license is
    included in the section entitled "GNU Free Documentation License".
 
|      
    
Exceptions
==========


.. index:: exception, handling an exception, exception; handling, try ... except 

Catching exceptions
-------------------

Whenever a runtime error occurs, it creates an **exception** object. The program stops
running at this point and Python prints out the traceback, which ends with a message
describing the exception that occurred.

For example, dividing by zero creates an exception:

    .. sourcecode:: python3
        
        >>> print(55/0)
        Traceback (most recent call last):
          File "<interactive input>", line 1, in <module>
        ZeroDivisionError: integer division or modulo by zero
        >>>

So does accessing a non-existent list item:

    .. sourcecode:: python3
        
        >>> a = []
        >>> print(a[5])
        Traceback (most recent call last):
          File "<interactive input>", line 1, in <module>
        IndexError: list index out of range
        >>>

Or trying to make an item assignment on a tuple:

    .. sourcecode:: python3
        
        >>> tup = ('a', 'b', 'd', 'd')
        >>> tup[2] = 'c' 
        Traceback (most recent call last):
          File "<interactive input>", line 1, in <module>
        TypeError: 'tuple' object does not support item assignment
        >>>

In each case, the error message on the last line has two parts: the type of
error before the colon, and specifics about the error after the colon.

Sometimes we want to execute an operation that might cause an exception, but we
don't want the program to stop. We can **handle the exception** using the
``try`` statement to "wrap" a region of code.  

For example, we might prompt the user for the name of a file and then try to
open it. If the file doesn't exist, we don't want the program to crash; we want
to handle the exception:

    .. sourcecode:: python3
        :linenos:
        
        filename = input('Enter a file name: ')
        try:
            f = open(filename, 'r')
        except:
            print('There is no file named', filename)

The ``try`` statement has three separate clauses, or parts, 
introduced by the keywords ``try`` ... ``except`` ... ``finally``.
The ``finally`` clause can be omitted, so we'll consider the two-clause version
of the ``try`` statement first.        
        
The ``try`` statement executes and monitors the statements in the first block. If no
exceptions occur, it skips the block under the ``except`` clause. If any exception occurs,
it executes the statements in the ``except`` clause and then continues.

We could encapsulate this capability in a function: ``exists`` which takes a filename
and returns true if the file exists, false if it doesn't:

    .. sourcecode:: python3
        :linenos:
        
        def exists(filename):
            try:
                f = open(filename)
                f.close()
                return True 
            except:
                return False 

    .. admonition:: A template to test if a file exists, without using exceptions

        The function we've just shown is not one we'd recommend. It opens
        and closes the file, which is semantically different from asking "does
        it exist?". How?  Firstly, it might update some timestamps on the file.  
        Secondly, it might tell you that there is no such file if some other 
        program already happens to have the file open, or if your permissions 
        settings don't allow you to open the file.

        Python provides a module called ``os.path`` (this is the first
        time we've seen a dotted module name with two namespace components). It
        provides a number of useful functions to work with paths, files and directories,
        so you should check out the help.  
        
            .. sourcecode:: python3
                :linenos:
            
                import os.path
                
                # This is the preferred way to check if a file exists.
                if os.path.isfile("c:/temp/testdata.txt"):
                   ...
           
   
            
You can use multiple ``except`` clauses to handle different kinds of exceptions
(see the `Errors and Exceptions <http://docs.python.org/tut/node10.html>`__
lesson from Python creator Guido van Rossum's `Python Tutorial
<http://docs.python.org/tut/tut.html>`__ for a more complete discussion of
exceptions).  So your program could do one thing if the file does not exist,
but do something else if the file was in use by another program.

Raising your own exceptions
---------------------------

Can your program deliberately cause its own exceptions?  
If your program detects an error condition, you can **raise** an
exception. Here is an example that gets input from the user and checks that the
number is non-negative:

    .. sourcecode:: python3
       :linenos:
        
        def get_age():
            age = int(input('Please enter your age: '))
            if age < 0:
                # Create a new instance of an exception 
                myError = ValueError('{0} is not a valid age'.format(age))
                raise myError     
            return age
  

Line 4 creates an exception object, in this case, a ValueError 
object, which encapsulates your specific information about the error. The ``raise`` 
statement on line 5 carries this object out as a kind of "return value", and 
immediately exits from the function, and its caller, and its caller, until it 
encounters a ``try ... except`` that can handle the exception.   We call this 
"unwinding the call stack".

``ValueError`` is one of the built-in exception types which
most closely matches the kind of error we want to raise. The complete listing
of built-in exceptions is found in  the `Built-in Exceptions
<http://docs.python.org/lib/module-exceptions.html>`__ section of the `Python 
Library Reference <http://docs.python.org/lib/>`__, again by Python's creator, 
Guido van Rossum.

If the function that called ``get_age`` (or its caller, or their caller, ...) 
handles the error, then the program can
carry on running; otherwise, Python prints the traceback and exits:

    .. sourcecode:: python3
        
        >>> get_age()
        Please enter your age: 42
        42 
        >>> get_age()
        Please enter your age: -2
        Traceback (most recent call last):
          File "<interactive input>", line 1, in <module>
          File "learn_exceptions.py", line 4, in get_age
            raise ValueError('{0} is not a valid age'.format(age))
        ValueError: -2 is not a valid age
        >>>

The error message includes the exception type and the additional information
that was provided when the exception object was first created.

It is often the case that lines 4 and 5 (creating the exception object, then raising
the exception) are combined into a single statement, but there are really two different
and independent things happening, so perhaps it makes sense to keep the two
steps separate when we first learn to work with exceptions.   
Here we show it all in a single statement:

    .. sourcecode:: python3
        :linenos:
       
        raise ValueError('{0} is not a valid age'.format(age))
 

Revisiting an earlier example
-----------------------------

Using exception handling, we can now modify our ``recursion_depth`` example
from the previous chapter so that it stops when it reaches the 
maximum recursion depth allowed:

    .. sourcecode:: python3
        :linenos:
        
        def recursion_depth(number):
            print("Recursion depth number", number)
            try:
                recursion_depth(number + 1)
            except:
                print("I cannot go any deeper into this wormhole.")
        
        recursion_depth(0)

Run this version and observe the results.

.. index:: try ... except ... finally

The ``finally`` clause of the ``try`` statement
-----------------------------------------------

A common programming pattern is to grab a resource of some kind --- e.g. 
we create a window for turtles to draw on, or we dial up a connection to our
internet service provider, or we may open a file for writing.   
Then we perform some computation which may raise an exception, 
or may work without any problems.

Whatever happens, we want to "clean up" the resources we grabbed --- e.g. close
the window, disconnect our dial-up connection, or close the file.  The ``finally``
clause of the ``try`` statement is the way to do just this.  Consider
this (somewhat contrived) example:

    .. sourcecode:: python3
       :linenos:

        import turtle, time

        def show_poly():
            try:
                win = turtle.Screen()   # Grab/create a resource, eg a window 
                tess = turtle.Turtle()
                
                # This dialog could be cancelled, 
                # or the conversion to int might fail.
                n = int(input("How many sides do you want in your polygon?"))
                angle = 360 / n
                for i in range(n):      # Draw the polygon 
                    tess.forward(10)
                    tess.left(angle)
                time.sleep(3)           # make program wait a few seconds
            finally:         
                win.bye()               # close the turtle's window.


        show_poly()
        show_poly()
        show_poly()

In lines 19-21, ``show_poly`` is called three times.  Each one creates a new
window for its turtle, and draws a polygon with the number of sides
input by the user.  But what if the user enters a string that cannot be
converted to an ``int``?  What if they close the dialog?  We'll get an exception, 
*but even though we've had an exception, we still want to close the turtle's window*.  
Lines 16-17 does this for us.  Whether we complete the statements in the ``try`` 
clause successfully or not, the ``finally`` block will always be executed.

Notice that the exception is still unhandled --- only an ``except`` clause can
handle an exception, so your program will still crash.  But at least it's turtle 
window will be closed before it crashes! 


Glossary
--------

.. glossary::

    exception
        An error that occurs at runtime.

    handle an exception
        To prevent an exception from causing your program to crash, by wrapping
        the block of code in a ``try`` / ``except`` construct.

    immutable data type
        A data type which cannot be modified.  Assignments to elements or
        slices (sub-parts) of immutable types cause a runtime error.

     mutable data type
        A data type which can be modified. All mutable types are compound
        types.  Lists and dictionaries (see next chapter) are mutable data
        types; strings and tuples are not.

    raise
        To create a deliberate exception by using the ``raise`` statement.


Exercises
---------
   
                
#. Write a function named ``readposint`` that uses the ``input`` dialog to
   prompt the user for a positive
   integer and then checks the input to confirm that it meets the requirements. 
   It should be able to handle inputs that cannot be converted to int, as well
   as negative ints, and edge cases (e.g. when the user closes the dialog, or
   does not enter anything at all.)   
   

