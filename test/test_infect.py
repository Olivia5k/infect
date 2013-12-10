#!/usr/bin/env python
# coding: utf-8

import tempfile
import shutil
import os
from os import path

from infect.infect import Infect


class TestSymlink(object):
    """
    Test the infect symlinker.

    These tests will actually use the os interface rather than mocking it out.
    This is mainly to make sure that these tests are not 90% mocking code.

    """

    def setup_method(self, method):
        self.infect = Infect()
        self.codes = self.infect.Codes.symlink

        self.tempdir = tempfile.mkdtemp(
            prefix='infect-{0}-'.format(method.__name__)
        )

        # Store [1] to get the name only
        self.target = tempfile.mkstemp(dir=self.tempdir)[1]
        self.dest = path.join(self.tempdir, 'target')

    def teardown_method(self, method):
        # Try to tear down the temporary directory. Don't care if it fails.
        try:
            shutil.rmtree(self.tempdir)
        except OSError:
            pass

    def test_target_not_present(self):
        target = path.join(self.tempdir, 'nope')
        ret = self.infect.symlink(target, self.dest)

        assert ret == self.codes['target_not_found']
        assert not path.islink(self.dest)

    def test_target_present_and_dest_does_not_exist(self):
        ret = self.infect.symlink(self.target, self.dest)

        assert ret == self.codes['success']
        assert path.islink(self.dest)

    def test_target_present_and_dest_is_a_link(self):
        os.symlink(self.target, self.dest)
        ret = self.infect.symlink(self.target, self.dest)

        assert ret == self.codes['destination_already_linked']
        assert path.islink(self.dest)

    def test_target_present_and_dest_is_a_file(self):
        dest = tempfile.mkstemp(dir=self.tempdir)[1]
        ret = self.infect.symlink(self.target, dest)

        assert ret == self.codes['destination_exists']
        assert not path.islink(self.dest)

    def test_target_present_and_dest_is_a_directory(self):
        dest = tempfile.mkdtemp(dir=self.tempdir)
        ret = self.infect.symlink(self.target, dest)

        assert ret == self.codes['destination_exists']
        assert not path.islink(self.dest)
