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
log module handles the configuration and generation of a standard logger
"""

import logging
from logging.handlers import RotatingFileHandler
import sys

from lazyboost import path_handler

LOG_CLI_FORMAT = '%(message)s'
LOG_SHORT_FORMAT = '[%(asctime)s] - %(levelname)s: %(message)s'
LOG_LONG_FORMAT = '[%(asctime)s] - %(levelname)s - %(name)s: %(message)s'
LOG_DATE_LONG_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_DATE_SHORT_FORMAT = "%I:%M:%S %p"

# Keep only one shared instance of CONSOLE_LOGGER to avoid duplicate stream output
CONSOLE_LOGGER = None


def create_logger(module_name):
    """
    Function that generates a logger for the module_name passed in and the the static LOG_CONFIG.
    :return: logging, log object.
    """
    regular_log_file, error_log_file = path_handler.get_log_file_paths()
    logger = logging.getLogger(module_name)
    info_log_handler = RotatingFileHandler(
        filename=regular_log_file,
        maxBytes=5 * (1024 ** 2),
        backupCount=5,
    )
    info_log_handler.setFormatter(logging.Formatter(LOG_SHORT_FORMAT, datefmt=LOG_DATE_LONG_FORMAT))
    info_log_handler.setLevel(logging.DEBUG)

    error_log_handler = RotatingFileHandler(
        filename=error_log_file,
        maxBytes=5 * (1024 ** 2),
        backupCount=5,
    )
    error_log_handler.setFormatter(logging.Formatter(LOG_LONG_FORMAT, datefmt=LOG_DATE_LONG_FORMAT))
    error_log_handler.setLevel(logging.ERROR)

    logger.addHandler(info_log_handler)
    logger.addHandler(error_log_handler)

    logger.setLevel(logging.INFO)

    return logger


def console_logger():
    """
    Function that generates a logger that handles console prints.
    :return: logging, log object.
    """
    global CONSOLE_LOGGER
    if not CONSOLE_LOGGER:
        logger = logging.getLogger('cli')

        log_handler = logging.StreamHandler(stream=sys.stdout)
        log_handler.setFormatter(logging.Formatter(LOG_CLI_FORMAT, datefmt=LOG_DATE_SHORT_FORMAT))
        log_handler.setLevel(logging.DEBUG)

        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)
        CONSOLE_LOGGER = logger

    return CONSOLE_LOGGER


def combined_log(file_logger: logging, cli_logger: logging, logging_level: int, message: str):
    """
    Function that logs the given message to both file_logger as well as cli_logger as the given
    logging_level.
    :param file_logger: logging, Instance of the logging object.
    :param cli_logger: logging, Instance of the logging object.
    :param logging_level: int, logging level to be used.
    :param message: str, message that will be printed to both logging objects.
    """
    file_logger.log(logging_level, message)
    cli_logger.log(logging_level, message)
