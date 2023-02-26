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
from dataclasses import dataclass
from typing import List

from lazyboost.models.buyer_model import Buyer


@dataclass
class EtsyTransaction:
    product_sku: str
    product_quantity: int
    product_price: float
    product_shipping_cost: float


@dataclass
class EtsyOrder:
    receipt_id: int
    buyer: Buyer
    message_from_buyer: str
    is_shipped: bool
    create_timestamp: int
    update_timestamp: int
    is_gift: bool
    gift_message: str
    sale_total_cost: float
    sale_subtotal_cost: float
    sale_shipping_cost: float
    sale_tax_cost: float
    sale_discount_cost: float
    transactions: List[EtsyTransaction]
