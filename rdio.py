#!/usr/bin/env python
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
import json
import urllib

from rdio_functions import derive_rdio_type_from_data, validate_email
from rdio_functions import parse_result_dictionary, parse_result_list
from rdio_objects import *

# Declare some constants and stuff

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

# Define API error handling.

class RdioGenericAPIError(Exception):
    """Handles all other unknown Rdio API errors."""

    def __init__(self, method):
        super(RdioGenericAPIError, self).__init__()
        self.method   = method
        print "An error occurred: %s." % (
            self.method,)

class RdioMissingArgumentError(Exception):
    """Handles exceptions around missing arguments."""
    
    def __init__(self, argument, method):
        super(RdioMissingArgumentError, self).__init__()
        self.argument = argument
        self.method   = method
        print "Method %s is missing required argument %s." % (
            self.method, self.argument,)
    
    def __str__(self):
        return repr("Method %s is missing required argument %s." % (
            self.method, self.argument,))

class RdioNotAuthenticatedException(Exception):
    """Handles exceptions around not being logged in."""
    
    def __init__(self, method):
        super(RdioNotAuthenticatedException, self).__init__()
        self.method = method
        print "User is not authenticated. %s cannot be called." % (
            self.method,)
    
    def __str__(self):
        return repr("User is not authenticated. %s cannot be called." %
            (self.method,))

class RdioInvalidParameterException(Exception):
    """Handles exceptions around invalid parameters being passed in."""

    def __init__(self, value, param, method):
        super(RdioInvalidParameterException, self).__init__()
        self.value  = value
        self.param  = param
        self.method = method
        print "%s is an invalid parameter for %s in method %s." % (
            self.value, self.param, self.method,)

    def __str__(self):
        return repr("%s is an invalid parameter for %s in method %s." % (
            self.value, self.param, self.method,))

# Here's the big kahuna.

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
    
    def set_credentials(self, consumer_key=None, consumer_secret=None,
                       access_token_key=None, access_token_secret=None):
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
                raise RdioGenericAPIError("Must set token first.")
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
        except RdioGenericAPIError as e:
            print "API error: %s." % e.msg
    
    def call_api_authenticated(self, data):
        """Handles checking authentication before talking to the Rdio API.

        Keyword arguments:
        data -- the dictionary of data for the call, including 'method' param.

        """
        if not self._oauth_access_token:
            raise RdioNotAuthenticatedException(data['method'])
        else: return self.call_api(data)

    def call_api(self, data):
        """Calls the Rdio API. Responsible for handling errors from the API.

        Keyword arguments:
        data -- the dictionary of data for the call, including 'method' param.

        """
        data = urllib.urlencode(data)
        response, content = self._oauth_client.request(root_url,
                                                       http_method, data)
        parsed_content = json.loads(content)
        status = parsed_content['status']
        if status == 'error':
            raise RdioGenericAPIError(parsed_content['message'])
            return None
        elif status == 'ok':
            return parsed_content['result']

    def add_friend(self, user):
        """Add a friend to the current user. Returns True if the add succeeds,
        and False if it fails. Requires authentication.
        
        Keyword arguments:
        user -- the key of the user to add as a friend.
        
        """
        data = {'method': methods['add_friend'], 'user': user}
        
        return self.call_api_authenticated(data)
    
    def add_to_collection(self, keys):
        """Adds tracks or playlists to the current user's collection.
        
        Keyword arguments:
        keys -- a list of tracks or playlists to add to the user's collection.
        
        """
        data = {'method': methods['add_to_collection'], 'keys': ','.join(keys)}
        
        return self.call_api_authenticated(data)
    
    def add_to_playlist(self, playlist, tracks):
        """Add a track to a playlist.
        
        Keyword arguments:
        playlist -- key of the playlist to add to.
        tracks   -- keys of tracks to add to the playlist.
        
        """
        data = {
            'method': methods['add_to_playlist'],
            'playlist': playlist,
            'keys': ','.join(tracks)}
        
        return self.call_api_authenticated(data)
    
    def create_playlist(self, name, description, tracks, extras=[]):
        """Create a new playlist in the current user's collection. The new
        playlist will be returned if the creation is successful; otherwise null
        will be returned.
        
        Keyword arguments:
        name        -- playlist name.
        description -- playlist description.
        tracks      -- a list of initial tracks to start the playlist.
        extras      -- optional. A list of additional fields to return.
        """
        data = {
            'method': methods['create_playlist'],
            'name': name,
            'description': description,
            'tracks': ','.join(tracks)}
            
        if extras: data['extras'] = ','.join(extras)
        result = self.call_api_authenticated(data)
        
        return RdioPlaylist(result) if result else None
    
    def current_user(self, extras=[]):
        """Gets information about the currently logged in user. Requires
        authentication.
        
        Keyword arguments:
        extras -- a list of additional fields to return.
        
        """
        data = {'method': methods['current_user']}
        
        if extras: data['extras'] = ','.join(extras)
        result = self.call_api_authenticated(data)
        return RdioUser(result) if result else None
    
    def delete_playlist(self, playlist):
        """Delete a playlist.
        
        Keyword arguments:
        playlist -- the key of the playlist to delete.
        
        """
        data = {'method': methods['delete_playlist'], 'playlist': playlist}
        
        return self.call_api_authenticated(data)
    
    def find_user(self, email=None, vanity_name=None):
        """Finds an Rdio user by email or username. Exactly one of email or
        vanity_name must be supplied.
        
        Keyword arguments:
        email       -- the desired user's email address.
        vanity_name -- the desired user's vanity name.
        
        """
        data = {'method': methods['find_user']}
        
        if email:
            if validate_email(email): data['email'] = email
            else: raise RdioInvalidParameterException(
                "Invalid email address: %s." % email)
        if vanity_name: data['vanityName'] = vanity_name
        result = self.call_api(data)
        return RdioUser(result) if result else None
    
    def get(self, keys, extras=[]):
        """Fetch one or more objects from Rdio.
        
        Keyword arguments:
        keys   -- a list of keys for the objects to fetch.
        extras -- optional. A list of additional fields to return.
        
        """
        data = {'method': methods['get'], 'keys': ','.join(keys)}
            
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_dictionary(results) if results else None
    
    def get_activity_stream(self, user, scope, last_id=None):
        """Get the activity events for a user, a user's friends, or everyone
        on Rdio.
        
        Keyword arguments:
        user    -- the key of the user to retrieve an activity stream for.
        scope   -- the scope of the activity stream, either "user", "friends"
                   or "everyone".
        last_id -- optional. the last_id returned by the last call to
                   getActivityStream - only activity since that call will be
                   returned.
        
        """
        data = {'method': methods['get_activity_stream'], 'user': user}
        
        if scope:
            if scope in ('user','friends','everyone',):
                data['scope'] = scope
            else: raise RdioInvalidParameterException(
                scope, 'scope', 'get_activity_stream')
        else: raise RdioMissingArgumentError('scope','get_activity_stream')
        if last_id: data['last_id'] = last_id
        results = self.call_api(data)
        return RdioActivityStream(results) if results else None
    
    def get_albums_for_artist(self, artist, featuring=False, extras=[],
                              start=None, count=None):
        """Returns the albums by (or featuring) an artist.
        
        Keyword arguments:
        artist      -- the key of the artist to retrieve albums for.
        featuring   -- optional. True returns albums the artist is featured on
                       instead of albums by ther user.
        extras      -- optional. A list of optional fields to return.
        start       -- optional. The offset of the first result to return.
        count       -- optional. The maximum number of results to return.
        
        """
        data = {'method': methods['get_albums_for_artist'], 'artist': artist}
        
        if featuring: data['featuring'] = featuring
        if extras: data['extras'] = ','.join(extras)
        if start: data['start'] = start
        if count: data['count'] = count
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_albums_for_artist_in_collection(self, artist, user=None):
        """Returns the albums by an artist in a user's collection.

        Keyword arguments:
        artist  -- the key of the artist to retrieve albums for.
        user    -- optional. The owner of the collection to search.

        """
        data = {
            'method': methods['get_albums_for_artist_in_collection'],
            'artist': artist}
        
        if user: data['user'] = user
        
        if user: results = self.call_api(data)
        else: results = self.call_api_authenticated(data)
        return parse_result_list(results) if results else None
    
    def get_albums_in_collection(self, user=None, start=None, count=None,
                                 sort=None, query=None):
        """Returns the albums in a user's collection.
        
        Keyword arguments:
        user    -- optional. The owner of the collection to search.
        start   -- optional. The offset of the first result to return.
        count   -- optional. The maximum number of results to return.
        sort    -- optional. Ways to sort the results. Valid options are
                   'dateAdded', 'playCount', 'artist', and 'name'.
        query   -- optional. The query to filter albums with.
        
        """
        data = {'method': methods['get_albums_in_collection']}
        
        if user: data['user'] = user
        if start: data['start'] = start
        if count: data['count'] = count
        if sort:
            if sort in ('dateAdded','playCount','artist','name',):
                data['sort'] = sort
            else: raise RdioInvalidParameterException(
                sort, 'sort', 'get_albums_in_collection')
        if query: data['query'] = query
        if user: results = self.call_api(data)
        else: results = self.call_api_authenticated(data)
        return parse_result_list(results) if results else None
    
    def get_artists_in_collection(self, user=None, start=None, count=None,
                                  sort=None, query=None):
        """Returns the albums in a user's collection.

        Keyword arguments:
        user    -- optional. The owner of the collection to search.
        start   -- optional. The offset of the first result to return.
        count   -- optional. The maximum number of results to return.
        sort    -- optional. Ways to sort the results. Valid option is
                   'name' only.
        query   -- optional. The query to filter artists with.
        
        """
        data = {'method': methods['get_artists_in_collection']}
        
        if user: data['user'] = user
        if start: data['start'] = start
        if count: data['count'] = count
        if sort:
            if sort in ('name',):
                data['sort'] = sort
            else: raise RdioInvalidParameterException(
                sort, 'sort', 'get_artists_in_collection')
        if query: data['query'] = query
        if user: results = self.call_api(data)
        else: results = self.call_api_authenticated(data)
        return parse_result_list(results) if results else None
    
    def get_heavy_rotation(self, user=None, object_type=None, friends=False,
                           limit=None):
       """Finds the most popular artists or albums for a user, their friends,
       or the whole site.
       
       Keyword arguments:
       user        -- optional. The user to get heavy rotation for, or if this
                      is missing, everyone.
       object_type -- optional. Values are "artists" or "albums".
       friends     -- optional. If True, gets the user's friend's heavy
                      rotation instead of the user's.
       limit       -- optional. The maximum number of results to return.
       
       """
       data = {'method': methods['get_heavy_rotation']}
       
       if user: data['user'] = user
       if object_type:
           if object_type in ('artists','albums',):
               data['type'] = object_type
           else: raise RdioInvalidParameterException(
               object_type, 'type', 'get_heavy_rotation')
       if friends: data['friends'] = friends
       if limit: data['limit'] = limit
       results = self.call_api(data)
       return parse_result_list(results) if results else None
    
    def get_new_releases(self, time=None, start=None, count=False,
                         extras=[]):
        """Returns new albums released across a timeframe.
        
        Keyword arguments:
        time     -- optional. Timeframe, either 'thisweek', 'lastweek', or
                    'twoweeks'.
        start    -- optional. The offset of the first result to return.
        count    -- optional. The maximum number of results to return.
        extras   -- optional. A list of additional fields to return.
        
        """
        data = {'method': methods['get_new_releases']}
        
        if time:
            if time in ('thisweek','lastweek','twoweeks',):
                data['time'] = time
            else: raise RdioInvalidParameterException(
                time, 'time', 'get_new_releases')
        if start: data['start'] = start
        if count: data['count'] = count
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_object_from_short_code(self, short_code):
        """Returns the object that the supplied Rdio short-code is a
        representation of, or None if the short-code is invalid.
        
        Keyword arguments:
        short_code -- the short-code (everything after http://rd.io/x/).
        
        """
        data = {
            'method': methods['get_object_from_short_code'],
            'short_code': short_code}
        
        result = self.call_api_authenticated(data)
        return derive_rdio_type_from_data(result) if result else None
    
    def get_object_from_url(self, url):
        """Return the object that the supplied Rdio short-code is a
        representation of, or null if the short-code is invalid.
        
        Keyword arguments:
        url -- the path portion of the url, including first slash.
        
        """
        data = {'method': methods['get_object_from_url'], 'url': url}
        result = self.call_api_authenticated(data)
        return derive_rdio_type_from_data(result) if result else None
    
    def get_playback_token(self, domain=None):
        """Get a playback token. If you are using this for web playback, you
        must supply a domain.
        
        Keyword arguments:
        domain -- optional. The domain in which the playback SWF will be
                  embedded.
        
        """
        data = {'method': methods['get_playback_token']}
        if domain: data['domain'] = domain
        result = self.call_api(data)
        return result if result else None
    
    def get_playlists(self, extras=[]):
        """Get the current user's playlists.
        
        Keyword arguments:
        extras -- optional. A list of additional fields to return.
        
        """
        data = {'method': methods['get_playlists']}
        if extras: data['extras'] = ','.join(extras)
        
        results = self.call_api_authenticated(data)
        return RdioPlaylistSet(results) if results else None
    
    def get_top_charts(self, result_type, start=None, count=None, extras=[]):
        """Return the site-wide most popular items for a given type.
        
        Keyword arguments:
        result_type -- type to include in results, valid values are "Artist",
                       "Album", "Track", and "Playlist".
        start       -- optional. The offset of the first result to return.
        count       -- optional. The maximum number of results to return.
        extras      -- optional. A list of additional fields to return.
        
        """
        data = {'method': methods['get_top_charts']}
        
        if result_type in ('Artist','Album','Track','Playlist',):
            data['type'] = result_type
        else: raise RdioInvalidParameterException(
            result_type, 'result_type', 'get_top_charts')
        if start: data['start'] = start
        if count: data['count'] = count
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_tracks_for_album_in_collection(self, album, user=None, extras=[]):
        """Which tracks on the given album are in the user's collection.
        
        Keyword arguments:
        album  -- the key of the album.
        user   -- optional. The user whose collection to examine.
        extras -- optional. A list of additional fields to return.
        
        """
        data = {
            'method': methods['get_tracks_for_album_in_collection'],
            'album': album}
            
        if user: data['user'] = user
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_tracks_for_artist(self, artist, appears_on=None, extras=[],
                              start=None, count=None):
        """Get all of the tracks by this artist.
        
        Keyword arguments:
        artist     -- the key of the artist.
        appears_on -- optional. If true, returns tracks that the artist appears
                      on, rather than tracks credited to the artist.
        extras     -- optional. A list of additional fields to return.
        start      -- optional. The offset of the first result to return.
        count      -- optional. The maximum number of results to return.
        
        """
        data = {'method': methods['get_tracks_for_artist'], 'artist': artist}
        
        if appears_on: data['appears_on'] = appears_on
        if extras: data['extras'] = ','.join(extras)
        if start: data['start'] = start
        if count: data['count'] = count
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_tracks_for_artist_in_collection(self, artist, user=None,
                                            extras=[]):
        """Which tracks from the given artist are in the user's collection.
        
        Keyword arguments:
        artist -- the key of the artist.
        user   -- optional. The user whose collection to examine.
        extras -- optional. A list of additional fields to return.
        
        """
        data = {
            'method': methods['get_tracks_for_artist_in_collection'],
            'artist': artist}
        
        if user: data['user'] = user
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def get_tracks_in_collection(self, user=None, start=None, count=None,
                                 sort=None, query=None):
        """Get all of the tracks in the user's collection.
        
        Keyword arguments:
        user  -- optional. The key of the collection user.
        start -- optional. The offset of the first result to return.
        count -- optional. The maximum number of resutls to return.
        sort  -- optional. Sort by. Valid values are "dateAdded", "playCount",
                 "artist", "album", and "name".
        query -- optional. Filter collection tracks by this.
        
        """
        data = {'method': methods['get_tracks_in_collection']}
        
        if user: data['user'] = user
        if start: data['start'] = start
        if count: data['count'] = count
        if sort:
            if sort in ('dateAdded','playCount','artist','album','name',):
                data['sort'] = sort
            else: raise RdioInvalidParameterException(
                sort, 'sort', 'get_tracks_in_collection')
        if query: data['query'] = query
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
    def remove_friend(self, user):
        """Remove a friend from the current user.
        
        Keyword arguments
        user -- the key of the user to remove.
        
        """
        data = {'method': methods['remove_friend'], 'user': user}
        
        return self.call_api_authenticated(data)
    
    def remove_from_collection(self, keys):
        """Remove tracks or playlists from the current user's collection.
        
        Keyword arguments:
        keys -- the list of track or playlist keys to remove from the
                collection.
        
        """
        data = {
            'method': methods['remove_from_collection'],
            'keys': ','.join(keys)}
        
        return self.call_api_authenticated(data)
    
    def remove_from_playlist(self, playlist, tracks, index=None, count=None):
        """Remove an item from a playlist by its position in the playlist.
        
        Keyword arguments:
        playlist -- the key of the playlist to modify.
        index    -- the index of the first item to remove.
        count    -- the number of tracks to remove from the playlist.
        tracks   -- the list of keys of the tracks to remove.
        
        """
        data = {
            'method': methods['remove_from_playlist'],
            'playlist': playlist,
            'index': index if index else 0,
            'count': count if count else len(tracks),
            'tracks': ','.join(tracks)}
        
        return self.call_api_authenticated(data)
    
    def search(self, query, types, never_or=None, extras=[], start=None,
               count=None):
        """Search for artists, albums, tracks, users, or all kinds of
        objects.
        
        Keyword arguments:
        query    -- the search query.
        types    -- List of types to include in results. Valid values
                    are "Artist", "Album", "Track", "Playlist", and "User".
        never_or -- optional. Disables Rdio's and/or query default "and".
        extras   -- optional. A list of additional fields to return.
        start    -- optional. The offset of the first result to return.
        count    -- optional. The maximum number of results to return.
        
        """
        data = {
            'method': methods['search'],
            'query': query,
            'types': ','.join(types)}
        
        if never_or: data['never_or'] = never_or
        if extras: data['extras'] = ','.join(extras)
        if start: data['start'] = start
        if count: data['count'] = count
        results = self.call_api(data)
        return RdioSearchResult(results) if results else None
    
    def search_suggestions(self, query, extras=[]):
        """Match the supplied prefix against artists, albums, tracks, and
        people in the Rdio system. Returns the first 10 matches.
        
        Keyword arguments:
        query  -- the search prefix.
        extras -- optional. A list of additional fields to return.
        
        """
        data = {'method': methods['search_suggestions'], 'query': query}
        
        if extras: data['extras'] = ','.join(extras)
        results = self.call_api(data)
        return parse_result_list(results) if results else None
    
