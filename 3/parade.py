#!/usr/bin/env python
"""
"""
import argparse
import re
import sys

import networkx


def load(io):
    pattern_rgx = re.compile(
        '^(?P<node1>[\w\s]+?)\s+'                 # node 1
        'comes\s+(?P<direction>before|after)\s+'  # direction
        '(?P<node2>[\w\s]+)$'                     # node 2
        )
    graph = networkx.DiGraph()
    for i, line in enumerate(io):
        line = line.strip()
        if not line:
            continue
        m = pattern_rgx.match(line)
        if not m:
            raise ValueError('Line #{0} invalid - "{1}"'.format(i, line))
        direction = m.group('direction')
        if direction == 'after':
            src, dst = m.group('node2'), m.group('node1')
        elif direction == 'before':
            src, dst = m.group('node1'), m.group('node2')
        else:
            raise ValueError(
                'Line #{0} has unexpected direction - "{1}"'.format(i, line)
                )
        graph.add_edge(src, dst)
    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', default='-', metavar='FILE', nargs='?', help='Input file.')
    args = parser.parse_args()

    io = sys.stdin if args.file == '-' else open(args.file, 'r')
    graph = load(io)
    if not networkx.is_directed_acyclic_graph(graph):
        print >> sys.stderr, 'Illegal input, cycles detected: '
        for cycle in networkx.simple_cycles(graph):
            print >> sys.stderr, '\t', ', '.join(cycle)
        return 1
    for node in networkx.topological_sort(graph):
        print node
    return 0


if __name__ == '__main__':
    sys.exit(main())
