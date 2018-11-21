#!/usr/bin/env python

from __future__ import print_function

import unittest
from ngram import consume
from ngram import consume3
from ngram import ngram
from ngram import ngram_consume
from ngram import ngram_generator
from ngram import cbow2



class TestNgram(unittest.TestCase):
    text = """We are about to study the idea of a computational process.absComputational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.""".split()

    def test_invalid_n(self):
        with self.assertRaisesRegex(Exception, 'Cannot create negative n-grams.') as context:
            ngram('a b c d e'.split(), 0)


    def test_1gram(self):
        grams = list(ngram(''.split(), 1))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a'.split(), 1))
        self.assertSequenceEqual(grams, [('a',)])

        grams = list(ngram('a b c d e'.split(), 1))
        self.assertSequenceEqual(grams, [('a',), ('b',), ('c',), ('d',), ('e',)])


    def test_2gram(self):
        grams = list(ngram(''.split(), 2))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a'.split(), 2))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a b'.split(), 2))
        self.assertSequenceEqual(grams, [('a', 'b')])

        grams = list(ngram('a b c d e'.split(), 2))
        self.assertSequenceEqual(grams, [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')])


    def test_3gram(self):
        grams = list(ngram(''.split(), 3))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a b'.split(), 3))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a b c'.split(), 3))
        self.assertSequenceEqual(grams, [('a', 'b', 'c')])

        grams = list(ngram('a b c d e'.split(), 3))
        self.assertSequenceEqual(grams, [('a', 'b', 'c'), ('b', 'c', 'd'), ('c', 'd', 'e')])


    def test_4gram(self):
        grams = list(ngram(''.split(), 4))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a b c'.split(), 4))
        self.assertSequenceEqual(grams, [])

        grams = list(ngram('a b c d'.split(), 4))
        self.assertSequenceEqual(grams, [('a', 'b', 'c', 'd')])

        grams = list(ngram('a b c d e'.split(), 4))
        self.assertSequenceEqual(grams, [('a', 'b', 'c', 'd'), ('b', 'c', 'd', 'e')])


    def test_all_yield_same_result(self):
        for a, b, c in zip(ngram(self.text), ngram_consume(self.text), ngram_generator(self.text)):
            self.assertTrue(a == b == c, 'A: {a}\nB: {b}\nC: {c}'.format(a=a, b=b, c=c))



class TestConsume(unittest.TestCase):
    def test_consume(self):
        a = (i for i in range(10))
        self.assertSequenceEqual(list(consume(a, 5)), (5,6,7,8,9))
        self.assertSequenceEqual(list(consume(range(10), 5)), (5,6,7,8,9))


    def test_consume3(self):
        print(consume3(range(10), 5))
        self.assertSequenceEqual(list(consume3(range(10), 5)), (5,6,7,8,9))
        self.assertSequenceEqual(list(consume3(range(10), None)), ())


    def test_comparable(self):
        for a, b in zip(consume(range(10), 5), consume3(range(10), 5)):
            self.assertEqual(a, b)



def timeit_consume():
    import timeit
    number = 30000
    def helper(method_name, number = 30000):
       return (method_name,
          timeit.timeit('for n in {}(text, n=40):\n pass'.format(method_name),
                        setup="from ngram import {}; from __main__ import text".format(method_name),
                        number=number),
          timeit.timeit('[n for n in {}(text, n=40)]'.format(method_name),
                        setup="from ngram import {}; from __main__ import text".format(method_name),
                        number=number))
    results = [helper(m, number) for m in ('consume', 'consume3')]

    from tabulate import tabulate
    #NOTE a = (k,v,u)
    print(tabulate(sorted(results, key=lambda a: a[2]),
       headers=['method', 'for loop', 'list comprehension']))



def timeit_ngram():
   import timeit
   number = 30000
   def helper(method_name, number = 30000):
      return (method_name,
         timeit.timeit('for n in {}(text):\n pass'.format(method_name),
                       setup="from __main__ import {}, text".format(method_name),
                       number=number),
         timeit.timeit('[n for n in {}(text)]'.format(method_name),
                       setup="from __main__ import {}, text".format(method_name),
                       number=number))


   # python -mtimeit  --number=100000 --setup="from cbow import ngram, text" "[n for n in ngram(text)]"
   #results = [helper(m, number) for m in ('ngram', 'ngram_consume', 'cbow', 'cbow_a', 'cbow2', 'cbow_with_ngram')]
   results = [helper(m, number) for m in ('ngram', 'ngram_consume', 'ngram_generator')]

   from tabulate import tabulate
   #NOTE a = (k,v,u)
   print(tabulate(sorted(results, key=lambda a: a[2]),
      headers=['method', 'for loop', 'list comprehension']))



def timeit_cbow():
    import timeit
    number = 30000
    def helper(method_name, number = 30000):
       return (method_name,
          timeit.timeit('for n in {}(text):\n pass'.format(method_name),
                        setup="from ngram import {}; from __main__ import text".format(method_name),
                        number=number),
          timeit.timeit('[n for n in {}(text)]'.format(method_name),
                        setup="from ngram import {}; from __main__ import text".format(method_name),
                        number=number))
    results = [helper(m, number) for m in ('cbow', 'cbow_a', 'cbow2', 'cbow_with_ngram')]

    results.append(('cbow_from_ngram_iterator',
        timeit.timeit('for n in cbow_from_ngram_iterator(ngram(text, n=3)):' ' pass',
            setup="from __main__ import text; from ngram import ngram, cbow_from_ngram_iterator",
            number=number),
        timeit.timeit('[n for n in cbow_from_ngram_iterator(ngram(text, n=3))]',
            setup="from __main__ import text; from ngram import ngram, cbow_from_ngram_iterator",
            number=number)))

    from tabulate import tabulate
    #NOTE a = (k,v,u)
    print(tabulate(sorted(results, key=lambda a: a[2]),
       headers=['method', 'for loop', 'list comprehension']))





text = """We are about to study the idea of a computational process.absComputational processes are abstract beings that inhabit computers.
As they evolve, processes manipulate other abstract things called data.
The evolution of a process is directed by a pattern of rules
called a program. People create programs to direct processes. In effect,
we conjure the spirits of the computer with our spells.""".split()

if __name__ == '__main__':
    #unittest.main()

    #import sys
    #sys.exit()

    for n in ngram(text, 3):
        print(n)

    for n in cbow2(text, 3):
        print(n)

    if False:
        import timeit
        number = 30000
        method_name = 'ngram'
        t = timeit.timeit('for n in {}(text):\n pass'.format(method_name),
                setup="from __main__ import {}, text".format(method_name),
                number=number)
        print(t)

    timeit_consume()
    timeit_ngram()
    timeit_cbow()
