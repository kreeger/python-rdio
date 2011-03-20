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
__version__ = '0.2'

import cgi
import inspect
import oauth2 as oauth
import re
import json
import urllib

root_url = 'http://api.rdio.com/1/'
oauth_token_url = 'http://api.rdio.com/oauth/request_token'
oauth_access_url = 'http://api.rdio.com/oauth/access_token'
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
        """Instantiates a new Rdio API object.
        
        Keyword arguments:
        consumer_key        -- The oAuth API key for the application.
        consumer_secret     -- The oAuth API secret for the application.
        access_token_key    -- The oAuth user's token key.
        access_token_secret -- The oAuth user's token secret.
        
        
        """
        # The only thing to do right now is to set credentials.
        self.set_credentials(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             access_token_key=access_token_key,
                             access_token_secret=access_token_secret)
    
    def set_credentials(self,
                       consumer_key=None,
                       consumer_secret=None,
                       access_token_key=None,
                       access_token_secret=None):
        """Sets the consumer_key and _secret for this instance.
        
        Keyword arguments:
        consumer_key        -- The oAuth API key for the application.
        consumer_secret     -- The oAuth API secret for the application.
        access_token_key    -- The oAuth user's token key.
        access_token_secret -- The oAuth user's token secret.
        
        """
        
        # Set our keys and secrets, depending on what was passed in.
        if consumer_key and consumer_secret:
            # Get our consumer object, which is just made of a key and secret
            self._oauth_consumer     = oauth.Consumer(key=consumer_key,
                                                      secret=consumer_secret)
            # Get our client object, which is simply a consumer (un-authed)
            self._oauth_client       = oauth.Client(self._oauth_consumer)
        if access_token_key and access_token_secret:
            # Get our token object, which identifies us to the API for the user
            # Note: must check for access token when making authenticated calls
            self._oauth_access_token = oauth.Token(key=access_token_key,
                                                   secret=access_token_secret)
            # Upgrade our client object to talk to the API on the user's behalf
            self._oauth_client       = oauth.Client(self._oauth_consumer,
                                                     self._oauth_access_token)
    
    def get_token_and_login_url(self):
        """Gets the oAuth token via the oauth2 library."""
        data = urllib.urlencode({'oauth_callback': 'oob'})
        try:
            # Get token and secret from Rdio's authorization endpoint.
            response, content  = self._oauth_client.request(oauth_token_url,
                                                            http_method, data)
            # Make a dict out of it! Then, save entries to local variables.
            parsed_content     = dict(cgi.parse_qsl(content))
            token              = parsed_content['oauth_token']
            token_secret       = parsed_content['oauth_token_secret']
            login_url          = parsed_content['login_url']
            callback_confirmed = parsed_content['oauth_callback_confirmed']
            # Save our request token object. Don't do this in our 
            # set_credentials function as it's just for the request token,
            # not the full access token.
            self._oauth_request_token = oauth.Token(key=token,
                                                    secret=token_secret)
            # Remove the secret before we send it back.
            del parsed_content['oauth_token_secret']
            # Send back what the user needs to know.
            return parsed_content
        except:
            print "Something happened during %s." % inspect.stack()[0][3]
            pass
    
    def authorize_with_verifier(self, oauth_verifier):
        """Authorizes the oAuth handler with verifier and upgrades the token
        and client. Returns dictionary containing access key and secret if
        success; None if failure.
        
        Keyword arguments:
        oauth_verifier -- required. The PIN code from oAuth.
        
        """
        try:
            # If we don't have a request token yet, let the user know.
            if not self._oauth_request_token:
                raise ApiError("Must set token first.")
            # Tell the token object to get verified.
            self._oauth_request_token.set_verifier(oauth_verifier)
            # Update our client object with our private token object.
            # Don't do this in our set_credentials function as it's just for
            # the request token, not the full access token.
            self._oauth_client = oauth.Client(self._oauth_consumer,
                                              self._oauth_request_token)
            # Get our full-blown, shiny new access token.
            response, content  = self._oauth_client.request(oauth_access_url,
                                                    http_method)
            parsed_content     = dict(cgi.parse_qsl(content))
            token              = parsed_content['oauth_token']
            token_secret       = parsed_content['oauth_token_secret']
            # Send our token to our credential handler function.
            self.set_credentials(access_token_key=token,
                                 access_token_secret=token_secret)
            # If the private token was made, return True; else return False.
            if self._oauth_access_token:
                return {
                    'access_token_key':    token,
                    'access_token_secret': token_secret}
            else:
                return None
        except ApiError as e:
            print "API error: %s." % e.msg
    
    def add_friend(self, user):
        """Add a friend to the current user. Returns True if the add succeeds,
        and False if it fails. Requires authentication.
        
        Keyword arguments:
        user -- the key of the user to add as a friend.
        
        """
        data = {'method': methods['add_friend'], 'user': user}
        if not self._oauth_access_token:
            print "User is not authenticated. %s cannot be called." % (
                data['method'],)
            return None
        
        result = self.call_api(data)
        print result
        return result
    
    def current_user(self, extras=None):
        """Gets information about the currently logged in user. Requires
        authentication.
        
        Keyword arguments:
        extras -- a list of additional fields to return.
        
        """
        data = {'method': methods['current_user']}
        
        if not self._oauth_access_token:
            print "User is not authenticated. %s cannot be called." % (
                data['method'],)
            return None
            
        if extras:
            data['extras'] = extras
        
        result = self.call_api(data)
        if result:
            return User(result)
        else:
            return None
    
    def find_user(self, email=None, vanity_name=None):
        """Finds an Rdio user by email or username. Exactly one of email or
        vanity_name must be supplied.
        
        Keyword arguments:
        email       -- the desired user's email address.
        vanity_name -- the desired user's vanity name.
        
        """
        try:
            data = {'method': methods['find_user']}
        
            if email:
                if validate_email(email):
                    data['email'] = email
                else:
                    raise ApiError("Invalid email address: %s." % email)
            if vanity_name:
                data['vanityName'] = vanity_name
        
            result = self.call_api(data)
            if result:
                return User(result)
            else:
                return None
        except ApiError as e:
            print "API error: %s" % e.msg
    
    def call_api(self, data):
        """Calls the Rdio API. Responsible for handling errors from the API.
        
        Keyword arguments:
        data -- the dictionary of data for the call, including 'method' param.
        
        """
        data = urllib.urlencode(data)
        try:
            response, content = self._oauth_client.request(root_url,
                                                           http_method, data)
            parsed_content = json.loads(content)
            status = parsed_content['status']
            if status == 'error':
                raise ApiError(parsed_content['message'])
                return None
            elif status == 'ok':
                return parsed_content['result']
        except (ApiError) as e:
            print "API error: %s" % e.msg

def validate_email(email):
    """Validates email address. Should work for now.
    Yanked from http://goo.gl/EuVRg
    
    Keyword arguments:
    email -- the text string of an email to validate.
    
    """
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
