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
from typing import Any


@dataclass
class EtsyBuyer:
    name: str
    email: str
    address_first_line: str
    address_second_line: str
    address_city: str
    address_state: str
    address_zip: str
    address_country_code: str

    @staticmethod
    def from_dict(obj: Any) -> "EtsyBuyer":
        _name = str(obj.get("name"))
        _email = str(obj.get("buyer_email"))
        _address_first_line = str(obj.get("first_line"))
        _address_second_temp = str(obj.get("second_line"))
        _address_second_line = (
            _address_second_temp if _address_second_temp and _address_second_temp != "None" else ""
        )
        _address_city = str(obj.get("city"))
        _address_state = str(obj.get("state"))
        _address_zip = str(obj.get("zip"))
        _address_country_code = str(obj.get("country_iso"))
        return EtsyBuyer(
            _name,
            _email,
            _address_first_line,
            _address_second_line,
            _address_city,
            _address_state,
            _address_zip,
            _address_country_code,
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
