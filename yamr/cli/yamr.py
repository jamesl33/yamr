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

from typing import List, Tuple, Dict, TypeVar

import colorama
import guessit

from ..core import album
from ..core import episode
from ..core import movie
from ..core import track
from ..core import tv_show


AUDIO_EXTENSIONS = ['.flac', '.mp3', '.ogg']
SUBTITLE_EXTENSIONS = ['.srt']
VIDEO_EXTENSIONS = ['.avi', '.mkv', '.mp4']
FILE_EXTENSIONS = set(AUDIO_EXTENSIONS + SUBTITLE_EXTENSIONS + VIDEO_EXTENSIONS)

T = TypeVar('T')  # Generic type


class YAMR():
    """Class representing the YAMR tool itself."""
    def __init__(self, config: Dict[str, T], overrides: Dict[str, T]) -> None:
        """Instantiate the YAMR class.

        Arguments:
            config: Generic configuration used to manipulate how YAMR behaves.
            overrides: Values which override information extracted by Guessit.
        """
        self._config = config
        self._overrides = overrides

    def rename_media_files(self):
        """Rename all the media files in the given directory."""
        media_files = self._get_media_files(self._config['folder'])
        albums, movies, tv_shows = self._process_media_files(media_files)

        for title in albums:
            albums[title].rename_tracks(self._config['dry_run'])

        for mo in movies:
            mo.rename(self._config['dry_run'])

        for title in tv_shows:
            tv_shows[title].rename_episodes(self._config['dry_run'])

    def _process_media_files(self, files: List[str]) -> Tuple[Dict[str, List[album.Album]], Dict[str, List[tv_show.TVShow]], List[movie.Movie]]:
        """Process a list of media files into Ablum, Movie, TVShow objects.

        Arguments:
            files: List of paths to any supported media files.

        Returns:
            A tuple containing the media files in a format yamr can understand.
        """
        albums, tv_shows = {}, {}
        episodes, movies, tracks = [], [], []

        for file in [f for f in files if os.path.splitext(f)[-1] in AUDIO_EXTENSIONS]:
            tracks.append(track.Track(file, overrides=self._overrides))

        for file in [f for f in files if os.path.splitext(f)[-1] in set(VIDEO_EXTENSIONS + SUBTITLE_EXTENSIONS)]:
            file_info = guessit.guessit(os.path.basename(file))

            if file_info['type'] == 'movie':
                movies.append(movie.Movie(file, file_info, self._overrides))
            elif file_info['type'] == 'episode':
                episodes.append(episode.Episode(file, file_info, self._overrides))

        # Separate the episodes into individual shows
        for ep in episodes:
            show_title = ep._info['title'].lower()

            if show_title not in tv_shows:
                tv_shows[show_title] = tv_show.TVShow(show_title)

            tv_shows[show_title].add(ep)

        # Separate the tracks into individual albums
        for tr in tracks:
            if 'alternative_title' in tr._info:
                album_title = tr._info['alternative_title'].lower()
            elif 'episode_title' in tr._info:
                album_title = tr._info['episode_title'].lower()
            else:
                album_title = tr._info['title'].lower()

            if album_title not in albums:
                albums[album_title] = album.Album(album_title)

            albums[album_title].add(tr)

        album_count = colorama.Fore.LIGHTGREEN_EX + str(len(albums)) + colorama.Fore.RESET
        movie_count = colorama.Fore.LIGHTGREEN_EX + str(len(movies)) + colorama.Fore.RESET
        tv_show_count = colorama.Fore.LIGHTGREEN_EX + str(len(tv_shows)) + colorama.Fore.RESET

        print('Discovered {0} Albums / {1} Movies / {2} TV Shows'.format(album_count, movie_count, tv_show_count))

        return albums, movies, tv_shows

    @classmethod
    def _get_media_files(cls, directory: str) -> List[str]:
        """Search for all the media files in a given directory.

        Arguments:
            directory: The directory to search in.

        Returns:
            The paths to any media files which are supported by yamr.
        """
        media_files = []

        for dirpath, _, filenames in os.walk(directory):
            media_files += [os.path.join(dirpath, f) for f in filenames if os.path.splitext(f)[-1] in FILE_EXTENSIONS]

        return media_files
