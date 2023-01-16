#  LazyBoost
#  Copyright (C) 2023  Ankit Sadana
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

"""

import json
import os

from lazyboost import constants, log, path_handler, utility_base
from lazyboost.models import LazyBoostConfig

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def read_config_from_file(file_name) -> LazyBoostConfig:
    """
    Function that opens file_name in read only mode, parses/decodes json and returns as 
    LazyBoostConfig.
    :param file_name: the full path of the file that contains the config
    :return: An object of L{LazyBoostConfig}
    :exception: TypeError, raised if the config file is not of LazyBoostConfig type.
    :exception: FileNotFoundError, raised if the file_name provided doesn't exist.
    """
    lazy_boost_config = None

    file_name = utility_base.get_path(file_name)
    try:
        with open(file_name, 'r') as config_file:
            try:
                config_dict = json.load(config_file)
                _logger.info(f'Reading config file: {file_name}.')
                lazy_boost_config = _parse_lazy_boost_config_dict(config_dict)
            except (TypeError, ValueError) as e:
                raise TypeError(f"File was not of type LazyBoostConfig: {file_name}") from e
    except FileNotFoundError as err:
        raise FileNotFoundError(f"File not found: {file_name}") from err
    return lazy_boost_config


def get_current_lazy_boost_config(file_name=None) -> LazyBoostConfig:
    """
    Function that attempts to retrieve existing LazyBoostConfig.
    If none exists or there is an error reading it, a new object of LazyBoostConfig is returned.
    :param file_name: the full path of the file that contains the config
    :return: An object of L{LazyBoostConfig}
    """
    lazy_boost_config = None

    if not file_name:
        file_name = path_handler.get_config_file_path()

    try:
        lazy_boost_config = read_config_from_file(file_name)
    except TypeError as err:
        err_msg = f'Parsing failed of the config file: {file_name}'
        _logger.error(f'{err_msg}. Error: {err}')
        _cli_logger.error(f'{err_msg}. Using empty configuration.')
    except FileNotFoundError as err:
        err_msg = f'No existing configuration detected at: {file_name}'
        _logger.warning(f'{err_msg}. Error: {err}')
        _cli_logger.warning(f'{err_msg}. Using empty configuration.')

    if not lazy_boost_config:
        lazy_boost_config = LazyBoostConfig()
    return lazy_boost_config


def write_config_to_file(lazy_boost_config: LazyBoostConfig, file_name=None) -> bool:
    """
    Function that writes the lazy_boost_config to file.
    :param lazy_boost_config: LazyBoostConfig, object that contains the config to be saved.
    :param file_name: str, absolute path to config file.
    :return: bool, True if the config was successfully saved, False otherwise.
    """
    file_written = False
    if not file_name:
        file_name = path_handler.get_config_file_path()

    file_name = utility_base.get_path(file_name)

    if os.path.isfile(file_name):
        backup_file_name = file_name + constants.CONFIG_BACKUP_SUFFIX
        _logger.info(f'Config file already exists, saving existing config to: {backup_file_name}.')
        os.replace(src=file_name, dst=backup_file_name)

    try:
        with open(file_name, 'w') as file:
            _logger.info(f'Writing config file: {file_name}.')
            file.write(utility_base.convert_to_json_str(lazy_boost_config, indent=4))
            file_written = True
    except IOError as err:
        _logger.error(f'Failed to write config file: {file_name}, reason: {err}')

    return file_written


# Internal helper functions

def _parse_lazy_boost_config_dict(config_dict: dict) -> LazyBoostConfig:
    """
    Helper function that takes the config_dict received and converts it into LazyBoostConfig.
    :param config_dict: dict, config dictionary.
    :return: LazyBoostConfig, generated object from the config_dict.
    """
    lazy_boost_config = LazyBoostConfig()
    return lazy_boost_config
