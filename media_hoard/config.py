# -*- coding: utf-8 -*-

"""Module Media Hoard.config"""
import os

def get_data_root():
    """Return data root directory path."""
    data_root_default = '{}/.local/share/jstout-us/media-hoard'.format(os.environ['HOME'])
    return os.environ.get('MH_DATA_ROOT', data_root_default)
