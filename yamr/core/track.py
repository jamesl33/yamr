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


from .media_abc import Media


class Track(Media):
    """Class which represents a single track from an artists album."""
    def __init__(self, path, info=None, overrides=None):
        """See super class."""
        super().__init__(path, info, overrides)

        # Ensure we have the required information for MusicBrainz, Guessit
        # doesn't officially support music files, however, it will work for
        # this use case; this is why the keys are still "episode" related.
        for req in [r for r in ['title', 'episode'] if r not in self._info]:
            raise ValueError('Error: Filename lacks a {0}.'.format(req))

    def rename(self, dry_run: bool, **kwargs) -> None:
        """See super class."""
        artist_name = kwargs['album']['artist-credit'][0]['artist']['name']
        album_name = kwargs['album']['title']
        track_num = str(self._info['episode']).zfill(2)

        try:
            track_name = kwargs['track_list'][self._info['episode'] - 1]['recording']['title']
        except IndexError:
            print('"{0}" track {1} not found (no changes made)'.format(album_name, track_num))
            return

        new_filename = '{0} - {1} - {2} - {3}{4}'.format(artist_name, album_name, track_num,
                                                         self.clean_string(track_name),
                                                         self.file_extension)

        self._rename(new_filename, dry_run)

    def sortable_data(self):
        """See super class."""
        return self._info['title'], self._info['episode']

    def __repr__(self):
        track_num = self._info['episode']
        track_title = self._info['title']

        return 'Track {0} from album titled "{1}"'.format(track_num, track_title)


Media.register(Track)
