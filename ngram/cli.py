#!/usr/bin/env  python3

import click
import sys

from .ngram import (
        cbow2,
        consume,
        make_word_iterator,
        ngram,
        )
from typing import (
        Iterable,
        )



@click.group
@click.help_option("-h", "--help")
def cli():
    """
    blah
    """
    pass



@cli.command
@click.option(
    '-n',
    '--number',
    'number',
    default=0,
    type=int,
    help='number of words to consume [%(defaults)]')
@click.argument('words', type=make_word_iterator, default=sys.stdin)
def consume(
        number: int,
        words: Iterable,
        ):
    """
    Consumes n words from the input.
    """
    for line in words:
        print(*list(consume(line.split(), n=number)))



@cli.command
@click.option(
    '-n',
    '--number',
    'number',
    default=0,
    type=int,
    help='number of words to consume [%(defaults)]')
@click.argument('words', type=make_word_iterator, default=sys.stdin)
def ngram(
        number: int,
        words: Iterable,
        ):
    """
    create ngrams from the input.
    """
    for line in words:
        print(*list(ngram(line.split(), n=number)))



@cli.command
@click.option(
    '-n',
    '--number',
    'number',
    default=0,
    type=int,
    help='number of words to consume [%(defaults)]')
@click.argument('words', type=make_word_iterator, default=sys.stdin)
def cbow(
        number: int,
        words: Iterable,
        ):
    """
    create cbow from the input.
    """
    for line in words:
        print(*list(cbow2(line.split(), window=number)))





if __name__ == '__main__':
    cli()
