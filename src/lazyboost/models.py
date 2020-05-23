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
Models module contains the data structures and enums.
"""

from dataclasses import dataclass


@dataclass
class LazyEtsyConfig:
    etsy_token: str
    etsy_shop_id: int


@dataclass
class LazyFacebookConfig:
    facebook_token: str


@dataclass
class LazyConfig:
    etsy_config: LazyEtsyConfig
    facebook_config: LazyFacebookConfig
