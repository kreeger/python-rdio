========
Examples
========

Below are some examples on how to get data from the Rdio API using the wrapper. For each example, assume that I've already got an instance of the manager class as such (fully authenticated). Also, note that each python prompt line will begin with ``>>>`` Continuations after line breaks begin with ``...``.

>>> import rdio
>>> api = rdio.Api('aosiudASUDH76ASD&8&SDasd', 'iuahd6542gSSA', 'UAHiduas7d6A%SD24dsaa', 'AJSADU36shj')

Finding user
============

>>> user = api.find_user(vanity_name='ian')
>>> print "%s, %s" % (user.name, user.key,)
Ian McKellar, s13
>>> user = api.find_user(email='benjaminkreeger@gmail.com')
>>> print "%s, %s" % (user.name, user.key,)
Benjamin Kreeger, s1250

Authenticating user with OAuth pin
==================================

First, you'll need to get the login url and token.

>>> token_dict = api.get_token_and_login_url()
>>> print 'Authorize this application at: %s?oauth_token=%s' % (
...     token_dict['login_url'], token_dict['oauth_token'])

Then you'll need to launch the URL in a web browser, which will prompt the user to login and authorize the application. This'll give the user a PIN code. Have the user copy and paste the code as input to the next line.

>>> oauth_verifier = raw_input('Enter the PIN / oAuth verifier: ').strip()

Then feed it to the ``authorize_with_verifier`` method.

>>> auth_dict = api.authorize_with_verifier(oauth_verifier)

The ``auth_dict`` will contain the ``access_token_key`` and ``access_token_secret`` keys, which you'll undoubtedly want to keep in your datastore for the user's record.

Getting current user
====================

>>> user = api.current_user()
>>> print 'Name: %s, Key: %s' % (user.name, user.key,)
Name: Benjamin Kreeger, Key: s1250

The following examples assume you have the ``current_user``'s results stored in the ``user`` variable.

Getting current user's heavy rotation
=====================================

>>> rotation = api.get_heavy_rotation(user=user.key, friends=True)
>>> for album in rotation[:3]:
...     print "Album: %s, by %s" % (album.name, album.artist_name,)
...     print "Key: %s" % album.key
...     print "Users: %s" % ', '.join([user.name for user in album.users])
...     print "---"
...
Album: TRON: Legacy Reconfigured, by Daft Punk
Key: a687025
Users: Ian McKellar, Michael Battey, Wilson Miner, Madelyn Taylor
---
Album: Disreali Gears (Deluxe Edition), by Cream
Key: a228508
Users: Keith K
---
Album: Hot Sauce Committee Part Two, by Beastie Boys
Key: a711764
Users: Frank Chimero, Madelyn Taylor, Tyler Abele, Nick Kreeger
---

