#!/usr/bin/python3

import argparse
import itertools
import collections
import random
import sys


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", dest="input", required=True)
    parser.add_argument("--words", dest="words", required=True, type=int)

    return parser.parse_args()


def read_words(input_file):
    for line in input_file.readlines():
        for word in line.split():
            if not word:
                continue
            yield word
        yield "_NEWLINE_"


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def generate_graph(words):
    graph = dict()

    for prev_word, cur_word in pairwise(words):
        vertex = graph.setdefault(prev_word, collections.Counter())
        vertex[cur_word] += 1

    return graph


def markov_random(graph):
    cur_word = random.choice(
            list(key for key in graph.keys() if key[0].isupper()))

    while True:
        possible_words, possible_weights = zip(*graph[cur_word].items())
        cur_word = random.choices(possible_words, possible_weights)[0]
        yield transform_word(cur_word)


def transform_word(word):
    if word == "_NEWLINE_":
        return "\n"
    return word


def main():
    args = parse_args()

    with open(args.input, 'r') as input_file:
        print("[*] reading file", file=sys.stderr)
        words = read_words(input_file)
        print("[*] generating graph", file=sys.stderr)
        graph = generate_graph(words)

    print("[*] here goes the text", file=sys.stderr)

    markov_words = itertools.islice(markov_random(graph), args.words)
    print(' '.join(markov_words))


if __name__ == "__main__":
    main()
