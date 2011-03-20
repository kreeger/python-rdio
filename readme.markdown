# python-rdio

## About

Another Python library for accessing the [Rdio API](http://developer.rdio.com/), using OAuth. Inspired by [Rdio's own 'rdio-python' library](http://github.com/rdio/rdio-python/) and [python-twitter](http://code.google.com/p/python-twitter/). 

## Usage

    import rdio
    rdio_manager = rdio.Api(CONSUMER_KEY, CONSUMER_SECRET)
    user = rdio_manager.get_user('benjaminkreeger@gmail.com')
    print '%s %s's key is: %s.' % (user.first_name, user.last_name, user.key)

## Version history

Because you all care.

 * **Version 0.1**: Initial release. Includes data models, unauthenticated API call logic, and one call.