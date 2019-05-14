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

import os.path
import re

import imdb

from . import media_abc
from ..helper import user_input


class Movie(media_abc.Media):
    """Class which represents a single movie."""
    def __init__(self, path: str, info: dict = None, overrides: dict = None) -> None:
        """See super class."""
        super().__init__(path, info, overrides)

        # Ensure we have the required information for IMDB.
        for req in [r for r in ['title'] if r not in self._info]:
            raise ValueError('Error: Filename lacks a {0}.'.format(req))

    def rename(self, dry_run: bool, **kwargs) -> None:
        """See super class."""
        imdb_movie = self._determine_movie(self._info['title'])

        # There weren't any search results
        if imdb_movie is None:
            print('Movie "{0}" not found (no changes made)'.format(self._info['title']))
            return

        movie_title = imdb_movie['title']

        try:
            movie_year = imdb_movie['year']
        except KeyError:
            movie_year = None

        if movie_year is None:
            new_filename = '{0}{1}'.format(movie_title, self.file_extension)
        else:
            new_filename = '{0} ({1}){2}'.format(movie_title, movie_year, self.file_extension)

        if self.filename != new_filename:
            print('"{0}" -> "{1}"'.format(os.path.basename(self._path), new_filename))

            if not dry_run:
                self.filename = new_filename

    def sortable_data(self) -> tuple:
        """See super class."""
        try:
            # Attempt to return 'year' to allow for better sorting.
            return (self._info['title'], self._info['year'])
        except KeyError:
            return self._info['title']

    def _determine_movie(self, title: str) -> imdb.Movie.Movie:
        """Use the IMDB api and information extracted by Guessit to
        determine which movie we are renaming.

        Arguments:
            title: The title of the movie extracted by Guessit.

        Returns:
            The movie we are renaming, as chosen by the user.
        """
        imdb_movies = imdb.IMDb().search_movie(title)

        valid_imdb_movies = [mo for mo in imdb_movies if re.search('movie', mo['kind'])]

        if not valid_imdb_movies:
            return

        print('\nIMDB search results for "{0}"'.format(title))

        for index, mo in enumerate(valid_imdb_movies[:5]):
            try:
                print('{0}: {1} ({2})'.format(index + 1, mo['title'], mo['year']))
            except KeyError:
                print('{0}: {1}'.format(index + 1, mo['title']))

        if len(valid_imdb_movies) == 1:
            print('Automatically choosing only result')
            return valid_imdb_movies[0]

        return valid_imdb_movies[user_input.prompt_input()]

    def __repr__(self):
        title = self._info['title']
        year = self._info['year']

        return 'Movie "{0}" released in {1}'.format(title, year)


media_abc.Media.register(Movie)
