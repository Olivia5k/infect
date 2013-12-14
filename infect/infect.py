#!/usr/bin/env python
# coding: utf-8

import sys
import os

import argparse


class Infect(object):
    def __init__(self, ns):
        self.ns = ns
        self.conf = {}
        self._skipped = []

    def install(self):  # pragma: nocover
        pass

    def upload(self):  # pragma: nocover
        pass

    def uninstall(self):  # pragma: nocover
        pass

    def symlink(self, *apps):
        for app in apps:
            # TODO thiderman: Allow argument like --all that overrides
            if not self._is_installed(app):
                self._skipped.append(app)
                continue

            appconf = self.conf['apps'][app]
            for f in appconf['files']:
                src = os.path.join(self.conf['root'], f)

                # If the application has a dest set, use that, otherwise just
                # use the root infect dest.
                if 'dest' in appconf and f in appconf['dest']:
                    dest = appconf['dest'][f]
                    dest = os.path.expandvars(dest)  # Support env variables
                else:
                    dest = os.path.join(self.conf['dest'], '.{0}'.format(f))

                try:
                    self._symlink(src, dest)
                except OSError as exc:
                    if exc.errno != 17:
                        # Some other OSError, because of reasons. Re-raise!
                        raise  # pragma: nocover

                    # Check if the destination file is already a link. If
                    # not, back it up and re-run the symlinker.
                    if not os.path.islink(dest):
                        self._backup(dest)
                        self._symlink(src, dest)

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

    def _is_installed(self, program):
        """
        http://stackoverflow.com/questions/377017/

        """

        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    def _backup(self, target):  # pragma: nocover
        pass


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
