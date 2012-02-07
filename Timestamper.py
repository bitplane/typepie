#!/usr/bin/python
"""Timestamper (c) Gaz Davidson February 2012.

    This module provides a queue that wraps around another queue,
    timestamping each item as it is added.

    When executed from the command line, it will timestamp each 
    line from stdin producing a CSV file.
"""

class Timestamper(object):
    """A queue which timestamps other queues."""
    def __init__(self, source):
        """ constructor """
        self.queue = source

def main():
    # todo: parse command line, get data from stdin until exit

if __name__ == '__main__':
    main()
