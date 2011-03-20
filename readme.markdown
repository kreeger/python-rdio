# python-rdio

## About

Another Python library for accessing the [Rdio API](http://developer.rdio.com/), using OAuth. Inspired by [Rdio's own 'rdio-python' library](http://github.com/rdio/rdio-python/) and [python-twitter](http://code.google.com/p/python-twitter/). This is more or less a test of my own abilities, as I've been writing [Django](http://djangoproject.com/) for a while, and I'd like to get into more Python-oriented development.

Function names and objects will follow Rdio's API specs for [methods](http://developer.rdio.com/docs/read/rest/methods) and [object types](http://developer.rdio.com/docs/read/rest/types) as closely as possible, accounting for Python-ish function and property names (underscores and all that, instead of camelCase).

## Notes

Please don't fire up `setuptools` just yet. I clearly don't know how to use it.

## Requirements

 * [oauth2](https://github.com/simplegeo/python-oauth2)
 * patience for me

## Usage

    import rdio
    rdio_manager = rdio.Api(CONSUMER_KEY, CONSUMER_SECRET)
    user = rdio_manager.get_user('benjaminkreeger@gmail.com')
    print '%s %s's key is: %s.' % (user.first_name, user.last_name, user.key)

## Version history

Because you all care.

 * **Version 0.1**: Initial release. Includes data models, unauthenticated API call logic, and one call.