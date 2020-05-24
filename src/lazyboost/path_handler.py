#  LazyBoost
#  Copyright (C) 2020  Ankit Sadana
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
path handler module handles retrieval of respective directories based on RuntimeFileType needed.
"""

from enum import auto
import os
import sys

from lazyboost.constants import LOG_DEFAULT_NAME, LOG_DIR, \
    LOG_ERROR_NAME, CONFIG_DIR, CONFIG_PATH, USER_DATA
from lazyboost.utility_base import BaseEnum


class RuntimeFileType(BaseEnum):
    """
    RuntimeFileType extends lazyboost.utility_base.BaseEnum.
    This class provides enums to sort and organize the paths of files created/used by this
    application.
    """
    CONFIG = auto()
    LOG = auto()


class ContainmentType(BaseEnum):
    """
    ContainmentType extends lazyboost.utility_base.BaseEnum.
    This class provides enums as identifiers for each type of containment.
    """
    NONE = auto()
    PIPENV = auto()
    SNAP = auto()


def _get_containment_type():
    """
    Function to return the application containment type.
    NOTE: pipenv is preferred over snap.
    :return: ContainmentType.NONE, if the install is without containment.
    :return: ContainmentType.SNAP, if the install is contained inside a SNAP.
    :return: ContainmentType.PIPENV, if the install is contained within pipenv.
    """
    # check if the application is working in python virtual environment
    _is_pipenv = os.getenv('VIRTUAL_ENV')
    # check if the application is working in snapcraft environment
    _is_snap = os.getenv('SNAP')

    if _is_pipenv:
        return ContainmentType.PIPENV

    if _is_snap:
        return ContainmentType.SNAP

    return ContainmentType.NONE


def get_log_dir():
    """
    Function that generates and returns log directory path based on current ContainmentType.
    :return: str, directory path to log folder.
    """
    containment_type = _get_containment_type()
    if containment_type == ContainmentType.SNAP:
        log_path = os.path.join(os.getenv('SNAP_USER_COMMON'), 'logs')
    else:
        if containment_type == ContainmentType.PIPENV:
            os_prefix = sys.prefix
        else:
            os_prefix = os.path.expanduser('~')

        log_path = os.path.join(os_prefix, LOG_DIR)

    if not os.path.isdir(log_path):
        os.makedirs(log_path, mode=0o775)
    return log_path


def get_log_file_paths():
    """
    Function that uses get_log_dir and appends the regular and error log name.
    :return: (str, str), absolute paths for regular and error log files.
    """
    log_dir = get_log_dir()
    return os.path.join(log_dir, LOG_DEFAULT_NAME), os.path.join(log_dir, LOG_ERROR_NAME)


def get_config_dir():
    """
    Function that generates and returns config directory path based on current ContainmentType.
    :return: str, directory path to config folder.
    """
    containment_type = _get_containment_type()
    if containment_type == ContainmentType.SNAP:
        config_path = os.path.join(os.getenv('SNAP_USER_COMMON'), 'configs')
    else:
        if containment_type == ContainmentType.PIPENV:
            os_prefix = sys.prefix
        else:
            os_prefix = os.path.expanduser('~')

        config_path = os.path.join(os_prefix, CONFIG_DIR)

    if not os.path.isdir(config_path):
        os.makedirs(config_path, mode=0o775)
    return config_path


def get_config_file_path():
    """
    Function that uses get_config_dir and appends the config file name.
    :return: str, absolute path for config file.
    """
    return os.path.join(get_config_dir(), CONFIG_PATH)


def get_user_data_dir():
    """
    Function that generates and returns user data directory path based on current ContainmentType.
    :return: str, directory path to the user data folder.
    """
    containment_type = _get_containment_type()
    if containment_type == ContainmentType.SNAP:
        user_data_path = os.path.join(os.getenv('SNAP_USER_DATA'), 'exports')
    else:
        if containment_type == ContainmentType.PIPENV:
            os_prefix = sys.prefix
        else:
            os_prefix = os.path.expanduser('~')

        user_data_path = os.path.join(os_prefix, USER_DATA)

    if not os.path.isdir(user_data_path):
        os.makedirs(user_data_path, mode=0o775)
    return user_data_path
