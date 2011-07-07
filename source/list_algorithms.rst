..  Copyright (C)  Peter Wentworth, Jeffrey Elkner, Allen B. Downey and Chris Meyers.
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3
    or any later version published by the Free Software Foundation;
    with Invariant Sections being Foreword, Preface, and Contributor List, no
    Front-Cover Texts, and no Back-Cover Texts.  A copy of the license is
    included in the section entitled "GNU Free Documentation License".

|

.. index:: list, element, item, sequence, collection    

List Algorithms
===============

This chapter is a bit different from what we've done so far: rather than
introduce more new Python syntax and features, we're going to focus on 
the program development process, and some algorithms that work with lists.
 
.. index:: Test-driven development, scaffolding

Test-driven development (TDD)
-----------------------------

**Test-driven development (TDD)** is a software development practice which
arrives at a desired feature through a series of small, iterative steps
motivated by automated tests which are *written first* that express increasing
refinements of the desired feature.

Unit tests enable us to easily demonstrate TDD. Let's say we want a function
which creates a ``rows`` by ``columns`` matrix given arguments for ``rows`` and
``columns``.

We first setup a skeleton for this function, and add some test cases.  We assume
the test scaffolding from the earlier chapters is also included:

.. sourcecode:: python
    
    def make_matrix(rows, columns):
        """ 
          Create an empty matrix, all elements 0, of rows 
          where each row has columns elements. 
        """
        return []  # dummy return value...
    
    test(make_matrix(3,5), [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

Running this fails, of course::

    >>> 
    Test on line 20 failed. Expected '[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]', but got '[]'.
    >>> 

We could make the test pass by just returning what the test wants.  But a bit of forethought
suggests we need a few more tests first::

    test(make_matrix(4, 2), [[0, 0], [0, 0], [0, 0], [0, 0]])
    test(make_matrix(1, 1), [[0]])
    test(make_matrix(0, 7), [])
    test(make_matrix(7, 0), [[], [], [], [], [], [], []])

Notice how thinking about the test cases *first*, especially those
tough edge condition cases, helps us create a clearer specification
of what we need our function to do.  

This technique is called *test-driven* because --- if we are to believe the extremists
--- code should only be written when there is a failing test to make pass. 
Motivated by the failing tests, we can now produce a more general solution:

.. sourcecode:: python

    def make_matrix(rows, columns):
        """ 
          Create an empty matrix, all elements 0, of rows 
          where each row has columns elements. 
        """
        return [[0] * columns] * rows 

Running this produces the much more agreeable::

    Test on line 20 passed.
    Test on line 21 passed.
    Test on line 22 passed.
    Test on line 23 passed.
    Test on line 24 passed.

We may think we are finished, but when we use the new function later we discover a bug:

.. sourcecode:: python

    >>> m = make_matrix(4, 3)
    >>> m
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    >>> m[1][2] = 7
    >>> m
    [[0, 0, 7], [0, 0, 7], [0, 0, 7], [0, 0, 7]]
    >>>

We wanted to assign the element in the second row and the third column the
value 7, instead, *all* elements in the third column are 7!

Upon reflection, we realize that in our current solution, each row is an
*alias* of the other rows. This is definitely not what we intended, so we set
about fixing the problem, *first by writing a failing test*:

.. sourcecode:: python
    
    m = make_matrix(4, 2)
    m[2][1] = 7
    test(m, [[0, 0], [0, 0], [0, 7], [0, 0]])

When run, we get::

    Test on line 20 passed.
    Test on line 21 passed.
    Test on line 22 passed.
    Test on line 23 passed.
    Test on line 24 passed.
    Test on line 28 failed. Expected '[[0, 0], [0, 0], [0, 7], [0, 0]]', but got '[[0, 7], [0, 7], [0, 7], [0, 7]]'.
 
This last test is not a "one-liner" like most of our other tests have been.  
It illustrates that tests can be arbitrarily complex, and may require some 
setup before we can test what we wish to.  

Software development teams generally have people whose sole job is to 
construct devious and complex test cases for a product.
Being a software tester is certainly not a "secondary" role ranked 
behind programmers, either --- development
managers often report that the brightest and most capable programmers 
often move into testing roles because
they find it very challenging work, and it requires more 
"thinking out of the box" to be able to anticipate
situations in which some code could fail.  

In addition, the test suites that go with a large software product
are regarded as valuable company "assets", just as the code itself is a 
valuable asset. 

With a failing test to fix, we are now driven to a better solution:

.. sourcecode:: python
    
    def make_matrix(rows, columns):
        """ 
          Create an empty matrix, all elements 0, of rows
          where each row has columns elements 
        """
        matrix = []
        for r in range(rows):
            this_row = [0] * columns
            matrix.append(this_row)
        return matrix

Using TDD has several benefits to our software development process.  It:

* helps us think concretely about the problem we are trying solve *before* we
  attempt to solve it.
* encourages breaking down complex problems into smaller, simpler problems and
  working our way toward a solution of the larger problem step-by-step.
* assures that we have a well developed automated test suite for our software,
  facilitating later additions and improvements.


.. admonition::  Beware of using `*` for replicating objects

    The bug we introduced and caught here was really tricky, and required a deep 
    insight into the inner workings of Python. The Python designers gave us 
    us a cute-looking shorthand notation ``xs * 3``, but it was not at all 
    obvious that what we were getting was three alias references, rather than three 
    clones of `xs`. You might prefer to avoid language features that have
    hidden landmines.  
    
    For example, if your boss gave you the working 
    version of `create_matrix` above, and said "instead of initializing each 
    element of the array to 0, make that value a parameter of the function, 
    so that the caller can choose what initial values he wants in the matrix.  
    You leap into action, and deliver this new version, proudly announcing that
    it passes all the tests:

    .. sourcecode:: python
       :linenos:
    
       def make_matrix(rows, columns, val=0):
           """
              Create an empty matrix, all elements val (which defaults to 0),
              of rows where each row has columns elements
           """
           matrix = []
           for r in range(rows):
               this_row = [val] * columns
               matrix.append(this_row)
           return matrix

    But when your boss wants a matrix of dates, he calls your function like this::
    
        dts = make_matrix(3, 4, [1,'Jan',2012])
        
    Oops! It is wrong again, because again the `*` operator on line 7 has created
    aliases again!  Changing one of the months in the matrix of dates 
    changes all the others in the same row! 
    
    We'll see how to solve this in the next chapter.
 

 
Glossary
--------

.. glossary::

    test-driven development (TDD)
        A software development practice which arrives at a desired feature
        through a series of small, iterative steps motivated by automated tests
        which are *written first* that express increasing refinements of the
        desired feature.  (see the Wikipedia article on `Test-driven
        development <http://en.wikipedia.org/wiki/Test_driven_development>`__
        for more information.)

Exercises
---------


#. What is the Python interpreter's response to the following?

   .. sourcecode:: python
    
       >>> list(range(10, 0, -2))

   The three arguments to the *range* function are *start*, *stop*, and *step*, 
   respectively. In this example, ``start`` is greater than ``stop``.  What
   happens if ``start < stop`` and ``step < 0``? Write a rule for the
   relationships among ``start``, ``stop``, and ``step``.
   
#. Consider this fragment of code::

        import turtle
        
        tess = turtle.Turtle()
        alex = tess
        alex.color("hotpink")
   
   Does this fragment create one or two turtle instances?  Does setting
   the colour of ``alex`` also change the colour of ``tess``?  Explain in detail.
   
#. Draw a state snapshot for ``a`` and ``b`` before and after the third line of
   the following python code is executed:

   .. sourcecode:: python
    
       a = [1, 2, 3]
       b = a[:]
       b[0] = 5

#. What will be the output of the following program?

   .. sourcecode:: python
    
       this = ['I', 'am', 'not', 'a', 'crook']
       that = ['I', 'am', 'not', 'a', 'crook']
       print("Test 1: {0}".format(this is that))
       that = this
       print("Test 2: {0}".format(this == that))

   Provide a *detailed* explaination of the results.
     
#. Lists can be used to represent mathematical *vectors*.  In this exercise
   and several that follow you will write functions to perform standard
   operations on vectors.  Create a script named ``vectors.py`` and 
   write Python code to pass the tests in each case.

   Write a function ``add_vectors(u, v)`` that takes two lists of numbers of
   the same length, and returns a new list containing the sums of the
   corresponding elements of each::
   
       test(add_vectors([1, 1], [1, 1]), [2, 2])
       test(add_vectors([1, 2], [1, 4]), [2, 6])
       test(add_vectors([1, 2, 1], [1, 4, 3]), [2, 6, 4])
 
#. Write a function ``scalar_mult(s, v)`` that takes a number, ``s``, and a
   list, ``v`` and returns the `scalar multiple
   <http://en.wikipedia.org/wiki/Scalar_multiple>`__ of ``v`` by ``s``. ::

        test(scalar_mult(5, [1, 2]), [5, 10])
        test(scalar_mult(3, [1, 0, -1]), [3, 0, -3])
        test(scalar_mult(7, [3, 0, 5, 11, 2]), [21, 0, 35, 77, 14])

#. Write a function ``dot_product(u, v)`` that takes two lists of numbers of
   the same length, and returns the sum of the products of the corresponding
   elements of each (the `dot_product
   <http://en.wikipedia.org/wiki/Dot_product>`__).

   .. sourcecode:: python
    
      test(dot_product([1, 1], [1, 1]),  2)
      test(dot_product([1, 2], [1, 4]),  9)
      test(dot_product([1, 2, 1], [1, 4, 3]), 12)
      
#. *Extra challenge for the mathematically inclined*: Write a function
   ``cross_product(u, v)`` that takes two lists of numbers of length 3 and
   returns their
   `cross product <http://en.wikipedia.org/wiki/Cross_product>`__.  You should
   write your own tests and use the test driven development process
   described in the chapter.      

#. Create a new module named ``matrices.py`` and add the following two
   functions introduced in the section on test-driven development:
  
   .. sourcecode:: python
       
        m = [[0, 0], [0, 0]]
        q = add_row(m)
        test(q, [[0, 0], [0, 0], [0, 0]])
        n = [[3, 2, 5], [1, 4, 7]]
        w = add_row(n)
        test(w, [[3, 2, 5], [1, 4, 7], [0, 0, 0]])
        test(n, [[3, 2, 5], [1, 4, 7]])
        n[0][0] = 42
        test(w, [[3, 2, 5], [1, 4, 7], [0, 0, 0]])
    
        m = [[0, 0], [0, 0]]
        q = add_column(m)
        test(q, [[0, 0, 0], [0, 0, 0]])
        n = [[3, 2], [5, 1], [4, 7]]
        w = add_column(n)
        test(w, [[3, 2, 0], [5, 1, 0], [4, 7, 0]])
        test( n, [[3, 2], [5, 1], [4, 7]])


   Your new functions should pass the tests. Note that the last test in
   each case assures that ``add_row`` and ``add_column`` are pure
   functions. ( *hint:* Python has a ``copy`` module with a function named
   ``deepcopy`` that could make your task easier here. We will talk more about
   ``deepcopy`` in chapter 13, but google python copy module if you would like
   to try it now.)
   
#. Write a function ``add_matrices(m1, m2)`` that adds ``m1`` and ``m2`` and
   returns a new matrix containing their sum. You can assume that ``m1`` and
   ``m2`` are the same size. You add two matrices by adding their corresponding 
   values::

     a = [[1, 2], [3, 4]]
     b = [[2, 2], [2, 2]]
     x = add_matrices(a, b)
     test(x, [[3, 4], [5, 6]])
     c = [[8, 2], [3, 4], [5, 7]]
     d = [[3, 2], [9, 2], [10, 12]]
     y = add_matrices(c, d)
     test(y, [[11, 4], [12, 6], [15, 19]])
     test(c, [[8, 2], [3, 4], [5, 7]])
     test(d, [[3, 2], [9, 2], [10, 12]])
          
   The last two tests confirm that ``add_matrices`` is a pure
   function.
   
#. Write a pure function ``scalar_mult(s, m)`` that multiplies a matrix, ``m``, by a 
   scalar, ``s``::

        a = [[1, 2], [3, 4]]
        x = scalar_mult(3, a)
        test(x, [[3, 6], [9, 12]])
        b = [[3, 5, 7], [1, 1, 1], [0, 2, 0], [2, 2, 3]]
        y = scalar_mult(10, b)
        test(y, [[30, 50, 70], [10, 10, 10], [0, 20, 0], [20, 20, 30]])
        test(b, [[3, 5, 7], [1, 1, 1], [0, 2, 0], [2, 2, 3]])

#.  Let's create functions to make these tests pass::

       test(row_times_column([[1, 2], [3, 4]], 0, [[5, 6], [7, 8]], 0), 19)
       test(row_times_column([[1, 2], [3, 4]], 0, [[5, 6], [7, 8]], 1), 22)
       test(row_times_column([[1, 2], [3, 4]], 1, [[5, 6], [7, 8]], 0), 43)
       test(row_times_column([[1, 2], [3, 4]], 1, [[5, 6], [7, 8]], 1), 50)

       test(matrix_mult([[1, 2], [3,  4]], [[5, 6], [7, 8]]), [[19, 22], [43, 50]])
       test(matrix_mult([[1, 2, 3], [4,  5, 6]], [[7, 8], [9, 1], [2, 3]]), 
                     [[31, 19], [85, 55]])
       test(matrix_mult([[7, 8], [9, 1], [2, 3]], [[1, 2, 3], [4, 5, 6]]),
             [[39, 54, 69], [13, 23, 33], [14, 19, 24]])

#. Write functions to pass these tests: 

   .. sourcecode:: python

        test(only_evens([1, 3, 4, 6, 7, 8]), [4, 6, 8])
        test(only_evens([2, 4, 6, 8, 10, 11, 0]), [2, 4, 6, 8, 10, 0])
        test(only_evens([1, 3, 5, 7, 9, 11]), [])
        test(only_evens([4, 0, -1, 2, 6, 7, -4]), [4, 0, 2, 6, -4])
        nums = [1, 2, 3, 4]
        test(only_evens(nums), [2, 4])
        test(nums, [1, 2, 3, 4])

        test(only_odds([1, 3, 4, 6, 7, 8]), [1, 3, 7])
        test(only_odds([2, 4, 6, 8, 10, 11, 0]), [11])
        test(only_odds([1, 3, 5, 7, 9, 11]), [1, 3, 5, 7, 9, 11])
        test(only_odds([4, 0, -1, 2, 6, 7, -4]), [-1, 7])
        nums = [1, 2, 3, 4]
        test(only_odds(nums), [1, 3])
        test(nums, [1, 2, 3, 4])
   
#. Add a function ``multiples_of(num, numlist)`` to ``numberlists.py`` that
   takes an integer (``num``), and a list of integers (``numlist``) as
   arguments and returns a list of those integers in ``numlist`` that are
   multiples of ``num``.  Add your own tests and use TDD to develope this
   function.             
             
             
             
#. Describe the relationship between ``' '.join(song.split())`` and
   ``song`` in the fragment of code below. 
   Are they the same for all strings assigned to ``song``? 
   When would they be different? ::
   
        song = "The rain in Spain..."
   
#. Write a function ``replace(s, old, new)`` that replaces all occurences of
   ``old`` with ``new`` in a string ``s``::

      test(replace('Mississippi', 'i', 'I'), 'MIssIssIppI')
      
      s = 'I love spom!  Spom is my favorite food.  Spom, spom, spom, yum!'
      test(replace(s, 'om', 'am'),
             'I love spam!  Spam is my favorite food.  Spam, spam, spam, yum!')
    
      test(replace(s, 'o', 'a'),
             'I lave spam!  Spam is my favarite faad.  Spam, spam, spam, yum!')

   *Hint*: use the ``split`` and ``join`` methods.
   
   
#. Every week a computer scientist buys four lotto tickets. He always choses the 
   same prime numbers, with the hope that he ever hits the jackpot, others
   will suddenly get interested in prime numbers.  He represents his weekly tickets
   in Python as a list of lists::

        my_tickets = [ [ 7, 17, 37, 19, 23, 43], 
                       [ 7,  2, 13, 41, 31, 43], 
                       [ 2,  5,  7, 11, 13, 17], 
                       [13, 17, 37, 19, 23, 43] ]
                       
   Complete these exercises.
    
   a. Each lotto draw takes six random balls, numbered from 1 to 49.  Write
      a function to return a lotto draw.
   b. Write a function that returns compares a single ticket and a draw, and returns
      the number of correct picks on that ticket::
      
        test(lotto_match([42, 4, 7, 11, 1, 13], [2, 5, 7, 11, 13, 17]), 3)
         
   c. Write a function that takes a list of tickets and a draw, and returns a list 
      telling how many picks were correct on each ticket::
      
        test(lotto_matches([42, 4, 7, 11, 1, 13], my_tickets), [1, 2, 3, 1])
      
   d. Write a function that takes a list of integers, and returns the number of primes in the list::
   
        test(primes_in([42, 4, 7, 11, 1, 13]), 3)
   
   e. Write a function to discover whether the computer scientist has missed any
      prime numbers in his selection of the four tickets.  Return a list of all primes that he has missed::
      
         test(prime_misses(my_tickets), [3, 29, 47])
         
   f. Write a function that repeatedly makes a new draw, and compares the draw to the four tickets.
   
      i. Count how many draws are needed until one of the computer scientist's tickets has at least 
         3 correct picks.
         Try the experiment twenty times, and average out the number of draws needed.
       
      ii. How many draws are needed, on average, before he gets at least 4 picks correct?  
              
      iii. How many draws are needed, on average, before he gets at least 5 correct?  (Hint: this
           might take a while.  It would be nice if you could print some dots, like a progress bar,
           to show when each of the 20 experiments has completed.)

      Notice that we have difficulty constructing test cases here, because our random numbers
      are not deterministic. Automated testing only really works if you already know what 
      the answer should be! 
