# python-rdio

## About

Another Python library for accessing the [Rdio API](http://developer.rdio.com/), using OAuth. Inspired by [Rdio's own 'rdio-python' library](http://github.com/rdio/rdio-python/) and [python-twitter](http://code.google.com/p/python-twitter/). This is more or less a test of my own abilities, as I've been writing [Django](http://djangoproject.com/) for a while, and I'd like to get into more Python-oriented development.

Function names and objects will follow Rdio's API specs for [methods](http://developer.rdio.com/docs/read/rest/methods) and [object types](http://developer.rdio.com/docs/read/rest/types) as closely as possible, accounting for Python-ish function and property names (underscores and all that, instead of camelCase).

## Notes

I'll eventually get `setuptools` rockin' for this thing. Once I figure out how to use it.

## Requirements

 * [python 2.6 or higher](http://python.org/download/releases/) but not python 3.0
 * [oauth2](https://github.com/simplegeo/python-oauth2)

## Usage

    # Setup the API manager. If you have an ACCESS_KEY and ACCESS_SECRET for a
    # particular user, you can pass that in as the third and forth arguments
    # to Api().
    import rdio
    rdio_manager = rdio.Api(CONSUMER_KEY, CONSUMER_SECRET)
    user = rdio_manager.find_user('benjaminkreeger@gmail.com')
    print '%s %s's key is: %s.' % (user.first_name, user.last_name, user.key)
    
    # Set authorization: get authorization URL, then pass back the PIN.
    token_dict = rdio_manager.get_token_and_login_url()
    print 'Authorize this application at: %s?oauth_token=%s' % (
        token_dict['login_url'], token_dict['oauth_token'])
    oauth_verifier = raw_input('Enter the PIN / oAuth verifier: ').strip()
    authorization_dict = rdio_manager.authorize_with_verifier(oauth_verifier)
    
    # Get back key and secret. rdio_manager is now authorized
    # on the user's behalf.
    print 'Access token key: %s' % authorization_dict['access_token_key']
    print 'Access token secret: %s' % authorization_dict['access_token_secret']
    
    # Make an authorized call.
    current_user = rdio_manager.current_user()
    print 'The full name of the current user is %s.' % (
        current_user.name,)
    
    # Have some fun.
    search_object = rdio_manager.search(
            query='Big Echo',
            types=['Albums',],
            extras=['trackKeys',])
    album = search_object.results[0]
    print "Found album %s by %s." % (album.name, album.artist_name,)
    new_playlist = rdio_manager.create_playlist(
        name='Whoopie!',
        description='A test playlist for the Rdio API.',
        tracks=album.track_keys,
        extras=['trackKeys',])
    print "Just made playlist %s with %i tracks at %s! Has tracks: " % (
            new_playlist.name,
            new_playlist.track_count,
            new_playlist.short_url)
    tracks = rdio_manager.get(new_playlist.track_keys)
    for t in tracks: print "%s (Duration: %s seconds)" % (t.name, t.duration,)
    
## Version history

Because you all care.

 * **Version 0.3**: All calls implemented; most of them are working properly. Some minor tweaking may need to be done here and there, but a majority of the work is done.
 * **Version 0.2**: Supports PIN authorization through Rdio's oAuth implementation. Added `current_user` call.
 * **Version 0.1**: Initial release. Includes data models, unauthenticated API call logic, and one call.