import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = 'python-rdio',
    version          = '0.1',
    author           = 'Benjamin Kreeger',
    author_email     = 'benjaminkreeger@gmail.com',
    description      = 'A library to interact with the Rdio API.',
    license          = 'MIT',
    keywords         = 'api rpc rdio music',
    platforms        = 'any',
    url              = 'http://developer.rdio.com/',
    packages         = find_packages(),
    long_description = read('README'),
)