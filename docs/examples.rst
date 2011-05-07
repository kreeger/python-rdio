========
Examples
========

Below are some examples on how to get data from the Rdio API using the wrapper. For each example, assume that I've already got an instance of the manager class as such (fully authenticated). Also, note that each python prompt line will begin with ``>>>``.

>>> import rdio
>>> api = rdio.Api('aosiudASUDH76ASD&8&SDasd', 'iuahd6542gSSA', 'UAHiduas7d6A%SD24dsaa', 'AJSADU36shj')

Finding a user
==============

>>> user = api.find_user(vanity_name='ian')
>>> print "%s, %s" % (user.name, user.key,)
Ian McKellar, s13
>>> user = api.find_user(email='benjaminkreeger@gmail.com')
>>> print "%s, %s" % (user.name, user.key,)
Benjamin Kreeger, s1250

Authenticating a user
=====================

Also coming soon.