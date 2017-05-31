from setuptools import setup

setup(
    name='spotify_connect_scrobbler',
    version='0.1',
    license='MIT',
    packages=['spotify_connect_scrobbler'],
    install_requires=['python-dateutil', 'requests'],
    entry_points = {
        'console_scripts': ['scrobbler=spotify_connect_scrobbler.scrobbler:main']
    }
    )
