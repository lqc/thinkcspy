..  Copyright (C)  Peter Wentworth, Jeffrey Elkner, Allen B. Downey and Chris Meyers.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with Invariant Sections being Foreword, Preface, and Contributor List, no
    Front-Cover Texts, and no Back-Cover Texts.  A copy of the license is
    included in the section entitled "GNU Free Documentation License".
 
|      
    
Tuples
======

.. index:: mutable, immutable, tuple

Tuples and mutability
---------------------

So far, you have seen two compound types: strings, which are made up of
characters; and lists, which are made up of elements of any type.  One of the
differences we noted is that the elements of a list can be modified, but the
characters in a string cannot. In other words, strings are **immutable** and
lists are **mutable**.

A **tuple**, like a list, is a sequence of items of any type. Unlike lists,
however, tuples are immutable. Syntactically, a tuple is a comma-separated
sequence of values.  Although it is not necessary, it is conventional to 
enclose tuples in parentheses:

.. sourcecode:: python
    
    >>> julia = ("Julia", "Roberts", 1967, "Duplicity", 2009, "Actress", "Atlanta, Georgia")
    
Tuples are useful for representing what other languages often call *records* ---
some related information that belongs together, like your student record.  There is
no description of what each of these *fields* means, but we can guess.  A tuple
lets us "chunk" together related information and use it as a single thing.
 
Tuples support the same sequence operations as strings and
lists. The index operator selects an element from a tuple.

.. sourcecode:: python
    
    >>> julia[2]
    1967

But if we try to use item assignment to modify one of the elements of the
tuple, we get an error:

.. sourcecode:: python
    
    >>> julia[0] = 'X'
    TypeError: 'tuple' object does not support item assignment

Of course, even if we can't modify the elements of a tuple, we can make a variable
reference a new tuple holding different information.  To construct the new tuple,
it is convenient that we can slice parts of the old tuple and join up the
bits to make the new tuple.  So ``julia`` has a new recent film, and we might want
to change her tuple:

.. sourcecode:: python
    
    >>> julia = julia[:3] + ("Eat Pray Love", 2010) + julia[5:]
    >>> julia
    ('Julia', 'Roberts', 1967, 'Eat Pray Love', 2010, 'Actress', 'Atlanta, Georgia')


To create a tuple with a single element (but you're probably not likely
to do that too often), we have to include the final comma, because without
the final comma, Python treats the ``(5)`` below as an integer in parentheses:

.. sourcecode:: python
    
    >>> tup = (5,)
    >>> type(tup)
    <class 'tuple'> 
    >>> x = (5)
    >>> type(x)
    <class 'int'>     
    
.. index::
    single: assignment; tuple 
    single: tuple; assignment  
  
Tuple assignment
----------------

Python has a very powerful **tuple assignment** feature that allows a tuple of variables 
on the left of an assignment to be assigned values from a tuple
on the right of the assignment.

.. sourcecode:: python
    
    (name, surname, birth_year, movie, movie_year, profession, birth_place) = julia
    
This does the equivalent of seven assignment statements, all on one easy line.  
One requirement is that the number of variables on the left must match the number
of elements in the tuple. 
     
Once in a while, it is useful to swap the values of two variables.  With
conventional assignment statements, we have to use a temporary variable. For
example, to swap ``a`` and ``b``:

.. sourcecode:: python
    
    temp = a
    a = b
    b = temp

Tuple assignment solves this problem neatly:

.. sourcecode:: python
    
    (a, b) = (b, a)

The left side is a tuple of variables; the right side is a tuple of values.
Each value is assigned to its respective variable. All the expressions on the
right side are evaluated before any of the assignments. This feature makes
tuple assignment quite versatile.

Naturally, the number of variables on the left and the number of values on the
right have to be the same:

.. sourcecode:: python
    
    >>> (a, b, c, d) = (1, 2, 3)
    ValueError: need more than 3 values to unpack 

.. index::
    single: tuple; return value 

Tuples as return values
-----------------------

Functions can return tuples as return values. This is very useful --- we often want to
know some batsman's highest and lowest score, or we want to find the mean and the standard 
deviation, or we want to know the year, the month, and the day, or if we're doing some
some ecological modelling we may want to know the number of rabbits and the number
of wolves on an island at a given time.  In each case, a function (which 
can only return a single value), can create a single tuple holding multiple elements. 

For example, we could write a function that returns both the area and the circumference
of a circle of radius r:

.. sourcecode:: python
    
    def f(r):
        """ Return (circumference, area) of a circle of radius r """
        c = 2 * math.pi * r
        a = math.pi * r * r
        return (c, a)
    

Glossary
--------

.. glossary::


    data structure
        An organization of data for the purpose of making it easier to use.

    immutable data type
        A data type which cannot be modified.  Assignments to elements or
        slices (sub-parts) of immutable types cause a runtime error.

    mutable data type
        A data type which can be modified. All mutable types are compound
        types.  Lists and dictionaries (see next chapter) are mutable data
        types; strings and tuples are not.

    tuple
        An immutable data type that contains related elements. Tuples are used
        to group together related data, such as a person's name, their age, 
        and their gender.  Tuples can be used wherever an immutable type
        is required, such as for a key in a dictionary (see the next chapter).

    tuple assignment
        An assignment to all of the elements in a tuple using a single
        assignment statement. Tuple assignment occurs *simultaneously* rather than
        in sequence, making it useful for swapping values.


Exercises
---------
   

   
