#!/usr/bin/env python
# coding: utf-8

import os
import tempfile
import shutil
import pytest
import mock

from infect import infect


class TestSymlinkInternal(object):
    """
    Test the internal infect symlinker.

    These tests will actually use the os interface rather than mocking it out.
    This is mainly to make sure that these tests are not 90% mocking code.

    """

    def setup_method(self, method):
        self.infect = infect.Infect(mock.MagicMock())
        self.tempdir = tempfile.mkdtemp(
            prefix='infect-{0}-'.format(method.__name__)
        )

        # Store [1] to get the name only
        self.target = tempfile.mkstemp(dir=self.tempdir)[1]
        self.dest = os.path.join(self.tempdir, 'target')

    def teardown_method(self, method):
        # Try to tear down the temporary directory. Don't care if it fails.
        try:
            shutil.rmtree(self.tempdir)
        except OSError:
            pass

    def test_target_not_present(self):
        target = os.path.join(self.tempdir, 'nope')
        with pytest.raises(OSError) as exc:
            self.infect._symlink(target, self.dest)

        assert exc.value.errno == 2
        assert exc.value.filename == target
        assert not os.path.islink(self.dest)

    def test_target_present_and_dest_does_not_exist(self):
        self.infect._symlink(self.target, self.dest)

        assert os.path.islink(self.dest)

    def test_target_present_and_dest_is_a_link(self):
        os.symlink(self.target, self.dest)
        with pytest.raises(OSError) as exc:
            self.infect._symlink(self.target, self.dest)

        assert exc.value.errno == 17
        assert exc.value.filename == self.dest
        assert os.path.islink(self.dest)

    def test_target_present_and_dest_is_a_file(self):
        dest = tempfile.mkstemp(dir=self.tempdir)[1]
        with pytest.raises(OSError) as exc:
            self.infect._symlink(self.target, dest)

        assert exc.value.errno == 17
        assert exc.value.filename == dest
        assert not os.path.islink(self.dest)

    def test_target_present_and_dest_is_a_directory(self):
        dest = tempfile.mkdtemp(dir=self.tempdir)
        with pytest.raises(OSError) as exc:
            self.infect._symlink(self.target, dest)

        assert exc.value.errno == 17
        assert exc.value.filename == dest
        assert not os.path.islink(self.dest)


class TestSymlinkArguments(object):
    def setup_method(self, method):
        self.parser = infect.setup_args()

    def test_symlink_present(self):
        ns = self.parser.parse_args(['symlink'])
        assert ns.command == 'symlink'
