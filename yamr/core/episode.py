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

import tvdb_api

from . import media_abc


class Episode(media_abc.Media):
    """Class which represents a single episode from a tv show."""
    def __init__(self, path: str, info: dict = None, overrides: dict = None) -> None:
        """See super class."""
        super().__init__(path, info, overrides)

        # Ensure we have the required information for TVDB.
        for req in [r for r in ['title', 'season', 'episode'] if r not in self._info]:
            raise ValueError('Error: Filename lacks a {0}.'.format(req))

        # Ensure the 'episode' key corresponds to a list object
        if not isinstance(self._info['episode'], list):
            self._info['episode'] = [self._info['episode']]

    def rename(self, dry_run: bool, **kwargs) -> None:
        """See super class."""
        tvdb_show = kwargs['tvdb_show']
        series_name = tvdb_show['seriesName']

        try:
            season_num = sorted(tvdb_show)[self._info['season']]
            tvdb_season = tvdb_show[season_num]
            tvdb_episode = tvdb_season[self._info['episode'][0]]
        except (IndexError, tvdb_api.tvdb_episodenotfound):
            se_num = str(self._info['season']).zfill(2)
            ep_num = str(self._info['episode'][0]).zfill(2)
            print('S{0}E{1} not found (no changes made)'.format(se_num, ep_num))
            return

        episode_info = ''

        for index, ep in enumerate(self._info['episode']):
            se_num = str(season_num).zfill(2)
            ep_num = str(ep).zfill(2)
            episode_info += 'S{0}E{1}'.format(se_num, ep_num)

            if index + 1 != len(self._info['episode']):
                episode_info += ' - '

        episode_title = self.clean_string(tvdb_episode['episodeName'], len(self._info['episode']) != 1)

        new_filename = '{0} - {1} - {2}{3}'.format(series_name, episode_info, episode_title, self.file_extension)

        self._rename(new_filename, dry_run)

    def sortable_data(self) -> tuple:
        """See super class."""
        return (self._info['season'], self._info['episode'][0])

    @classmethod
    def clean_string(cls, title: str, multipart: bool = False) -> str:
        """See super class."""
        expressions = [r'\(a.k.a. .*\)']

        if multipart:
            expressions += [r'\(\d\)', r'-pt\d', r'pt\d', r'-prt\d', r'prt\d', r'-part\d', r'part\d']

        for regex in expressions:
            title = re.sub(re.compile(regex), '', title)

        return super().clean_string(title)

    def __repr__(self):
        if len(self._info['episode']) == 1:
            ep_num = '{0}-{1}'.format(self._info['episode'][0], self._info['episode'][-1])
        else:
            ep_num = self._info['episode'][0]

        se_num = self._info['season']
        se_title = self._info['title']

        return 'Episode(s) {0} from season {1} of "{2}"'.format(ep_num, se_num, se_title)


media_abc.Media.register(Episode)
