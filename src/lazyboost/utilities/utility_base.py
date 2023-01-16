#   LazyBoost
#   Copyright (C) 2023  Ankit Sadana
#  #
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
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
utility base module contains essential helper functions.

NOTE: Things that require utility_base to initialize (like logging) should be avoided in this
class to avoid circular dependencies.
"""
import enum
import json
import os
import sys
from datetime import datetime

from dotenv import dotenv_values

from lazyboost.models import BaseEnum


def prompt_user_yes_no(question: str) -> bool:
    """
    Function that prompts user the question from the argument for a Yes/No answer.
    :param question: str, question the user will be prompted for.
    :return: bool, True if user answers Yes, False otherwise.
    """
    while (answer := input(f"{question} (y/n): ").lower()) not in {"y", "yes", "n", "no"}:
        print("Invalid input.")

    if answer[0] == "y":
        return True

    return False


def get_os_prefix():
    """
    Function to return the OS path prefix.
    If the install is without containment, '/' is returned.
    If the install is contained, i.e., within pipenv or venv, sys.prefix is returned.
    :return: str, prefix string.
    """

    if _is_pipenv_active():
        _os_prefix = sys.prefix + "/"
    else:
        _os_prefix = '/'

    return _os_prefix


def get_path(file_path):
    """
    Function that uses get_os_prefix and joins file_path
    :param file_path: path that needs to be sanitized.
    :return: str, absolute path
    """
    prefix = get_os_prefix()
    # Ensure that path is expanded, e.g. '~'
    file_path = os.path.expanduser(file_path)

    # If path is already correct, return as is
    if file_path.startswith(prefix):
        return file_path

    # in pipenv
    if prefix != '/':

        # if file_path is already absolute path, os.path.join won't work
        if file_path.startswith('/'):
            return prefix + file_path

    return os.path.join(prefix, file_path)


def _is_pipenv_active():
    """
    Function that checks sys if pipenv is active.
    :return: bool, True if pipenv is active, False if not.
    """
    return os.getenv('VIRTUAL_ENV')


def convert_to_json_str(obj, indent=None) -> str:
    """
    Function that uses an object of a custom class, and recursively uses __dict__ on it using json.
    :param obj: object of any class.
    :param indent: indentation to be used in json string to make it readable, default=None
    :return: str, in json format
    """

    def _convert_obj_to_json(object_var):
        """
        Inner method that checks if the object_var is of type Enum.
        If type Enum, print custom json format.
        If not Enum, print dict.
        :param object_var: member variable of obj
        :return: json string representation of the object_var.
        """
        if isinstance(object_var, BaseEnum):
            return f"{object_var.value.lower()}"
        return object_var.__dict__

    return json.dumps(obj, default=_convert_obj_to_json, indent=indent)


def get_timestamp() -> str:
    """
    Function that gets the current time and returns formatted version of it.
    :return: str, current date/time stamp
    """
    # current date and time
    now = datetime.now()
    return now.strftime("%Y%m%d%H%M%S")


def get_dotenv_variables() -> dict:
    """
    Function that uses python-dotenv to read from .env file and return dict.
    :return dict, key-value pairs from .env file
    """
    return dotenv_values(".env")
