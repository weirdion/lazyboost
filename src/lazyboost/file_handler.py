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
FileHandler module that handles ability to write to file in different formats.
"""

import csv
import logging
import os

from lazyboost import constants, log, path_handler, utility_base
from lazyboost.models import FacebookListing

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def write_facebook_import_csv_file(facebook_listings: list) -> bool:
    """
    Function that takes list of FacebookListing and writes a CSV file with it
    :param facebook_listings: list(FacebookListing)
    :return: bool, True if the file was successfully written, False otherwise.
    """
    if not facebook_listings or not isinstance(facebook_listings[1], FacebookListing):
        log.combined_log(_logger, _cli_logger, logging.ERROR,
                         "Invalid facebook listings received, failed to generate import csv file.")
        return False

    file_name = constants.IMPORT_FACEBOOK_FILE_NAME % utility_base.get_timestamp()
    file_path = os.path.join(path_handler.get_user_data_dir(), file_name)
    file_written = False
    field_names = list(facebook_listings[1].__dict__.keys())

    try:
        with open(file_path, 'w') as file:
            log.combined_log(_logger, _cli_logger, logging.INFO,
                             f'Beginning to write Facebook import CSV file...')
            csv_writer = csv.DictWriter(file, fieldnames=field_names, delimiter="\t")
            for listing in facebook_listings:
                csv_writer.writerow(listing.__dict__)
            file_written = True
            log.combined_log(_logger, _cli_logger, logging.INFO,
                             f'Successfully generated Facebook import CSV file at {file_path}.')
    except IOError as err:
        log.combined_log(_logger, _cli_logger, logging.INFO,
                         f'Failed to write config file: {file_path}, reason: {err}')

    return file_written
