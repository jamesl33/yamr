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

import re

import colorama
import imdb

from . import episode
from ..helper import user_input


class TVShow():
    """Class representing an individual TV show.

    Container class which represents a full TV show. The instance will contain
    multiple 'Episode' instances.
    """
    def __init__(self, title: str) -> None:
        """Instantiate the TVShow class.

        Arguments:
            title: The title of the TV show that this instance is representing.
        """
        self._title = title
        self._episodes = []

    def add(self, episode: episode.Episode) -> None:
        """Add a new episode to the TV show.

        Arguments:
            episode: The episode to be added to the TV show.
        """
        self._episodes.append(episode)

    def rename_episodes(self, dry_run: bool) -> None:
        """Rename all the episodes in the TV show.

        Arguments:
            dry_run: Whether or not make any changes.
        """
        imdb_show = self._determine_show(self._title)

        # There weren't any search results
        if imdb_show is None:
            print('TV show "{0}" skipped or not found (no changes made)'.format(self._title))
            return

        imdb.IMDb().update(imdb_show, 'episodes')

        # rename episodes in season/episode sorted order to make visual checks simpler
        for ep in sorted(self._episodes, key=lambda e: e.sortable_data()):
            ep.rename(dry_run, imdb_show=imdb_show)

    def _determine_show(self, title: str) -> imdb.Movie.Movie:
        """Use the IMDB api and information extracted by Guessit to
        determine which TV show we are renaming.

        Arguments:
            title: The title of the TV show extracted by Guessit.

        Returns:
            The show we are renaming, as chosen by the user.
        """
        imdb_shows = imdb.IMDb().search_movie(title)

        valid_imdb_shows = [mo for mo in imdb_shows if re.search('tv series', mo['kind'])]

        if not valid_imdb_shows:
            return

        print('\nIMDB search results for "{0}"'.format(colorama.Fore.LIGHTBLUE_EX + title + colorama.Fore.RESET))

        def _print_show(index: int, show: dict) -> None:
            number = colorama.Fore.LIGHTBLUE_EX + str(index) + '.' + colorama.Fore.RESET

            if show['year'] == '':
                print('{0} {1}'.format(number, show['title']))
            else:
                print('{0} {1} ({2})'.format(number, show['title'], show['year']))

        return user_input.prompt_choice(valid_imdb_shows, _print_show)

    def __len__(self) -> int:
        return len(self._episodes)

    def __repr__(self):
        title = self._title
        episode_count = len(self._episodes)

        return 'TV show "{0}" with {1} episodes'.format(title, episode_count)
