from distutils.core import setup

setup(
    name='infect',
    version='0.0.1',
    url='https://github.com/thiderman/infect',
    author='Lowe Thiderman, Anton Lazarev',
    author_email='lowe.thiderman@gmail.com, tony@lazarew.me',
    description=('dotfiles distribution management'),
    license='MIT',
    packages=['infect'],
    scripts=[
        'bin/infect'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2',
    ],
)
