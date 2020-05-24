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
from enum import auto

from lazyboost.utility_base import BaseEnum


@dataclass
class LazyEtsyConfig:
    etsy_token: str
    etsy_shop_id: str


@dataclass
class LazyFacebookConfig:
    facebook_token: str


@dataclass
class LazyConfig:
    etsy_config: LazyEtsyConfig
    facebook_config: LazyFacebookConfig


class EtsyListingState(BaseEnum):
    ACTIVE = auto()
    REMOVED = auto()
    SOLD_OUT = auto()
    EXPIRED = auto()
    DRAFT = auto()
    PRIVATE = auto()
    UNAVAILABLE = auto()


@dataclass
class EtsyListing:
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


class FacebookListingAvailability(BaseEnum):
    IN_STOCK = "in stock"
    OUT_OF_STOCK = "out of stock"
    AVAILABLE_FOR_ORDER = "available for order"
    PRE_ORDER = "preorder"
    DISCONTINUED = "discontinued"


@dataclass
class FacebookListing:
    id: str
    title: str
    description: str
    availability: FacebookListingAvailability
    price: str
    image_link: str
    additional_image_link: str
    inventory: int
    condition: str = "new"
    brand: str = "AmourFrontDoor"
    age_group: str = "adult"
    google_product_category: str = "6267"
    commerce_tax_category: str = "FB_HMGN_DCOR"
    shipping: str = "US::Air:0.0 USD"
