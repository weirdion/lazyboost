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
constants module contains constant variables as static references across the project.
"""

# version of the application
__version__ = "0.0.1"

# cli top-level constants
CLI_NAME = "lazyboost"
CLI_COMMAND_BACKUP = "backup"
CLI_COMMAND_RESTORE = "restore"

# log constants
LOG_DIR = f'.local/share/{CLI_NAME}'
LOG_DEFAULT_NAME = f'{CLI_NAME}.log'
LOG_ERROR_NAME = f'{CLI_NAME}-error.log'

# config constants
CONFIG_DIR = f'.config/{CLI_NAME}'
CONFIG_PATH = f'{CLI_NAME}.json'
CONFIG_BACKUP_SUFFIX = '.backup'

# User data constants
USER_DATA = f'Downloads/{CLI_NAME}'
FILE_PREFIX = f'{CLI_NAME}-'
IMPORT_FACEBOOK_FILE_NAME = f'{CLI_NAME}-facebook-import-%s.csv'
