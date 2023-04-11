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

# Ref: https://www.shopuploader.com/tools/etsy-product-category-taxonomy
# Home & Living > Home Decor > Ornaments & Accents - #1023
# Home & Living > Home Decor > Wreaths & Door Hangers > Wreaths - #1930
# Home & Living > Home Decor > Wreaths & Door Hangers > Door Hangers - #1931
ETSY_TRANSACTION_ID_DICT = {"Bows": 1023, "Wreaths": 1930, "Door Hangers": 1931, "Swags": 1931}

# SHOPIFY constants
