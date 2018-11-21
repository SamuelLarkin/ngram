#!/usr/bin/env python

from __future__ import print_function

from collections import deque
from itertools import islice
from itertools import izip
from itertools import tee



# CONSUMER
def consume(iterator, n):
    """
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    From: https://docs.python.org/2/library/itertools.html#recipes
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)
    return iterator



def consume3(iterator, n):
    '''Advance the iterator n-steps ahead. If n is none, consume entirely.'''
    deque(islice(iterator, n), maxlen=0)
    return iterator



# NGRAM
def ngram(iterable, n=2):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    assert n > 0, 'Cannot create negative n-grams.'
    l = tee(iterable, n)
    for i, s in enumerate(l):
        for _ in xrange(i):
            next(s, None)
    return izip(*l)



def ngram_consume(iterable, n=2):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    assert n > 0, 'Cannot create negative n-grams.'
    #return izip(*[consume(s, i) for i, s in enumerate(tee(iterable, n))])
    context = [consume(s, i) for i, s in enumerate(tee(iterable, n))]
    return izip(*context)



def ngram_for(words, n=2):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    assert n > 0, "n is not in (0,inf)"
    for i in xrange(len(words)-n+1):
        yield tuple(words[i:i+n])


# CONTINUOUS BAG OF WORDS
def cbow(iterable, window=1):
    "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
    context = [consume(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return izip(izip(*context), target)



def cbow_a(iterable, window=1):
    "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
    context = [consume3(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return izip(izip(*context), target)



def cbow2(iterable, window=2):
   "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
   context = list(tee(iterable, 2*window+1))
   for i, s in enumerate(context):
      for _ in xrange(i):
         next(s, None)
   target = context[window]
   del context[window]
   return izip(izip(*context), target)



def cbow_with_ngram(iterable, window=1):
   "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
   for n in ngram(iterable, 2*window+1):
      n = list(n)
      t = n[window]
      del n[window]
      yield (tuple(n), t)



def cbow_from_ngram_iterator(ngrams):
   "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
   for n in ngrams:
      window = len(n) // 2
      n = list(n)
      t = n[window]
      del n[window]
      yield (tuple(n), t)






def test():
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


   # python -mtimeit  --setup="from cbow import ngram, text" "[n for n in ngram(text)]"
   results = [helper(m, number) for m in ('ngram', 'ngram_consume', 'cbow', 'cbow_a', 'cbow2', 'cbow_with_ngram')]
   results.append(('cbow_from_ngram_iterator',
      timeit.timeit('for n in cbow_from_ngram_iterator(ngram(text)):' ' pass',
          setup="from __main__ import ngram, cbow_from_ngram_iterator",
          number=number),
      timeit.timeit('[n for n in cbow_from_ngram_iterator(ngram(text))]',
          setup="from __main__ import ngram, cbow_from_ngram_iterator",
          number=number)))

   from tabulate import tabulate
   print(tabulate(sorted(results, key=lambda (k,v,u): u),
      headers=['method', 'for loop', 'list comprehension']))



if __name__ == '__main__':
    text = """We are about to study the idea of a computational process.absComputational processes are abstract beings that inhabit computers.
    As they evolve, processes manipulate other abstract things called data.
    The evolution of a process is directed by a pattern of rules
    called a program. People create programs to direct processes. In effect,
    we conjure the spirits of the computer with our spells.""".split()

    for n in ngram(text, 3):
        print(n)

    import timeit
    number = 30000
    method_name = 'ngram'
    t = timeit.timeit('for n in {}(text):\n pass'.format(method_name),
            setup="from __main__ import {}, text".format(method_name),
            number=number)
    print(t)

    test()
