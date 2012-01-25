# -*- coding:utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Album(object):
    '''
    Represents an album.
    Do not use this class directly.
        
    :param id: internal album id
    :param name: name
    :param artist_id: artist's id to generate an :py:class:`Artist` object
    :param artist_name: artist's name to generate an :py:class:`Artist` object
    :param cover_url: album's cover to generate an :class:`Album` object
    :param connection: underlying :class:`Connection` object
    '''
    def __init__(self, id, name, artist_id, artist_name, cover_url, connection):
        self._connection = connection
        self._id = id
        self._name = name
        self._artist_id = artist_id
        self._artist_name = artist_name
        self._cover_url = cover_url
        self._songs = None
        self._cover = None
        self._artist = None

    def __str__(self):
        return '%s - %s' % (self.name, self.artist.name)
    
    @property
    def id(self):
        '''
        internal album id
        '''
        return self._id
    
    @property
    def name(self):
        '''
        album's name
        '''
        return self._name
    
    @property
    def artist(self):
        '''
        :class:`Artist` object of album's artist
        '''
        if not self._artist:
            self._artist = Artist(self._artist_id, self._artist_name, self._connection)
        return self._artist
    
    @property
    def cover(self):
        '''
        album cover as :class:`Picture` object
        '''
        if self._cover_url:
            if not self._cover:
                self._cover = Picture(self._cover_url)
            return self._cover
    
    @property
    def songs(self):
        '''
        iterator over album's songs as :class:`Song` objects
        '''
        if self._songs is None:
            self._songs = [Song.from_response(song, self._connection) for song in \
                           self._connection.request('albumGetSongs', {'albumID' : self.id, 'isVerified' : False, 'offset' : 0},
                                                    self._connection.header('albumGetSongs'))[1]['songs']]
        return iter(self._songs)
    
from grooveshark.classes.song import Song
from grooveshark.classes.artist import Artist
from grooveshark.classes.picture import Picture