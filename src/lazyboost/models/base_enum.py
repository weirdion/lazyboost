#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2025  Ankit Patterson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import enum


class BaseEnum(enum.Enum):
    """
    BaseEnum class extends enum.Enum.
    This class provides a base for other Enum classes in this project.
    """

    # pylint: disable=no-self-argument,unused-argument
    def _generate_next_value_(name, start, count, last_values):
        """
        Inner method is overridden from parent class.
        This is done so as to use string value (in lower case) with enum.auto()
        :return: str, lower-case representation of the member name.
        """
        return str(name).lower()

    @classmethod
    def member_names(cls):
        """
        Class method that returns a list of the class' member names.
        :return: list, member names.
        """
        return list(cls.__members__.keys())

    @classmethod
    def member_values(cls):
        """
        Class method that returns a list of the class' member values.
        :return: list, member values.
        """
        return list(map(lambda x: x.value, cls.__members__.values()))

    @classmethod
    def check_if_member(cls, name: str):
        """
        Class method that checks if the `name` str value is present in the member_names.
        :param name: str, value to be compared against member names.
        :return: bool, True if string value is a valid member name, false otherwise.
        """
        return name.lower() in cls.member_values()
