#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2025  Ankit Patterson
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
class EtsyUser:
    user_id: int
    primary_email: str
    first_name: str
    last_name: str

    @staticmethod
    def from_dict(obj: Any) -> "EtsyUser":
        _user_id = int(obj.get("user_id"))
        _primary_email = str(obj.get("primary_email"))
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        return EtsyUser(_user_id, _primary_email, _first_name, _last_name)
