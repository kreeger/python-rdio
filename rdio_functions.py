from rdio_objects import rdio_types, RdioArtist, RdioAlbum, RdioTrack
from rdio_objects import RdioPlaylist, RdioUser

def derive_rdio_type_from_data(rdio_object):
    if rdio_types[rdio_object['type']] == 'Artist':
        return RdioArtist(rdio_object)
    if rdio_types[rdio_object['type']] == 'Album':
        return RdioAlbum(rdio_object)
    if rdio_types[rdio_object['type']] == 'Track':
        return RdioTrack(rdio_object)
    if rdio_types[rdio_object['type']] == 'Playlist':
        return RdioPlaylist(rdio_object)
    if rdio_types[rdio_object['type']] == 'User':
        return RdioUser(rdio_object)

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

def parse_list_to_comma_delimited_string(list_object):
    """Parses a list object into a comma-delimited string."""
    string = ''
    for thing in list_object:
        string += '%s,' % thing
    return string[:-1]

def parse_result_list(results):
    """Takes a dictionary and returns a list of RdioObjects."""
    objects = []
    for rdio_object in results:
        objects.append(derive_rdio_type_from_data(rdio_object))
    return objects