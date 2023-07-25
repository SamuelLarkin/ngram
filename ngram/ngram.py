#!/usr/bin/env python3

from collections import deque
from itertools import islice
from itertools import tee
from typing import (
        Iterable,
        )



# CONSUMER
def consume(iterable: Iterable, *, n=None):
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



def consume3(iterable: Iterable, *, n=None):
    """
    Advance the iterator n-steps ahead. If n is none, consume entirely.
    Returns: iterator
    """
    iterator = iter(iterable)
    deque(islice(iter(iterator), n), maxlen=0)
    return iterator



# NGRAM
def ngram(iterable: Iterable, *, n=2):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    assert n > 0, "Cannot create negative n-grams."
    l = tee(iterable, n)
    for i, s in enumerate(l):
        for _ in range(i):
            next(s, None)
    return zip(*l)



def ngram_consume(iterable: Iterable, *, n=2):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    assert n > 0, "Cannot create negative n-grams."
    #return zip(*[consume(s, i) for i, s in enumerate(tee(iterable, n))])
    context = [consume(s, i) for i, s in enumerate(tee(iterable, n))]
    return zip(*context)



def ngram_generator(words, *, n=2):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    assert n > 0, "n is not in (0,inf)"
    for i in range(len(words)-n+1):
        yield tuple(words[i:i+n])


# CONTINUOUS BAG OF WORDS
def cbow(iterable: Iterable, *, window: int=1):
    """
    s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ...
    """
    context = [consume(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return zip(zip(*context), target)



def cbow_a(iterable: Iterable, *, window: int=1):
    """
    s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ...
    """
    context = [consume3(s, i) for i, s in enumerate(tee(iterable, 2*window+1))]
    target = context[window]
    del context[window]
    return zip(zip(*context), target)



def cbow2(iterable: Iterable, *, window: int=1):
    """
    s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ...
    """
    context = list(tee(iterable, 2*window+1))
    for i, s in enumerate(context):
        for _ in range(i):
            next(s, None)
    target = context[window]
    del context[window]
    return zip(zip(*context), target)



def cbow_with_ngram(iterable: Iterable, *, window: int=1):
    """
    s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ...
    """
    for n in ngram(iterable, 2*window+1):
        n = list(n)
        t = n[window]
        del n[window]
        yield (tuple(n), t)



def cbow_from_ngram_iterator(ngrams: Iterable):
    """
    s -> ((s0,s2), s1), ((s1,s3), s2), ((s2, s4), s3), ...
    """
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
        with open(a, mode="r", encoding="UTF-8") as fin:
            for line in fin:
                yield line
    except:
        yield a
