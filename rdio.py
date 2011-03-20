#!/usr/bin/python
#
# The MIT License
# 
# Copyright 2011 Benjamin Kreeger
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""A library that provides a Python interface to Rdio's API."""

__author__ = 'benjaminkreeger@gmail.com'
__version__ = '0.1'

import ast
import cgi
import inspect
import oauth2 as oauth
import urllib

root_url = 'http://api.rdio.com/1/'
oauth_token_url = 'http://api.rdio.com/oauth/request_token'
root_site_url = 'http://www.rdio.com'
http_method = 'POST'
methods = {
    'add_friend': 'addFriend',
    'add_to_collection': 'addToCollection',
    'add_to_playlist': 'addToPlaylist',
    'create_playlist': 'createPlaylist',
    'current_user': 'currentUser',
    'delete_playlist': 'deletePlaylist',
    'find_user': 'findUser',
    'get': 'get',
    'get_activity_stream': 'getActivityStream',
    'get_albums_for_artist': 'getAlbumsForArtist',
    'get_albums_for_artist_in_collection': 'getAlbumsForArtistInCollection',
    'get_albums_in_collection': 'getAlbumsInCollection',
    'get_artists_in_collection': 'getArtistsInCollection',
    'get_heavy_rotation': 'getHeavyRotation',
    'get_new_releases': 'getNewReleases',
    'get_object_from_short_code': 'getObjectFromShortCode',
    'get_object_from_url': 'getObjectFromUrl',
    'get_playback_token': 'getPlaybackToken',
    'get_playlists': 'getPlaylists',
    'get_top_charts': 'getTopCharts',
    'get_tracks_for_album_in_collection': 'getTracksForAlbumInCollection',
    'get_tracks_for_artist': 'getTracksForArtist',
    'get_tracks_for_artist_in_collection': 'getTracksForArtistInCollection',
    'get_tracks_in_collection': 'getTracksInCollection',
    'remove_friend': 'removeFriend',
    'remove_from_collection': 'removeFromCollection',
    'remove_from_playlist': 'removeFromPlaylist',
    'search': 'search',
    'search_suggestions': 'searchSuggestions',
}

class RdioObject(object):
    """Describes common fields a base Rdio object will have."""
    
    def __init__(self, data=None):
        self._data = data
        self.key = data['key']
        self.url = data['url']
        self.icon = data['icon']
        self.base_icon = data['baseIcon']
        self.rdio_type = None
        if data['type'] == 'r':
            self.rdio_type = 'Artist'
        elif data['type'] == 'a':
            self.rdio_type = 'Album'
        elif data['type'] == 't':
            self.rdio_type = 'Track'
        elif data['type'] == 'p':
            self.rdio_type = 'Playlist'
        elif data['type'] == 's':
            self.rdio_type = 'User'

class Artist(RdioObject):
    """Describes an Rdio artist."""
    
    def __init__(self, data=None):
        if data:
            super(Artist, self).__init__(data)
            self.name = data['name']
            self.track_count = data['length']
            self.has_radio = data['hasRadio']
            self.short_url = data['shortUrl']
            self.album_count = None
            if data['albumCount']:
                self.album_count = data['albumCount']

class MusicObject(RdioObject):
    """Describes an Rdio music object."""
    
    def __init__(self, data=None):
        if data:
            super(MusicObject, self).__init__(data)
            self.name = data['name']
            self.artist_name = data['artist']
            self.artist_url = data['artistUrl']
            self.artist_key = data['artistKey']
            self.is_explicit = data['isExplicit']
            self.is_clean = data['isClean']
            self.price = data['price']
            self.can_stream = data['canStream']
            self.can_sample = data['canSample']
            self.can_tether = data['canTether']
            self.short_url = data['shortUrl']
            self.embed_url = data['embedUrl']
            self.duration = data['duration']

class Album(MusicObject):
    """Describes an Rdio album."""
    
    def __init__(self, data=None):
        if data:
            super(Album, self).__init__(data)
            self.track_keys = data['trackKeys']
            self.release_date = data['displayDate']
            self.release_date_iso = None
            if data['releaseDateISO']:
                self.release_date_iso = data['releaseDateISO']

class Track(MusicObject):
    """Describes an Rdio track."""
    
    def __init__(self, data=None):
        if data:
            super(Track, self).__init__(data)
            self.album_artist_name = data['albumArtist']
            self.album_artist_key = data['albumArtistKey']
            self.can_download = data['canDownload']
            self.can_download_album_only = data['canDownloadAlbumOnly']
            self.play_count = None
            if data['playCount']:
                self.play_count = data['playCount']

class Playlist(RdioObject):
    """Describes an Rdio playlist."""
    
    def __init__(self, data=None):
        if data:
            super(Playlist, self).__init__(data)
            self.name = data['name']
            self.track_count = data['length']
            self.owner_name = data['owner']
            self.owner_url = data['ownerUrl']
            self.owner_key = data['ownerKey']
            self.owner_icon = data['ownerIcon']
            self.last_updated = data['lastUpdated']
            self.short_url = data['shortUrl']
            self.embed_url = data['embedUrl']

class User(RdioObject):
    """Describes an Rdio user."""
    
    def __init__(self, data=None):
        if data:
            super(User, self).__init__(data)
            self.first_name = data['firstName']
            self.last_name = data['lastName']
            self.library_version = data['libraryVersion']
            self._gender = data['gender']
            if self._gender == 'm':
                self.gender = 'Male'
            elif self._gender == 'f':
                self.gender = 'Female'
            self.user_type = data['type']
            self.username = None
            self.last_song_played = None
            self.display_name = None
            self.track_count = None
            self.last_song_play_time = None
            if 'username' in data:
                self.username = data['username']
            if 'lastSongPlayed' in data:
                self.last_song_played = data['lastSongPlayed']
            if 'displayName' in data:
                self.display_name = data['displayName']
            if 'trackCount' in data:
                self.track_count = data['trackCount']
            if 'lastSongPlayTime' in data:
                self.last_song_play_time = data['lastSongPlayTime']
    
    def get_full_url(self):
        return root_site_url + self.url

class ApiError(Exception):
    """Handles exceptions around missing API arguments."""
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return repr(self.msg)

class Api(object):
    """Handles communication with Rdio API."""
    
    def __init__(self,
                 consumer_key=None,
                 consumer_secret=None,
                 access_token_key=None,
                 access_token_secret=None):
        """Instantiates a new Rdio API object."""
        self.set_credentials(consumer_key, consumer_secret)
    
    def set_credentials(self,
                       consumer_key,
                       consumer_secret,
                       access_token_key=None,
                       access_token_secret=None):
        """Sets the consumer_key and _secret for this instance."""
        self._consumer_key        = consumer_key
        self._consumer_secret     = consumer_secret
        self._access_token_key    = access_token_key
        self._access_token_secret = access_token_secret
        
        if access_token_key and access_token_secret:
            self._oauth_token    = oauth.Token(key=access_token_key,
                                               secret=access_token_secret)
        if consumer_key and consumer_secret:
            self._oauth_consumer = oauth.Consumer(key=consumer_key,
                                                  secret=consumer_secret)
            self._oauth_client   = oauth.Client(self._oauth_consumer)
    
    def find_user(self, email=None, vanity_name=None):
        data = {'method': methods[inspect.stack()[0][3]]}
        
        if email:
            data['email'] = email
        if vanity_name:
            data['vanityName'] = vanity_name
        
        print data
        result = self.call_api(data)
        if result:
            return User(result)
        else:
            return None
    
    def call_api(self, data):
        """Calls the Rdio API. Responsible for handling errors from the API."""
        try:
            request = self._oauth_client.request(root_url, http_method,
                                                 urllib.urlencode(data))
            request_dict = ast.literal_eval(request[1])
            if request_dict['status'] == 'error':
                raise ApiError(request_dict['message'])
                return None
            elif request_dict['status'] == 'ok':
                return request_dict['result']
            return request_dict
        except (ApiError) as e:
            print "API error: %s" % e.msg
    