#!/usr/bin/env python
# coding: utf-8

import sys
import os

import argparse


class Infect(object):
    def __init__(self, ns):
        self.ns = ns

    def install(self):  # pragma: nocover
        pass

    def upload(self):  # pragma: nocover
        pass

    def uninstall(self):  # pragma: nocover
        pass

    def symlink(self):  # pragma: nocover
        pass

    def _symlink(self, target, dest):
        """
        Internal helper: Symlink a file and its destination

        Will raise OSErrors if the source is missing or if the destination
        already exists. Check the exception for the `errno` and `filename`
        attributes to determine what went wrong. `errno == 17` means that the
        destination existed and `errno == 2` means that the target was not
        found.

        """

        if not os.path.isfile(target):
            raise OSError(2, 'target file not found', target)
        os.symlink(target, dest)


def setup_args():
    parser = argparse.ArgumentParser('infect')
    subparsers = parser.add_subparsers(help="Core commands", dest="command")

    subparsers.add_parser(
        'symlink',
        help='Symlink configurations for installed applications'
    )
    return parser


def main():  # pragma: nocover
    parser = setup_args()
    parser.parse_args()


if __name__ == "__main__":  # pragma: nocover
    sys.exit(main())
