#!/usr/bin/env python
# coding: utf-8

import sys
import os

# import argparse


class Infect(object):
    def __init__(self):
        pass

    def install(self):  # pragma: nocover
        pass

    def upload(self):  # pragma: nocover
        pass

    def symlink(self, target, dest):
        """
        Symlink a file and its destination

        Will raise OSErrors if the source is missing or if the destination
        already exists. Check the exception for the `errno` and `filename`
        attributes to determine what went wrong. `errno == 17` means that the
        destination existed and `errno == 2` means that the target was not
        found.

        """

        if not os.path.isfile(target):
            raise OSError(2, 'target file not found', target)
        os.symlink(target, dest)

    def uninstall(self):  # pragma: nocover
        pass


def main():  # pragma: nocover
    print('Running infect main()')
    return 0


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
