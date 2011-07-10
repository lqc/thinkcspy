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

As in all parts of this book, our expectation is that you, the reader, will
copy our code into your Python environment, play and experiment, and work along with us. 
 
.. index:: Test-driven development, scaffolding

Test-driven development
-----------------------

Early in our `Fruitful functions` chapter we introduced the idea of
*incremental development*, where we added small fragments of
code to slowly build up the whole, so that we could easily find 
problems early. Later in that same chapter we introduced `unit testing` 
and gave code for our testing framework so that we could capture, in code, 
appropriate tests for the functions we were writing. 
 
**Test-driven development (TDD)** is a software development practice which
takes these practices one step further.  The key idea is that automated 
tests should be written *first*.  This technique is called *test-driven* 
because --- if we are to believe the extremists --- non-testing code should 
only be written when there is a failing test to make pass. 
 
We can still retain our mode of working in small incremental steps, but 
now we'll define and express those steps in terms of a sequence of increasingly
sophisticated unit tests that demand more from our code at each stage.

We'll turn our attention to some standard algorithms that process lists now, but
as we proceed through this chapter we'll attempt to do so in the spirit envisaged
by TDD.

The linear search algorithm
---------------------------

We'd like to know the index where a specific item occurs within in a list of items.  
Specifically, we'll return the index of the item if it is found, or we'll return
-1 if the item doesn't occur in the list.  Let us start with some tests:

.. sourcecode:: python

    friends = ["Joe", "Amy", "Brad", "Angelina", "Zuki", "Thandi", "Paris"]
    test(search_linear(friends, 'Amy'), 1)
    test(search_linear(friends, 'Joe'), 0)
    test(search_linear(friends, 'Paris'), 7)
    test(search_linear(friends, 'Bill'), -1)

Motivated by the fact that our tests don't even run, let alone pass, we now write
the function:
 
.. sourcecode:: python 

    def search_linear(xs, key):
        ''' Find and return the index of key in sequence xs '''
        for (i, v) in enumerate(xs):
           if v == key:
               return i
        return -1
      
There are a some points to learn here: We've seen a similar algorithm in section 8.10 when
we searched for a character in a string.  There we used a ``while`` loop, here we've used a 
``for`` loop, coupled with ``enumerate`` to extract the ``(i, v)`` pair on each iteration.
There are other variants --- for example, we could have used ``range`` and made the loop 
run only over the indexes, or we could have used the idiom of returning ``None`` when the 
item was not found in the list.  But the essential similarity in all these variations is 
that we test every item in the list in turn, from first to last, using the pattern of 
the `eureka traversal` that we introduced in section 8.10 --- that we return from the 
function as soon as we find what we're looking for.

Searching all items of a sequence from first to last is called a **linear search**.  
Each time we check whether ``v == key`` we'll call it a **probe**.  We like to count 
probes as a measure of how efficient our algorithm is, and this will be a good enough 
indication of how long our algorithm will take to execute. 

Linear searching is characterized by the fact that the nunmber of probes needed to find an
item depends directly on the length of the list. So if the list becomes ten times bigger,
we can expect to wait ten times longer when searching for things. 
Notice too, that if we're searching for something
that is not present in the list, we'll have to go all the way to the end before we can return
the negative value. So this case needs N probes, if N is the length of the list. However, if we're 
searching for something that is in the list, we could be lucky
and find it immediately in position 0, or we might have to look further, perhaps even all 
the way to the last item. On average, when the item we seek is present, we're going to need 
to go about halfway through the list, or N/2 probes.

We say that this search has **linear performance** (linear meaning `straight line`) because,
if we were to measure the search times for different sizes of lists (N), and then plot a graph
of time-to-search against N, we'd get a more-or-less straight line graph.

Analysis like this is pretty meaningless for small lists --- the computer is quick enough
not to bother if the list only has a handful of items. So generally, we're interested in
the **scalability** of our algorithms --- how do they perform if we throw bigger problems at
them.  Would this search be a sensible one to use if we had a million or ten million 
items (perhaps the catalog of books in your local library) in our list. What happens
for really large datasets, e.g. how does Google search so brilliantly well? 

A more realistic problem
------------------------

As children learn to read, there are expectations that their vocabulary will grow.  So a
child of age 14 is expected to know more words than a child of age 8. When prescribing
reading books for a grade, an important question might be *"which words in this book
are not in the expected vocabulary at this level?"*  

Let us assume we can read a vocabulary of words into our program, and read the text
of a book, and split it into words.  Let us write some tests for what we need to do
next.  Test data can usually be very small, even if we intend to finally use our 
program for larger cases: 

.. sourcecode:: python

    vocab = ['apple', 'boy', 'dog', 'down', 'fell', 'girl', 'grass', 'the', 'tree']
    book_words = 'the apple fell from the tree to the grass'.split()
    test(find_unknown_words(vocab, book_words), ['from', 'to'])
    test(find_unknown_words([], book_words), book_words)
    test(find_unknown_words(vocab, ['the', 'boy', 'fell']), [])
    
Notice we were a bit lazy, and used ``split`` to create our list of words ---
it is easier than typing out the list, and very convenient if you want to input a
sentence into the program and check its words.

We now need to implement the function for which we've written tests, and we'll make 
use of our linear search.  The basic strategy is to run through each of the words in
the book, look it up in the vocabulary, and if it is not in the vocabulary, save it
into a new resulting list which we return from the function:

.. sourcecode:: python

    def find_unknown_words(vocab, wds):
        """ Return a list of words in wds that do not occur in vocab """
        result = []
        for w in wds:
            if (search_linear(vocab, w) < 0):
                result.append(w)
        return result
                     
We can happily report now that the tests all pass.

Now let us look at the scalability.  We have more realistic vocabulary in a text file,
so let us read in the file (as a single string) and split it into a list of words. For
convenience, we'll create a function to do this for us, and test it on a file we happen
to have available:

.. sourcecode:: python

    def load_words_from_file(filename):
        """ Read a file of words from filename, and return the words in a list """
        f = open(filename, 'r')
        file_content = f.read()
        f.close()
        wds = file_content.split()
        return wds

    bigger_vocab = load_words_from("vocab.txt")
    print("There are {0} words in the vocab, starting with\n {1} "
                  .format(len(bigger_vocab), bigger_vocab[:6]))

Python responds with:: 

     There are 19469 words in the vocab, starting with 
     ['a', 'aback', 'abacus', 'abandon', 'abandoned', 'abandonment'] 

So we've got a sensible size vocabulary. Now let us load up a book.
Loading a book is much like loading words from a file, but we're going
to do a little extra black magic.  Books are full of punctuation, and have
mixtures of lowercase and uppercase letters.  We need to clean up the contents
of the book.  This will involve removing punctuation, and converting everything
to the same case (lowercase, because our vocabulary is all in lowercase).  So
we'll want a more sophisticated way of converting text to words.

.. sourcecode:: python 

    test(text_to_words("My name is Earl!"), ['my', 'name', 'is', 'earl'])
    test(text_to_words('"Well, I never!", said Alice.'), ['well', 'i', 'never', 'said', 'alice'])

There is a powerful ``translate`` method available for strings.  The idea is that one sets up
a table of substitutions --- for every ascii character, you can give a corresponding substitution.
The ``translate`` method will apply these substitions throughout the whole string.  So here we go: 

.. sourcecode:: python

     import string 
     
     def text_to_words(the_text):
        """ return a list of words with all punctuation removed, and all in lowercase """
        my_substitutions = string.maketrans(
          b'ABCDEFGHIJKLMNOPQRSTUVWXYZ,.!?"-*+/>()0123456789[]:;\'', # if you find this
          b'abcdefghijklmnopqrstuvwxyz                           ')  # replace it by this

        # Translate the text according to our translation table.
        cleaned_text = the_text.translate(my_substitutions)
        wds = cleaned_text.split()
        return wds
  
The translations take all punctuation, and turn it into spaces. Then, of course, ``split``
will get rid of the spaces as it breaks the text into a list of words.  The tests pass.

Now we're ready to read in our book:

.. sourcecode:: python

    def get_words_in_book(filename):
        """ Read a book from filename, and return a list of its words. """
        f = open(filename, 'r')
        content = f.read()
        f.close()
        wds = text_to_words(content)
        return wds

    book_words = get_words_in_book("AliceInWonderland.txt")
    print("There are {0} words in the book, starting with \n{1} ".
               format(len(book_words), book_words[:100]))

Python prints the following (all on one line, we've cheated a bit for the textbook)::

    There are 27336 words in the book, starting with 
    ['alice', 's', 'adventures', 'in', 'wonderland', 'lewis', 'carroll', 
        'chapter', 'i', 'down', 'the', 'rabbit', 'hole', 'alice', 'was', 
        'beginning', 'to', 'get', 'very', 'tired', 'of', 'sitting', 'by', 
        'her', 'sister', 'on', 'the', 'bank', 'and', 'of', 'having', 'nothing', 
        'to', 'do', 'once', 'or', 'twice', 'she', 'had', 'peeped', 'into', 'the', 
        'book', 'her', 'sister', 'was', 'reading', 'but', 'it', 'had', 'no', 'pictures', 
        'or', 'conversations', 'in', 'it', 'and', 'what', 'is', 'the', 'use', 'of', 
        'a', 'book', 'thought', 'alice', 'without', 'pictures', 'or', 'conversation', 
        'so', 'she', 'was', 'considering', 'in', 'her', 'own', 'mind', 'as', 'well', 
        'as', 'she', 'could', 'for', 'the', 'hot', 'day', 'made', 'her', 'feel', 
        'very', 'sleepy', 'and', 'stupid', 'whether', 'the', 'pleasure', 'of', 
        'making', 'a']  
        
 
Well now we have all the pieces ready.  Let us see what words in this book are not in
the vocabulary: 

.. sourcecode:: python

    >>> missing_words = find_unknown_words(bigger_vocab, book_words) 
 
We wait a considerable time now, something like a minute, before Python finally
works its way through this, and prints a list of 3398 words in the book that are
not in the vocabulary.  mmm.  This is not particularly scaleable.  For a vocabularly
that is twenty times larger (you'll often find school dictionaries with 300 000 words,
for example), and longer books, this is not going to work.  So let us make some timing
measurements, and think about how to improve this in the next section.

.. sourcecode:: python

   import time
   
   t0 = time.clock()
   missing_words = find_unknown_words(bigger_vocab, book_words) 
   t1 = time.clock()
   print("There are {0} unknown words.".format(len(missing_words)))
   print("That took {0:.4f} seconds.".format(t1-t0))

We get the results and some timing that we can refer back to later:

.. sourcecode:: python
 
    There are 3398 unknown words.
    That took 49.8014 seconds. 
 
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
        
    linear search 
        A search that probes each item in a list or sequence, from first, until it finds
        what it is looking for.  It is used for unordered lists of items.
        
    probe
        Each time we take a look when searching for an item is called a probe.  In our
        chapter on `Iteration` we also played a guessing game where the computer tried
        to guess the user's secret number. Each of those tries would also be called a probe.
         
    

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
