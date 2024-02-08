#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Patterson
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
from typing import Any, Optional


@dataclass
class EtsyBuyer:
    name: str
    email: Optional[str]
    address_first_line: str
    address_second_line: str
    address_city: str
    address_state: str
    address_zip: str
    address_country_code: str
    user_id: str

    @staticmethod
    def from_dict(obj: Any) -> "EtsyBuyer":
        _name = str(obj.get("name"))
        _email = obj.get("buyer_email", None)
        _address_first_line = str(obj.get("first_line")).rstrip()
        _address_second_temp = str(obj.get("second_line"))
        _address_second_line = (
            _address_second_temp.rstrip()
            if _address_second_temp and _address_second_temp != "None"
            else ""
        )
        _address_city = str(obj.get("city")).rstrip()
        _address_state = str(obj.get("state"))
        _address_zip = str(obj.get("zip"))
        _address_country_code = str(obj.get("country_iso"))
        _buyer_user_id = str(obj.get("buyer_user_id"))
        return EtsyBuyer(
            name=_name,
            email=_email,
            address_first_line=_address_first_line,
            address_second_line=_address_second_line,
            address_city=_address_city,
            address_state=_address_state,
            address_zip=_address_zip,
            address_country_code=_address_country_code,
            user_id=_buyer_user_id,
        )

    def to_shopify_address(self) -> dict:
        (buyer_name1, buyer_name2) = self.name.rsplit(" ", 1)
        return {
            "address1": self.address_first_line,
            "address2": self.address_second_line,
            "city": self.address_city,
            "first_name": buyer_name1,
            "last_name": buyer_name2,
            "zip": self.address_zip,
            "name": self.name,
            "province_code": self.address_state,
            "country_code": self.address_country_code,
        }

    @property
    def etsy_tag(self) -> str:
        return f"ETSY_BUYER_ID_{self.user_id}"
