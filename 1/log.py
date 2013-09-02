#!/usr/bin/env python
"""
Use a heap to maintain sorted window of events. Oldest event can be consumed
from window heap once it *exceeds* the ripeness threshold.

Run it like:

    $ ./gen.py | ./logs.py

"""
import argparse
import collections
import logging
import re
import sys
import heapq


logger = logging.getLogger(__name__)


PATTERN_RGX = re.compile(
    r'(?P<timestamp>\d+\.\d+)\s+'
    r'City\s+(?P<city>\w+)'
    )


def parse_events(io, strict=False):
    for i, line in enumerate(io):
        line = line.strip()
        m = PATTERN_RGX.match(line)
        if not m:
            if strict:
                raise ValueError('Line #{0} invalid - "{1}"'.format(i, line))
            logger.warning('line #%s invalid - "%s"', i, line)
            continue
        event = {
            'timestamp': float(m.group('timestamp')),
            'city': m.group('city'),
            }
        yield event


DEFAULT_WINDOW_SIZE_SECS = 300


def window_sort_events(events, window_size=DEFAULT_WINDOW_SIZE_SECS):
    max_key = None
    window = []
    for event in events:
        key = event['timestamp']
        max_key = max(key, max_key)
        i = (key, event)
        while window and window[0][0] + window_size < max_key:
            _, event = heapq.heappop(window)
            yield event
    while window:
        _, event = heapq.heappop(window)
        yield event



def model(event, prev_event=None):
    assert not prev_event or prev_event['timestamp'] <= event['timestamp']


def main():
    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument('file', default='-', metavar='FILE', nargs='?', help='Input file.')
    args = parser.parse_args()

    io = sys.stdin if args.file == '-' else open(args.file, 'r')
    prev_event = None
    for event in window_sort_events(parse_events(io)):
        model(event, prev_event)
        prev_event = event


if __name__ == '__main__':
    main()
