import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name             = 'python-rdio',
    version          = '0.4',
    author           = 'Benjamin Kreeger',
    author_email     = 'benjaminkreeger@gmail.com',
    description      = 'An unofficial wrapper for the Rdio API.',
    license          = 'MIT',
    keywords         = 'api rpc rdio music',
    platforms        = 'any',
    url              = 'http://github.com/kreeger/pyrdio',
    packages         = find_packages(),
    long_description = read('README'),
    install_requires = ['oauth2>=1.5.167',],
)