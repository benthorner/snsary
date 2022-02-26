"""
A store has a dict-like interface to get and set data that a consumer wants to persist between program restarts e.g. the current :mod:`Readings <snsary.models.reading>` in a :mod:`Window <snsary.functions.window>`. This module provides a ``get_storage`` function and a ``HasStore`` trait to make it easy access to persistent storage.

By default persistent storage is disabled to avoid creating files without warning - the data stored is only held in memory and not written to disk. Set the ``STORAGE_PATH`` environment variable to enable persistent storage to a file e.g. ``export STORAGE_PATH=snsary.db``.

Storage internals
=================

Persistent storage uses the `pickle <https://docs.python.org/3/library/pickle.html>`_ module internally. Data to be stored is only written to disk when a program exits, to prevent any issues from concurrent writes. If the specified file doesn't exist when a program starts, it will be created when data is first written.

Even persistent storage will expire, to prevent a build up of dead data over time as a program evolves with different consumers of storage and different data to store. Set the ``STORAGE_TTL`` environment variable to override the default TTL of 1 day.

The storage format is not versioned and may break without warning after an upgrade. You will need to manually remove the file at ``STORAGE_PATH`` if this happens.
"""

import atexit
import os
import pickle

from cachetools import TTLCache, cached

from .logger import get_logger


class HasStore:
    @property
    def store(self):
        """
        Shortcut to calling ``get_storage()`` directly.
        """
        return get_storage()


@cached({})
def get_storage():
    """
    Returns a memoised dict-like store.
    """
    return _get_storage_backend()


def _get_storage_backend():
    path = os.environ.get('STORAGE_PATH', '')

    if not path:
        get_logger().debug('Using memory store.')
        return dict()

    get_logger().debug(f'Using store {path}.')
    ttl = os.environ.get('STORAGE_TTL', 86400)

    get_logger().debug(f'Store TTL set to {ttl}.')
    return _get_file_backend(path, int(ttl))


def _get_file_backend(path, ttl):
    try:
        cache = pickle.load(open(path, 'rb'))
    except Exception:
        get_logger().debug(f'{path} not found.')
        get_logger().debug('Creating new store.')
        cache = TTLCache(float('inf'), ttl)

    def atexit_handler():
        get_logger().debug(f'Writing store {path}.')
        pickle.dump(cache, open(path, 'wb'))

    atexit.register(atexit_handler)
    return cache
