#!/usr/bin/env python
"""
Use dynamic programming (i.e. memoize overlapping sub-problems) to determine
maximum score.

Run it like:

    $ ./party.py < test.json

"""
import argparse
import collections
import functools
import itertools
import json
import sys


class Node(object):

    _id_key = 'name'

    _value_key = 'party-animal-score'

    _parent_key = 'boss'

    _children_key = 'children'

    @classmethod
    def load(cls, io):
        root_id = None
        raw = dict((data[cls._id_key], data) for data in json.load(io))
        for node in raw.itervalues():
            if cls._children_key not in node:
                node[cls._children_key] = []
            if node[cls._parent_key] is None:
                root_id = node[cls._id_key]
            else:
                if cls._children_key not in raw[node[cls._parent_key]]:
                    raw[node[cls._parent_key]][cls._children_key] = []
                raw[node[cls._parent_key]][cls._children_key].append(node[cls._id_key])
        return cls(raw, root_id)

    def __init__(self, tree, id):
        self.id = id
        self._tree = tree
        self._children = None

    @property
    def value(self):
        return self._tree[self.id][self._value_key]

    @property
    def children(self):
        if self._children is None:
            self._children = [
                Node(self._tree, child_id)
                for child_id in self._tree[self.id][self._children_key]
            ]
        return self._children


def memoize(obj):
    """
    http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
    """
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


@memoize
def max_score(node, required=None):

    def _accumulate(seq):
        return reduce(
            lambda x, y: [
                x[0] + y[0],  # score
                x[1] + y[1]   # nodes
                ],
            seq,
            [0,   # score
             []]  # nodes
            )

    if required and node.id in required:
        # node included so exclude children
        return _accumulate(itertools.chain(
            [(node.value, [node])],
            (max_score(cc, required) for c in node.children for cc in c.children)
            ))
    else:
        return max(
            # node included so exclude children
            _accumulate(itertools.chain(
                [(node.value, [node])],
                (max_score(cc, required) for c in node.children for cc in c.children)
                )),

            # node not included so consider children
            _accumulate(max_score(c, required) for c in node.children),

            # take whichever has highest score
            key=lambda x: x[0]
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', default='-', metavar='FILE', nargs='?', help='Input file.')
    parser.add_argument('--required', action='append', metavar='NAME', help='Required to attend.')
    args = parser.parse_args()

    io = sys.stdin if args.file == '-' else open(args.file, 'r')
    root = Node.load(io)
    score, nodes = max_score(root, args.required)

    print score
    for nodes in nodes:
        print nodes.id


if __name__ == '__main__':
    main()
