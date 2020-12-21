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

import os

from unittest import mock

from yamr.cli import yamr


def test_rename_track(tmp_path):
    (tmp_path / '01 Whenever You Need Somebody.mp3').touch()

    YAMR = yamr.YAMR({'folder': tmp_path, 'dry_run': False}, {})

    with mock.patch('builtins.input', side_effect='1'):
        YAMR.rename_media_files()

    files = [os.path.basename(f) for f in tmp_path.iterdir()]

    assert 'Rick Astley - Whenever You Need Somebody - 01 - Never Gonna Give You Up.mp3' in files


def test_multiple_album_detection(tmp_path):
    (tmp_path / '01 Whenever You Need Somebody.mp3').touch()
    (tmp_path / '01 What a Wonderful World.mp3').touch()

    YAMR = yamr.YAMR({'folder': tmp_path, 'dry_run': False}, {})

    with mock.patch('builtins.input', side_effect=['2', '1']):
        YAMR.rename_media_files()

    files = [os.path.basename(f) for f in tmp_path.iterdir()]

    assert 'Jérôme Noetinger - What a Wonderful World - 01 - Trees of Green.mp3' in files
    assert 'Rick Astley - Whenever You Need Somebody - 01 - Never Gonna Give You Up.mp3' in files
