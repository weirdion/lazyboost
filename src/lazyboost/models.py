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
Models module contains the data structures and enums.
"""

from dataclasses import dataclass
from enum import auto

from lazyboost.utility_base import BaseEnum


class LazyBoostConfig:
    """
    LazyBoostConfig class handles the structure and contents of the lazy_boost.json config.
    """


@dataclass
class LazyEtsyConfig:
    """
    LazyEtsyConfig is a data class that holds the Etsy elements needed to access and parse the
    Etsy API.
    """
    etsy_token: str
    etsy_shop_id: str


@dataclass
class LazyConfig:
    """
    LazyConfig is a data class that holds all platform based API objects.
    """
    etsy_config: LazyEtsyConfig


class EtsyListingState(BaseEnum):
    """
    EtsyListingState is an enum class that extends BaseEnum class to provide all supported
    Listing states provided by Etsy API.
    """
    ACTIVE = auto()
    REMOVED = auto()
    SOLD_OUT = auto()
    EXPIRED = auto()
    DRAFT = auto()
    PRIVATE = auto()
    UNAVAILABLE = auto()


@dataclass
class EtsyListing:
    """
    EtsyListing is a data class that contains all relevant entries returned by Etsy API that we
    need to parse.
    NOTE: This is not exhaustive list, there are fields returned by the API that are discarded.
    """
    listing_id: int
    state: EtsyListingState
    user_id: int
    title: str
    description: str
    price: float
    currency_code: str
    quantity: int
    sku: str
    tags: list
    materials: list
    occasion: str
    taxonomy_path: list
    primary_image: str = None
    secondary_images: list = None
    is_private: bool = False
