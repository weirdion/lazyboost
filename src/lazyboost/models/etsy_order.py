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
from dataclasses import dataclass
from typing import Any, List

from lazyboost.models.etsy_buyer_model import EtsyBuyer
from lazyboost.utilities.utility_etsy import get_float_amount


@dataclass
class EtsyTransaction:
    product_sku: str
    product_quantity: int
    product_price: float
    product_shipping_cost: float

    @staticmethod
    def from_dict(obj: Any) -> "EtsyTransaction":
        _product_sku = str(obj.get("sku"))
        _product_quantity = int(obj.get("quantity"))
        _product_price = float(get_float_amount(obj.get("price")))
        _product_shipping_cost = float(get_float_amount(obj.get("shipping_cost")))
        return EtsyTransaction(
            _product_sku, _product_quantity, _product_price, _product_shipping_cost
        )


@dataclass
class EtsyOrder:
    receipt_id: int
    buyer: EtsyBuyer
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

    @staticmethod
    def from_dict(obj: Any) -> "EtsyOrder":
        _receipt_id = int(obj.get("receipt_id"))
        _buyer = EtsyBuyer.from_dict(obj)
        _message_from_buyer = str(obj.get("message_from_buyer"))
        _is_shipped = bool(obj.get("is_shipped"))
        _create_timestamp = int(obj.get("create_timestamp"))
        _update_timestamp = int(obj.get("update_timestamp"))
        _is_gift = bool(obj.get("is_gift"))
        _gift_message = str(obj.get("gift_message"))
        _sale_total_cost = float(get_float_amount(obj.get("grandtotal")))
        _sale_subtotal_cost = float(get_float_amount(obj.get("subtotal")))
        _sale_shipping_cost = float(get_float_amount(obj.get("total_shipping_cost")))
        _sale_tax_cost = float(get_float_amount(obj.get("total_tax_cost")))
        _sale_discount_cost = float(get_float_amount(obj.get("discount_amt")))
        _transactions = [EtsyTransaction.from_dict(y) for y in obj.get("transactions")]
        return EtsyOrder(
            _receipt_id,
            _buyer,
            _message_from_buyer,
            _is_shipped,
            _create_timestamp,
            _update_timestamp,
            _is_gift,
            _gift_message,
            _sale_total_cost,
            _sale_subtotal_cost,
            _sale_shipping_cost,
            _sale_tax_cost,
            _sale_discount_cost,
            _transactions,
        )
