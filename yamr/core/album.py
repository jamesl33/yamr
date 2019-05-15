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

import sys

from typing import List, Tuple, Dict

import colorama
import musicbrainzngs

from . import track
from ..helper import user_input


class Album():
    """Class representing a music album.

    Container class which represents a complete album. The instance will contain
    multiple 'Track' instances.
    """
    def __init__(self, title: str) -> None:
        """Instantiate the Album class.

        Arguments:
            title: The title of the album that this instance is representing.
        """
        self._title = title
        self._tracks = []

    def add(self, tr: track.Track) -> None:
        """Add a new track to the album.

        Arguments:
            tr: The track that you are adding to the album.
        """
        self._tracks.append(tr)

    def rename_tracks(self, dry_run: bool) -> None:
        """Rename all of the tracks in the album.

        Arguments:
            dry_run: Whether or not make any changes.
        """
        album = self._determine_album(self._title)

        # There weren't any search results
        if album is None:
            print('Album "{0}" skipped or not found (no changes made)'.format(self._title))
            return

        release = musicbrainzngs.get_release_by_id(album['id'], includes='recordings')
        track_list = release['release']['medium-list'][0]['track-list']

        # rename tracks in order to make visual checks simpler
        for tr in sorted(self._tracks, key=lambda t: t.sortable_data()):
            tr.rename(dry_run, album=album, track_list=track_list)

    def _determine_album(self, title: str) -> Dict:
        """Use the MusicBrainz api and information extracted by Guessit to
        determine which album we are renaming.

        Arguments:
            title: The title of the album extracted by Guessit.

        Returns:
            The album we are renaming, as chosen by the user.
        """
        yamr = sys.modules[__name__.split('.')[0]]
        musicbrainzngs.set_useragent(yamr.__title__, yamr.__version__, yamr.__homepage__)

        musicbrainz_albums = musicbrainzngs.search_releases(self._title, limit=100)['release-list']

        known_albums = []
        valid_musicbrainz_albums = []

        for al in musicbrainz_albums:
            al_info = (al['title'].lower(), al['artist-credit-phrase'].lower())

            if 'type' in al['release-group'] and al['release-group']['type'] == 'Album':
                if al_info not in known_albums:
                    valid_musicbrainz_albums.append(al)
                    known_albums.append(al_info)

        if not valid_musicbrainz_albums:
            return

        print('\nMusicBrainz search results for "{0}"'.format(colorama.Fore.LIGHTBLUE_EX + self._title + colorama.Fore.RESET))

        def _print_album(index: int, album: dict) -> None:
            number = colorama.Fore.LIGHTBLUE_EX + str(index) + '.' + colorama.Fore.RESET

            artist_name = album['artist-credit'][0]['artist']['name']
            album_title = album['title']

            try:
                album_release = album['release-event-list'][0]['date']
            except KeyError:
                album_release = None

            if album_release is None:
                print('{0} {1} - {2}'.format(number, artist_name, album_title))
            else:
                print('{0} {1} - {2} ({3})'.format(number, artist_name, album_title, album_release))

        return user_input.prompt_choice(valid_musicbrainz_albums, _print_album)

    def sortable_data(self) -> Tuple[str, int, List[int]]:
        """See super class."""
        return self._info['title'], self._info['episode_title'], self._info['episode']

    def __len__(self) -> int:
        return len(self._tracks)

    def __repr__(self) -> str:
        album_title = self._title
        track_count = len(self._tracks)

        return 'Album "{0}" with {1} tracks'.format(album_title, track_count)
