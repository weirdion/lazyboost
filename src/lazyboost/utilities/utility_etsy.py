#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Sadana
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
from lazyboost.utilities.constants import ETSY_TAXONOMY_ID_DICT


def get_float_amount(price_dict: dict) -> float:
    return price_dict["amount"] / price_dict["divisor"]


def get_taxonomy_by_product_type(product_type: str) -> str:
    product_type = product_type.casefold()
    return ETSY_TAXONOMY_ID_DICT[product_type]
