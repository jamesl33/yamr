#!/usr/bin/env python3
"""
This file is part of yamr "Yet Another Media Renamer".

Copyright (C) 2019, James Lee <jamesl33info@gmail.com>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import setuptools

import yamr

setuptools.setup(
    author=yamr.__author__,
    author_email=yamr.__author_email__,
    entry_points={
        'console_scripts': [
            'yamr = yamr.cli.main:run_yamr'
        ],
    },
    install_requires=[
        'colorama',
        'guessit',
        'imdbpy',
        'musicbrainzngs',
    ],
    license=yamr.__license__,
    name=yamr.__name__,
    packages=setuptools.find_packages(),
    version=yamr.__version__
)
