#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2024  Ankit Patterson
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

"""
constants module contains constant variables as static references across the project.
"""

# version of the application
__version__ = "1.0.0"

# cli top-level constants
CLI_NAME = "lazyboost"

# ETSY constants
ETSY_AUTH_URL = "https://www.etsy.com/oauth/connect"
ETSY_TOKEN_URL = "https://openapi.etsy.com/v3/public/oauth/token"
ETSY_AUTH_BASE_URL = "https://openapi.etsy.com/v3"
ETSY_API_BASE_URL = "https://openapi.etsy.com/v3/application/"

# Stamped.io constants
STAMPED_IO_BASE_URL = "https://stamped.io/api"

# Judge.me constants
JUDGE_ME_BASE_URL = "https://judge.me/api/v1"
JUDGE_ME_REVIEW_PLATFORM = "shopify"
JUDGE_ME_REVIEW_NAME_FORMAT = ""
JUDGE_ME_TIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

# Ref: https://www.shopuploader.com/tools/etsy-product-category-taxonomy
# Home & Living > Home Decor > Ornaments & Accents - #1023
# Home & Living > Home Decor > Wreaths & Door Hangers > Wreaths - #1930
# Home & Living > Home Decor > Wreaths & Door Hangers > Door Hangers - #1931
ETSY_TAXONOMY_ID_DICT = {
    "bows": 1023,
    "wreaths": 1930,
    "door hangers": 1931,
    "swags": 1931,
}

ETSY_SHIPPING_PROFILE_ID_DICT = {
    "Bows": 134564374043,
    "SmallWreath-FixedShipCost": 102504595187,
    "MediumWreath-FixedShipCost": 103663156927,
    "WreathUSFreeShip": 80936078610,
}

ETSY_SECTION_ID_DICT = {
    "Pet Lovers": 28736369,
    "Bows": 33135046,
    "Spring Collection": 28736387,
    "Summer Fun": 29625639,
    "Patriotic": 28736371,
    "Beautiful Everyday": 28736377,
    "Mom/Grandma Love": 28736361,
    "Fall Collection": 29194414,
    "Halloween": 29334572,
    "Winter and Christmas": 29975497,
}

ETSY_RETURN_POLICY_ID = 1097280283271

# SHOPIFY constants
