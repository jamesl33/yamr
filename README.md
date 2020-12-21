YAMR - "Yet Another Media Renamer"
----------------------------------
Yet Another Media Renamer is a tool which simplifies the renaming of media files to allow accurate parsing by Plex/Kodi.

Dependencies
------------
- [guessit](https://github.com/guessit-io/guessit)
- [imdbpy](https://github.com/alberanid/imdbpy)
- [python-musicbrainzngs](https://github.com/alastair/python-musicbrainzngs)

Installation
------------
Yet Another Media Renamer can be installed using the 'pip' packaging tool.

```sh
# Clone a local copy of this repository
git clone https://github.com/jamesl33/yamr

# Change directory into the git repository
cd yamr

# Use pip to install 'yamr' locally
pip3 install --user .
```

Usage
-----
A command line user interface for YAMR is provided through the 'yamr' executable.

```sh
# Rename the supported media files in the 'media' directory.
yamr media

# Rename the supported media file in the 'media' directory with overriding values.
yamr "media/Game of Thrones" --overrides='{"title": "Game of Thrones"}'
```

FAQ
---
Q: Why write a new tool when there are existing tools available? <br>
A: Primarily as a learning exercise but I also wanted a tool which supports more media types e.g. episode, track and movie. <br>

License
-------
Copyright (C) 2019 James Lee <jamesl33info@gmail.com>

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
