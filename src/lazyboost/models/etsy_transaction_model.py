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
from typing import Any


@dataclass
class EtsyTransaction:
    transaction_id: int
    title: str
    description: str
    seller_user_id: int
    buyer_user_id: int
    receipt_id: int
    listing_id: int
    transaction_type: str
    product_id: int
    sku: str

    @staticmethod
    def from_dict(obj: Any) -> "EtsyTransaction":
        _transaction_id = int(obj.get("transaction_id"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _seller_user_id = int(obj.get("seller_user_id"))
        _buyer_user_id = int(obj.get("buyer_user_id"))
        _receipt_id = int(obj.get("receipt_id"))
        _listing_id = int(obj.get("listing_id"))
        _transaction_type = str(obj.get("transaction_type"))
        _product_id = int(obj.get("product_id"))
        _sku = str(obj.get("sku"))
        return EtsyTransaction(
            _transaction_id,
            _title,
            _description,
            _seller_user_id,
            _buyer_user_id,
            _receipt_id,
            _listing_id,
            _transaction_type,
            _product_id,
            _sku,
        )
