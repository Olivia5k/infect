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


class TestSymlink(object):
    def setup_method(self, method):
        self.infect = infect.Infect(mock.MagicMock())
        self.tempdir = tempfile.mkdtemp(
            prefix='infect-{0}-'.format(method.__name__)
        )
        self.destdir = tempfile.mkdtemp(dir=self.tempdir)
        self.filename = 'foo.conf'
        self.fileroot = os.path.join(self.tempdir, self.filename)
        self.filedest = os.path.join(self.destdir, '.' + self.filename)

        self.infect.conf = {
            'root': self.tempdir,
            'dest': self.destdir,
            'apps': {
                'foo': {
                    'files': [self.filename]
                }
            }
        }

    @mock.patch.object(infect.Infect, '_is_installed')
    @mock.patch.object(infect.Infect, '_symlink')
    def test_app_not_installed(self, sl, ii):
        ii.return_value = False
        self.infect.symlink('foo')

        assert ii.called
        assert not sl.called

    @mock.patch.object(infect.Infect, '_is_installed')
    @mock.patch.object(infect.Infect, '_symlink')
    def test_app_installed(self, sl, ii):
        ii.return_value = True
        self.infect.symlink('foo')

        assert ii.called
        sl.assert_called_once_with(self.fileroot, self.filedest)


class TestIsInstalled(object):
    def setup_method(self, method):
        self.infect = infect.Infect(mock.MagicMock())

    def test_app_does_not_exist(self):
        ret = self.infect._is_installed('this_cannot_possibly_exist')
        assert ret is None

    def test_app_exists(self):
        ret = self.infect._is_installed('yes')
        assert ret == '/usr/bin/yes'

    def test_app_absolute_path(self):
        ret = self.infect._is_installed('/usr/bin/ls')
        assert ret == '/usr/bin/ls'
