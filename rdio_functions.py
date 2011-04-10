import re

from rdio_objects import rdio_types, RdioArtist, RdioAlbum, RdioTrack
from rdio_objects import RdioPlaylist, RdioUser

def derive_rdio_type_from_data(rdio_object):
    if rdio_types[rdio_object['type']] == 'artist':
        return RdioArtist(rdio_object)
    if rdio_types[rdio_object['type']] == 'album':
        return RdioAlbum(rdio_object)
    if rdio_types[rdio_object['type']] == 'track':
        return RdioTrack(rdio_object)
    if rdio_types[rdio_object['type']] == 'playlist':
        return RdioPlaylist(rdio_object)
    if rdio_types[rdio_object['type']] == 'user':
        return RdioUser(rdio_object)

def validate_email(email):
    """Validates email address. Should work for now.
    From http://goo.gl/EuVRg.
    
    """
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0

def parse_result_dictionary(results):
    """Takes a dictionary and returns a list of RdioObjects."""
    objects = []
    for rdio_object in results:
        objects.append(derive_rdio_type_from_data(results[rdio_object]))
    return objects

def parse_result_list(results):
    """Takes a list and returns a list of RdioObjects."""
    objects = []
    for rdio_object in results:
        objects.append(derive_rdio_type_from_data(rdio_object))
    return objects