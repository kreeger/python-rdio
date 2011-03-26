rdio_types = {
    'r': 'Artist',
    'a': 'Album',
    't': 'Track',
    'p': 'Playlist',
    's': 'User',
}

rdio_genders = {
    'm': 'Male',
    'f': 'Female',
}

class RdioObject(object):
    """Describes common fields a base Rdio object will have."""
    
    def __init__(self, data=None):
        self._data = data
        self.key = data['key']
        self.url = data['url']
        self.icon = data['icon']
        self.base_icon = data['baseIcon']
        self.rdio_type = rdio_types[data['type']]

class RdioArtist(RdioObject):
    """Describes an Rdio artist."""
    
    def __init__(self, data=None):
        if data:
            super(RdioArtist, self).__init__(data)
            self.name = data['name']
            self.track_count = data['length']
            self.has_radio = data['hasRadio']
            self.short_url = data['shortUrl']
            self.album_count = None
            if 'albumCount' in data:
                self.album_count = data['albumCount']

class RdioMusicObject(RdioObject):
    """Describes an Rdio music object."""
    
    def __init__(self, data=None):
        if data:
            super(RdioMusicObject, self).__init__(data)
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

class RdioAlbum(RdioMusicObject):
    """Describes an Rdio album."""
    
    def __init__(self, data=None):
        if data:
            super(RdioAlbum, self).__init__(data)
            self.release_date = data['displayDate']
            self.release_date_iso = None
            if 'trackKeys' in data:
                self.track_keys = data['trackKeys']
            if 'releaseDateISO' in data:
                self.release_date_iso = data['releaseDateISO']

class RdioTrack(RdioMusicObject):
    """Describes an Rdio track."""
    
    def __init__(self, data=None):
        if data:
            super(RdioTrack, self).__init__(data)
            self.album_artist_name = data['albumArtist']
            self.album_artist_key = data['albumArtistKey']
            self.can_download = data['canDownload']
            self.can_download_album_only = data['canDownloadAlbumOnly']
            self.play_count = None
            if 'playCount' in data:
                self.play_count = data['playCount']

class RdioPlaylist(RdioObject):
    """Describes an Rdio playlist."""
    
    def __init__(self, data=None):
        if data:
            super(RdioPlaylist, self).__init__(data)
            self.name = data['name']
            self.track_count = data['length']
            self.owner_name = data['owner']
            self.owner_url = data['ownerUrl']
            self.owner_key = data['ownerKey']
            self.owner_icon = data['ownerIcon']
            self.last_updated = data['lastUpdated']
            self.short_url = data['shortUrl']
            self.embed_url = data['embedUrl']

class RdioUser(RdioObject):
    """Describes an Rdio user."""
    
    def __init__(self, data=None):
        if data:
            super(RdioUser, self).__init__(data)
            self.first_name = data['firstName']
            self.last_name = data['lastName']
            self.library_version = data['libraryVersion']
            self.gender = rdio_genders[data['gender']]
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

class RdioSearchResult(object):
    """Describes an Rdio search result and the extra fields it brings."""
    
    def __init__(self, data=None, results=None):
        if data:
            super(RdioSearchResult, self).__init__()
            self.album_count = data['album_count']
            self.artist_count = data['artist_count']
            self.number_results = data['number_results']
            self.person_count = data['person_count']
            self.playlist_count = data['playlist_count']
            self.track_count = data['track_count']
            self.results = results
