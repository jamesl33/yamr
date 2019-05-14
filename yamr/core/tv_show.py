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

import tvdb_api

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
        tvdb_show = self._determine_show(self._title)

        # There weren't any search results
        if tvdb_show is None:
            print('TV show "{0}" not found (no changes made)'.format(self._info['title']))
            return

        # rename episodes in season/episode sorted order to make visual checks simpler
        for ep in sorted(self._episodes, key=lambda e: e.sortable_data()):
            ep.rename(dry_run, tvdb_show=tvdb_show)

    def _determine_show(self, title: str) -> tvdb_api.Show:
        """Use the TVDB api and information extracted by Guessit to
        determine which TV show we are renaming.

        Arguments:
            title: The title of the TV show extracted by Guessit.

        Returns:
            The show we are renaming, as chosen by the user.
        """
        try:
            tvdb_shows = tvdb_api.Tvdb().search(title)
        except tvdb_api.tvdb_shownotfound:
            print('Error: TV show not found')
            exit(1)

        valid_tvdb_shows = [sh for sh in tvdb_shows if sh['seriesName'] != '** 403: Series Not Permitted **']

        if not valid_tvdb_shows:
            return

        print('TVDB search results for "{0}"'.format(title))

        for index, show in enumerate(valid_tvdb_shows[:5]):
            print('{0}: {1}'.format(index + 1, show['seriesName']))

        if len(valid_tvdb_shows) == 1:
            print('Automatically choosing only result')
            return tvdb_api.Tvdb()[valid_tvdb_shows[0]['id']]

        return tvdb_api.Tvdb()[valid_tvdb_shows[user_input.prompt_input()]['id']]

    def __repr__(self):
        title = self._title
        episode_count = len(self._episodes)

        return 'TV show "{0}" with {1} episodes'.format(title, episode_count)
