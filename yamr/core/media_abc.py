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

import abc
import os.path
import re
import sys

import colorama
import guessit


LANGUAGE_CODES = ['en']


class Media(metaclass=abc.ABCMeta):
    """Abstract class representing a piece of media supported by yamr.

    Abstract class which outlines the functions that a class must implement to
    be supported by yamr.
    """
    def __init__(self, path: str, info: dict = None, overrides: dict = None) -> None:
        """Instantiate the Media abstract class.

        Arguments:
            path: The path to the media file on disk.
            info: Filename info generated by guessit.
            overrides: Overriding values for the info dictionary.
        """
        self._path = path
        self._info = info

        if info is None:
            self._info = guessit.guessit(self.filename)

        if overrides is not None:
            for key in overrides:
                self._info[key] = overrides[key]

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        if self._path != value:
            os.rename(self._path, value)
            self._path = value

    @property
    def filename(self) -> str:
        return os.path.basename(self._path)

    @filename.setter
    def filename(self, value: str) -> None:
        self.path = os.path.join(os.path.dirname(self.path), value)

    @property
    def file_extension(self) -> str:
        split_filename = self.filename.split('.')

        if split_filename[-2] in LANGUAGE_CODES:
            return '.'.join(['', split_filename[-2], split_filename[-1]])

        return '.'.join(['', split_filename[-1]])

    @abc.abstractmethod
    def rename(self, dry_run: bool, **kwargs) -> None:
        """Use data fetched from an api to rename the media file.

        Arguments:
            dry_run: Whether or not make any changes.
            kwargs: Any additional information needed when renaming the file.
        """
        raise NotImplementedError

    def _rename(self, new_filename: str, dry_run: bool) -> None:
        """Perform the rename at the filesystem level.

        Prettify the rename and display it to the user.

        Arguments:
            new_filename: The filename generated by YAMR.
            dry_run: Whether or not to *actually* perform the rename.
        """
        if self.filename == new_filename:
            original = colorama.Fore.LIGHTGREEN_EX + self.filename + colorama.Fore.RESET

            print('Filename "{0}" is already correct (no changes made)'.format(original))
        elif os.path.exists(new_filename):
            new_filename = colorama.Fore.LIGHTRED_EX + new_filename + colorama.Fore.RESET

            print('Filename "{0}" already exists (no changes made)'.format(new_filename))
        else:
            original = colorama.Fore.LIGHTRED_EX + self.filename + colorama.Fore.RESET
            new = colorama.Fore.LIGHTGREEN_EX + os.path.basename(new_filename) + colorama.Fore.RESET

            print('"{0}" -> "{1}"'.format(original, new))

            if not dry_run:
                self.filename = new_filename

    @abc.abstractmethod
    def sortable_data(self) -> tuple:
        """Get information needed to allow accurate sorting on the media files

        Returns:
            The necessary information to allow accurate sorting.
        """
        raise NotImplementedError

    @classmethod
    def clean_string(cls, string: str) -> str:
        """Remove any characters from a string that will cause issues with
        filesystems.

        Arguments:
            string: The string which will be "cleaned".

        Returns:
            The same string with any "invalid" characters substitiuted.
        """
        if sys.platform.startswith('linux'):
            return re.sub('/', '-', string.strip())
        elif sys.platform.startswith('win32'):
            return re.sub(r'(?u)[^-\w.]', '', string.strip().replace(' ', '_'))
