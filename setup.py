#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
from glob import glob

setup(
    name="dynmen_scripts",
    version="0.1.0",
    url="https://github.com/frostidaho/dynmen_scripts",

    author="Idaho Frost",
    author_email="frostidaho@gmail.com",

    description="A collection of scripts using dynmen",
    long_description=open('README.rst').read(),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],


    entry_points={
        'console_scripts': [
            'rofi-run = dynmen_scripts.rofi_run:main_run',
            'rofi-window = dynmen_scripts.rofi_run:main_window',
            'dyn-dmenu-run = dynmen_scripts.dmenu_run:main',
            'dyn-tmux-sessions = dynmen_scripts.tmux_sessions:main',
            'xquery = dynmen_scripts.xquery:main',
            'dyn-tmux-test = dynmen_scripts.tmux.__main__:main',
        ],
    },
    install_requires=['dynmen', 'python-xlib'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
