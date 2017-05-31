from setuptools import setup, find_packages

setup(
    name='spotify_connect_scrobbler',
    version='0.1',
    license='MIT',
    packages=find_packages(),
    install_requires=['click', 'python-dateutil', 'requests'],
    entry_points = {
        'console_scripts': ['scrobbler=spotify_connect_scrobbler.scrobbler:main']
    }
    )
