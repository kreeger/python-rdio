=====
Usage
=====

Getting the manager
===================

This Python-based Rdio API wrapper (``python-rdio``) must be used by creating an instance of the manager class, known as ``Api``. Upon instance creation, you can either feed in just your OAuth ``consumer_key`` and ``consumer_secret``, or (if you've saved them for the user for which you're communicating with the API) your ``consumer_key``, ``consumer_secret``, ``access_key``, and ``access_secret``::

    import rdio
    api = rdio.Api('aosiudASUDH76ASD&8&SDasd', 'iuahd6542gSSA', 'UAHiduas7d6A%SD24dsaa', 'AJSADU36shj')

Making calls
============

Talking to the API manager merely involves calling its methods, and passing in parameters. Every method name on the `Rdio API`_ has been translated here from ``camelCase`` to ``underscored_lower_case``. Thus, ``getTracksForArtistInCollection`` has become ``get_tracks_for_artist_in_collection``. The same goes for parameters. To look at examples, visit :doc:`examples`.

.. _Rdio API: http://developer.rdio.com/docs/read/rest/Methods