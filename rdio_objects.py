import rdio_functions

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

rdio_activity_types = {
    0: 'track added to collection',
    1: 'track added to playlist',
    3: 'friend added',
    5: 'user joined',
    6: 'comment added to track',
    7: 'comment added to album',
    8: 'comment added to artist',
    9: 'comment added to playlist',
    10: 'track added via match collection',
    11: 'user subscribed to Rdio',
    12: 'track synced to mobile',
}

# Here come the objects

class RdioObject(object):
    """Describes common fields a base Rdio object will have."""
    
    def __init__(self, data):
        self._data = data
        self.key = data['key']
        self.url = data['url']
        self.icon = data['icon']
        self.base_icon = data['baseIcon']
        self.rdio_type = rdio_types[data['type']]

class RdioArtist(RdioObject):
    """Describes an Rdio artist."""
    
    def __init__(self, data):
        super(RdioArtist, self).__init__(data)
        self.name = data['name']
        self.track_count = data['length']
        self.has_radio = data['hasRadio']
        self.short_url = data['shortUrl']
        self.album_count = -1
        if 'albumCount' in data: self.album_count = data['albumCount']

class RdioMusicObject(RdioObject):
    """Describes an Rdio music object."""
    
    def __init__(self, data):
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
    
    def __init__(self, data):
        super(RdioAlbum, self).__init__(data)
        self.release_date = data['displayDate']
        self.track_keys = []
        self.release_date_iso = None
        if 'trackKeys' in data: self.track_keys = data['trackKeys']
        if 'releaseDateISO' in data:
            self.release_date_iso = data['releaseDateISO']

class RdioTrack(RdioMusicObject):
    """Describes an Rdio track."""
    
    def __init__(self, data):
        super(RdioTrack, self).__init__(data)
        self.album_artist_name = data['albumArtist']
        self.album_artist_key = data['albumArtistKey']
        self.can_download = data['canDownload']
        self.can_download_album_only = data['canDownloadAlbumOnly']
        self.play_count = -1
        if 'playCount' in data: self.play_count = data['playCount']

class RdioPlaylist(RdioObject):
    """Describes an Rdio playlist."""
    
    def __init__(self, data):
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
    
    def __init__(self, data):
        super(RdioUser, self).__init__(data)
        self.first_name = data['firstName']
        self.last_name = data['lastName']
        self.name = self.get_full_name()
        self.library_version = data['libraryVersion']
        self.gender = rdio_genders[data['gender']]
        self.user_type = data['type']
        self.username = None
        self.last_song_played = None
        self.display_name = None
        self.track_count = None
        self.last_song_play_time = None
        if 'username' in data: self.username = data['username']
        if 'lastSongPlayed' in data:
            self.last_song_played = data['lastSongPlayed']
        if 'displayName' in data: self.display_name = data['displayName']
        if 'trackCount' in data: self.track_count = data['trackCount']
        if 'lastSongPlayTime' in data:
            self.last_song_play_time = data['lastSongPlayTime']
    
    def get_full_url(self):
        return root_site_url + self.url
    
    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name,)

class RdioSearchResult(object):
    """Describes an Rdio search result and the extra fields it brings."""
    
    def __init__(self, data, results):
        super(RdioSearchResult, self).__init__()
        self.album_count = data['album_count']
        self.artist_count = data['artist_count']
        self.number_results = data['number_results']
        self.person_count = data['person_count']
        self.playlist_count = data['playlist_count']
        self.track_count = data['track_count']
        self.results = results

class RdioActivityItem(object):
    """Describes an item in Rdio's history object list."""
    
    def __init__(self, data):
        super(RdioActivityItem, self).__init__()
        self.owner = RdioUser(data['owner'])
        self.date = data['date']
        self.update_type_id = data['update_type']
        self.update_type = rdio_activity_types[data['update_type']]
        self.albums = []
        self.reviewed_item = None
        self.comment = ''
        self.subject = None
        if 'albums' in data:
            self.albums.append(RdioAlbum(album for album in data['albums']))
            self.subject = self.albums
        if 'reviewed_item' in data:
            self.reviewed_item = rdio_functions.derive_rdio_type_from_data(
                data['reviewed_item'])
            self.subject = self.reviewed_item
        if 'comment' in data: self.comment = data['comment']
            self.subject = self.comment

class RdioActivityStream(object):
    """Describes a stream of history for a user, for public, etc."""
    
    def __init__(self, data):
        super(RdioActivityStream, self).__init__()
        self.last_id = data['last_id']
        self.user = RdioUser(data['user']) # public? everyone?
        self.updates = []
        if 'updates' in data:
            self.updates.append(
                RdioActivityItem(update for update in data['updates']))