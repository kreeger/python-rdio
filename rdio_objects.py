import rdio_functions

rdio_types = {
    'r': 'artist',
    'rl': 'artist',
    'a': 'album',
    'al': 'album',
    't': 'track',
    'p': 'playlist',
    's': 'user',
}

rdio_genders = {
    'm': ('male', 'his',),
    'f': ('female', 'her',),
}

rdio_activity_types = {
    0: ('track added to collection','%s added some music to %s collection.',),
    1: ('track added to playlist','%s added some music to a playlist.',),
    3: ('friend added','%s added a friend.',),
    5: ('user joined','%s joined Rdio.',),
    6: ('comment added to track','%s commented on a track.',),
    7: ('comment added to album','%s commented on an album.',),
    8: ('comment added to artist','%s commented on an artist.',),
    9: ('comment added to playlist','%s commented on a playlist.',),
    10: ('track added via match collection',
         '%s matched music to %s collection.',),
    11: ('user subscribed to Rdio','%s subscribed to Rdio.',),
    12: ('track synced to mobile','%s synced some music to %s mobile app.',),
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
        self.hits = None
        if 'albumCount' in data: self.album_count = data['albumCount']
        if 'hits' in data: self.hits = data['hits']

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
        self.hits = None
        if 'trackKeys' in data: self.track_keys = data['trackKeys']
        if 'releaseDateISO' in data:
            self.release_date_iso = data['releaseDateISO']
        if 'hits' in data: self.hits = data['hits']

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
        self.gender = rdio_genders[data['gender']][0]
        self.gender_posessive = rdio_genders[data['gender']][1]
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
    
    def __init__(self, data):
        super(RdioSearchResult, self).__init__()
        self.album_count = data['album_count']
        self.artist_count = data['artist_count']
        self.number_results = data['number_results']
        self.person_count = data['person_count']
        self.playlist_count = data['playlist_count']
        self.track_count = data['track_count']
        self.results = parse_result_list(data['results'])

class RdioActivityItem(object):
    """Describes an item in Rdio's history object list."""
    
    def __init__(self, data):
        super(RdioActivityItem, self).__init__()
        self.owner = RdioUser(data['owner'])
        self.date = data['date']
        self.update_type_id = data['update_type']
        self.update_type = rdio_activity_types[data['update_type']][0]
        self._verbose_type = rdio_activity_types[data['update_type']][1]
        if self.update_type_id in (0,10,12,):
            self.verbose_update_type = self._verbose_type % (
                self.owner.name, self.owner.gender_posessive,)
        else: self.verbose_update_type = self._verbose_type % self.owner.name
        self.albums = []
        self.reviewed_item = None
        self.comment = ''
        # gotta be a better way of storing the main subject object
        self.subject = None
        if 'albums' in data:
            for album in data['albums']:
                self.albums.append(RdioAlbum(album))
            self.subject = self.albums
        if 'reviewed_item' in data:
            self.reviewed_item = rdio_functions.derive_rdio_type_from_data(
                data['reviewed_item'])
            self.subject = self.reviewed_item
        if 'comment' in data:
            self.comment = data['comment']
            self.subject = self.comment

class RdioActivityStream(object):
    """Describes a stream of history for a user, for public, etc."""
    
    def __init__(self, data):
        super(RdioActivityStream, self).__init__()
        self.last_id = data['last_id']
        self.user = RdioUser(data['user']) # public? everyone?
        self.updates = []
        if 'updates' in data:
            for update in data['updates']:
                self.updates.append(RdioActivityItem(update))