import functools
import os
import threading

from dvc.progress import progress


class track_progress(object):
    def __init__(self, progress_name, fobj):
        self.progress_name = progress_name
        self.fobj = fobj
        self.file_size = os.fstat(fobj.fileno()).st_size

    def read(self, size):
        progress.update_target(
            self.progress_name, self.fobj.tell(), self.file_size
        )
        return self.fobj.read(size)

    def __getattr__(self, attr):
        return getattr(self.fobj, attr)


def only_once(func):
    lock = threading.Lock()
    locks = {}
    results = {}

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        # could do with just setdefault, but it would require
        # create/delete a "default" Lock() object for each call, so it
        # is better to lock a single one for a short time
        with lock:
            if key not in locks:
                locks[key] = threading.Lock()
        with locks[key]:
            if key not in results:
                results[key] = func(*args, **kwargs)
        return results[key]

    return wrapped


def response_error_message(response):
    try:
        message = response.json()["error"]["message"]
    except (TypeError, KeyError):
        message = response.text
    return "HTTP {}: {}".format(response.status_code, message)


def response_is_ratelimit(response):
    if response.status_code not in (403, 429):
        return False
    errors = response.json()["error"]["errors"]
    domains = [i["domain"] for i in errors]
    return "usageLimits" in domains


class MetadataCache(object):
    """Remembers the metadata for folders traversal
    """

    def __init__(self, gdrive):
        self.gdrive = gdrive
        self.lock = threading.Lock()
        self.locks = {}
        self.storage = {}

    def _fetch(self, parent, path):
        key = (parent, path)
        with self.lock:
            if key not in self.locks:
                self.locks[key] = threading.Lock()
        with self.locks[key]:
            if key not in self.storage:
                self.storage[key] = self.gdrive.get_metadata_by_path(
                    parent, path
                )
        return self.storage[key]

    def get(self, parent, path):
        key = (parent, path)
        ret = self.storage.get(key)
        if ret is None:
            return self._fetch(parent, path)
        else:
            return self.storage[key]
