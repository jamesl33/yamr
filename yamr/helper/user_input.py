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

import colorama


def prompt_input() -> int:
    """Prompt the user for an integer input.

    Returns:
        An integer representing the users choice.
    """
    while True:
        try:
            user_input = input('Enter choice: ')
        except KeyboardInterrupt:
            print('\nAborted!')
            exit(0)

        if user_input == '':
            print('\033[FEnter choice: {0}'.format(colorama.Fore.LIGHTBLUE_EX + '1' + colorama.Fore.RESET))
            return 0

        try:
            user_input = int(user_input)
            print('\033[FEnter choice: {0}'.format(colorama.Fore.LIGHTBLUE_EX + str(user_input) + colorama.Fore.RESET))
            return user_input - 1
        except ValueError:
            pass  # Failed to parse the users input, ask again
