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
import os
import sys

LOG_DATE_SHORT_FORMAT = "%I:%M:%S %p"
LOG_LONG_FORMAT = "[%(asctime)s] - %(levelname)s - %(name)s: %(message)s"

# Keep only one shared instance of CONSOLE_LOGGER to avoid duplicate stream output
CONSOLE_LOGGER = None


def console_logger() -> logging.Logger:
    """
    Function that generates a logger to handles console output.
    :return: Logger object
    """
    global CONSOLE_LOGGER
    if not CONSOLE_LOGGER:
        logger = logging.getLogger("lazyboost")

        # Evaluate env variable "DEBUG" if available
        is_debug_enabled = os.getenv("DEBUG", "False").lower() in ("true", "1")
        log_level = logging.DEBUG if is_debug_enabled else logging.INFO

        log_handler = logging.StreamHandler(stream=sys.stdout)
        log_handler.setFormatter(logging.Formatter(LOG_LONG_FORMAT,
                                                   datefmt=LOG_DATE_SHORT_FORMAT))
        log_handler.setLevel(log_level)

        logger.addHandler(log_handler)
        logger.setLevel(log_level)
        CONSOLE_LOGGER = logger

        logger.debug("DEBUG logging enabled!")

    return CONSOLE_LOGGER
