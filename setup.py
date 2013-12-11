import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['test', '--cov=infect']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='infect',
    version='0.0.1',
    url='https://github.com/thiderman/infect',
    author='Lowe Thiderman, Anton Lazarev',
    author_email='lowe.thiderman@gmail.com, tony@lazarew.me',
    description=('dotfiles distribution management'),
    license='MIT',
    packages=['infect'],
    entry_points={
        'console_scripts': [
            'infect = infect.infect:main',
        ],
    },
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
)
