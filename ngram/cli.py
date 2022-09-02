#!/usr/bin/env  python3

import sys

from argparse import ArgumentParser

from .ngram import (
        cbow2,
        consume,
        make_word_iterator,
        ngram,
        )



def _consume_cli(subparsers):
    def function(args):
        for line in args.input:
            print(*list(consume(line.split(), n=args.number)))

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
    def function(args):
        for line in args.input:
            print(*list(ngram(line.split(), n=args.number)))

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
    def function(args):
        for line in args.input:
            print(*list(cbow2(line.split(), window=args.number)))

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
    parser = ArgumentParser(prog='ngram')
    subparsers = parser.add_subparsers(help='sub-command help')
    _consume_cli(subparsers)
    _ngram_cli(subparsers)
    _cbow_cli(subparsers)
    cmd_args = parser.parse_args()
    cmd_args.func(cmd_args)





if __name__ == '__main__':
    _main()
