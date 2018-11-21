#!/usr/bin/env python3

from __future__ import print_function

from collections import deque
from itertools import islice
from itertools import tee

try:
    from itertools import izip as zip
except ImportError:
    pass


# CONSUMER
def consume(iterable, n=None):
    """
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    From: https://docs.python.org/2/library/itertools.html#recipes
    Returns: iterator
    """
    iterator = iter(iterable)
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)
    return iterator



def consume3(iterable, n=None):
    '''
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    Returns: iterator
    '''
    iterator = iter(iterable)
    deque(islice(iter(iterator), n), maxlen=0)
    return iterator



# NGRAM
def ngram(iterable, n=2):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    assert n > 0, 'Cannot create negative n-grams.'
    l = tee(iterable, n)
    for i, s in enumerate(l):
        for _ in range(i):
            next(s, None)
    return zip(*l)



def ngram_consume(iterable, n=2):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    assert n > 0, 'Cannot create negative n-grams.'
    #return zip(*[consume(s, i) for i, s in enumerate(tee(iterable, n))])
    context = [consume(s, i) for i, s in enumerate(tee(iterable, n))]
    return zip(*context)



def ngram_generator(words, n=2):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    assert n > 0, "n is not in (0,inf)"
    for i in range(len(words)-n+1):
        yield tuple(words[i:i+n])


# CONTINUOUS BAG OF WORDS
def cbow(iterable, window=1):
    "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
    context = [consume(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return zip(zip(*context), target)



def cbow_a(iterable, window=1):
    "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
    context = [consume3(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return zip(zip(*context), target)



def cbow2(iterable, window=1):
   "s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ..."
   context = list(tee(iterable, 2*window+1))
   for i, s in enumerate(context):
      for _ in range(i):
         next(s, None)
   target = context[window]
   del context[window]
   return zip(zip(*context), target)



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






def make_word_iterator(a):
    """
    Handles been given a string or a file name.
    """
    try:
        with open(a, 'r') as f:
            for l in f:
                yield l
    except:
        yield a



def _consume_cli(subparsers):
    import sys
    def function(args):
        for l in args.input:
            print(*list(consume(l.split(), n=args.number)))

    help ="""
    consumes n words from the input.
    """
    parser = subparsers.add_parser('consume', help=help)
    parser.add_argument('-n',
            '--number',
            dest='number',
            default=0,
            type=int,
            help='number of words to consume [%(defaults)]')
    parser.add_argument('input',
            type=make_word_iterator,
            default=sys.stdin,
            help='Input text to consume')
    parser.set_defaults(func=function)



def _ngram_cli(subparsers):
    import sys
    def function(args):
        for l in args.input:
            print(*list(ngram(l.split(), n=args.number)))

    help ="""
    create ngrams from the input.
    """
    parser = subparsers.add_parser('ngram', help=help)
    parser.add_argument('-n',
            '--number',
            dest='number',
            default=0,
            type=int,
            help='number of words to consume [%(defaults)]')
    parser.add_argument('input',
            type=make_word_iterator,
            default=sys.stdin,
            help='Input text to consume')
    parser.set_defaults(func=function)



def _cbow_cli(subparsers):
    import sys
    def function(args):
        for l in args.input:
            print(*list(cbow2(l.split(), window=args.number)))

    help ="""
    create cbow from the input.
    """
    parser = subparsers.add_parser('cbow', help=help)
    parser.add_argument('-n',
            '--number',
            dest='number',
            default=0,
            type=int,
            help='number of words to consume [%(defaults)]')
    parser.add_argument('input',
            type=make_word_iterator,
            default=sys.stdin,
            help='Input text to consume')
    parser.set_defaults(func=function)



def _main():
    from argparse import ArgumentParser

    parser = ArgumentParser(prog='ngram')
    subparsers = parser.add_subparsers(help='sub-command help')
    _consume_cli(subparsers)
    _ngram_cli(subparsers)
    _cbow_cli(subparsers)
    cmd_args = parser.parse_args()
    cmd_args.func(cmd_args)



if __name__ == '__main__':
    _main()
