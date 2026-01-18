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
#

from dataclasses import asdict, dataclass
from typing import Any, List

from lazyboost.models.etsy_buyer_model import EtsyBuyer
from lazyboost.utilities.utility_generic import is_string_different


@dataclass
class Address:
    id: int
    customer_id: int
    first_name: str
    last_name: str
    company: str
    address1: str
    address2: str
    city: str
    province: str
    country: str
    zip: str
    phone: str
    name: str
    province_code: str
    country_code: str
    country_name: str
    default: bool

    def is_billing_address_same(self, etsy_buyer: EtsyBuyer) -> bool:
        (buyer_name1, buyer_name2) = etsy_buyer.name.rsplit(" ", 1)
        if (
            is_string_different(buyer_name1, self.first_name)
            or is_string_different(buyer_name2, self.last_name)
            or is_string_different(etsy_buyer.address_first_line, self.address1)
            or is_string_different(etsy_buyer.address_second_line, self.address2)
            or is_string_different(etsy_buyer.address_city, self.city)
            or is_string_different(etsy_buyer.address_state, self.province_code)
        ):
            return False
        return True

    @staticmethod
    def from_dict(obj: Any) -> "Address":
        _address_obj = obj.attributes
        _id = int(_address_obj.get("id"))
        _customer_id = int(_address_obj.get("customer_id"))
        _first_name = str(_address_obj.get("first_name"))
        _last_name = str(_address_obj.get("last_name"))
        _company = str(_address_obj.get("company"))
        _address1 = str(_address_obj.get("address1"))
        _address2 = str(_address_obj.get("address2"))
        if _address2 == "None":
            _address2 = ""
        _city = str(_address_obj.get("city"))
        _province = str(_address_obj.get("province"))
        _country = str(_address_obj.get("country"))
        _zip = str(_address_obj.get("zip"))
        _phone = str(_address_obj.get("phone"))
        _name = str(_address_obj.get("name"))
        _province_code = str(_address_obj.get("province_code"))
        _country_code = str(_address_obj.get("country_code"))
        _country_name = str(_address_obj.get("country_name"))
        _default = bool(_address_obj.get("default"))
        return Address(
            _id,
            _customer_id,
            _first_name,
            _last_name,
            _company,
            _address1,
            _address2,
            _city,
            _province,
            _country,
            _zip,
            _phone,
            _name,
            _province_code,
            _country_code,
            _country_name,
            _default,
        )

    def to_order_dict(self) -> dict:
        return {
            k: str(v)
            for k, v in asdict(self).items()
            if k and k not in ["id", "customer_id", "default"]
        }


@dataclass
class ShopifyCustomer:
    id: int
    email: str
    first_name: str
    last_name: str
    orders_count: int
    state: str
    total_spent: str
    last_order_id: str
    tags: str
    last_order_name: str
    currency: str
    phone: str
    addresses: List[Address]
    default_address: Address

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyCustomer":
        _id = int(obj.get("id"))
        _email = str(obj.get("email"))
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        _orders_count = int(obj.get("orders_count"))
        _state = str(obj.get("state"))
        _total_spent = str(obj.get("total_spent"))
        _last_order_id = str(obj.get("last_order_id"))
        _tags = str(obj.get("tags")) if obj.get("tags") else ""
        _last_order_name = str(obj.get("last_order_name"))
        _currency = str(obj.get("currency"))
        _phone = str(obj.get("phone"))
        _addresses = (
            [Address.from_dict(y) for y in obj.get("addresses")] if obj.get("addresses") else []
        )
        _default_address = (
            Address.from_dict(obj.get("default_address")) if obj.get("default_address") else None
        )
        return ShopifyCustomer(
            _id,
            _email,
            _first_name,
            _last_name,
            _orders_count,
            _state,
            _total_spent,
            _last_order_id,
            _tags,
            _last_order_name,
            _currency,
            _phone,
            _addresses,
            _default_address,
        )
