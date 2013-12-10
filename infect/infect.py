#!/usr/bin/env python
# coding: utf-8

import sys
import os

# import argparse


class Infect(object):
    class Codes:
        symlink = {
            'success': 0,
            'target_not_found': 1,
            'destination_already_linked': 2,
            'destination_exists': 3,
        }

    def __init__(self):
        pass

    def install(self):
        pass

    def upload(self):
        pass

    def symlink(self, target, dest):
        """
        Symlink a file and its destination

        Will return a return code from `Infect.Codes.symlink`.

        """

        if not os.path.isfile(target):
            return self.Codes.symlink['target_not_found']

        if os.path.islink(dest):
            return self.Codes.symlink['destination_already_linked']

        if os.path.isfile(dest) or os.path.isdir(dest):
            return self.Codes.symlink['destination_exists']

        os.symlink(target, dest)

        return self.Codes.symlink['success']

    def uninstall(self):
        pass


def main():
    print('Running infect main()')
    return 0


if __name__ == "__main__":
    sys.exit(main())
