# -*- coding: utf-8 -*-

"""Module Media Hoard.util."""
import hashlib
import shutil
import time

from pathlib import Path

import requests
from requests import exceptions

BUF_SIZE = 65536


def copy_file(src, dst):
    """Copy file between source and destination

    Args:
        src(str):   Path in either uri format or local path
        dst(fd):    Open file descriptor to a file like object

    Returns:
        None
    """
    try:
        with requests.get(src, stream=True) as resp:
            resp.raise_for_status()

            for chunk in resp.iter_content(chunk_size=BUF_SIZE):
                dst.write(chunk)

    except (exceptions.MissingSchema, exceptions.InvalidSchema):
        with Path(src).open('rb') as fd_src:
            shutil.copyfileobj(fd_src, dst)


def format_duration(dur):
    """Format runtime duration for display.

    Args:
        dur(int):   Duration in seconds

    Returns:
        duration(str):  Formatted hh:mm:ss
    """
    return time.strftime('%H:%M:%S', time.gmtime(dur))


def hash_file(src):
    """Generate sha1 hash of file.

    Args:
        src(fd):    Open file descriptor for file like object

    returns:
        hash(str):  Hexdigest of src
    """
    hash_ = hashlib.new('sha1')

    while True:
        data = src.read(BUF_SIZE)

        if not data:
            break

        hash_.update(data)

    return hash_.hexdigest()
