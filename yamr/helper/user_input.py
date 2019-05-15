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

from typing import Callable, List, TypeVar


T = TypeVar('T')  # Generic type


def prompt_choice(choices: List[T], print_choice: Callable[[int, T], T]) -> T:
    """Prompt the user to choose an item from a list.

    Returns:
        The users choice from the 'choices' list.
    """
    # There weren't any search results
    if not choices:
        return

    current_pos = 0

    while True:
        current_choices = choices[current_pos:current_pos + 5]

        for index, choice in enumerate(current_choices):
            print_choice((index + current_pos) + 1, choice)

        # There was only one search result, automatically choose it
        if len(choices) == 1:
            print('Automatically choosing only result: 1')
            return current_choices[0]

        try:
            user_input = input('\033[KEnter choice: ')
        except KeyboardInterrupt:
            exit(0)

        # Attempt to see if the user input a valid choice
        try:
            return choices[int(user_input) - 1]
        except ValueError:
            pass

        # Check for other valid input, which is *not* a choice
        if user_input == '' and choices[0] == current_choices[0]:
            print('\033[F\033[KEnter choice: 1')
            return current_choices[0]
        elif user_input == 'n' and current_pos <= len(choices) - (5 + 1):
            current_pos += 5
        elif user_input == 'p' and current_pos >= 5:
            current_pos -= 5
        elif user_input == 's':
            return None
        elif user_input == 'q':
            exit(0)

        # Erase the old output choices
        print('\033[F\033[K' * (len(current_choices) + 1), end='')
