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

import argparse
import json
import sys

from .yamr import YAMR


def run_yamr() -> None:
    """Run the command line user interface for yamr."""
    parser = argparse.ArgumentParser(
        description='yamr "Yet Another Media Renamer"',
        prog='yamr'
    )

    parser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        default=False,
        help='Do not perform any action, just show what would be done'
    )

    parser.add_argument(
        '-o',
        '--overrides',
        action='store',
        default='{}',
        help='Override the information parsed by Guessit',
        type=str
    )

    parser.add_argument(
        '-v',
        '--version',
        action='store_true',
        help="Display version information then exit"
    )

    parser.add_argument(
        'folder',
        action='store',
        help='Target folder, should contain some media files',
        nargs='?',
        type=str
    )

    arguments = parser.parse_args()

    config = {
        'dry_run': arguments.dry_run,
        'folder': arguments.folder
    }

    overrides = json.loads(arguments.overrides)

    if arguments.version:
        yamr = sys.modules[__name__.split('.')[0]]
        print('{0} {1}'.format(yamr.__title__, yamr.__version__))
        exit(0)

    if config['folder'] is None:
        parser.print_help()
        exit(0)

    yamr = YAMR(config, overrides)
    yamr.rename_media_files()
