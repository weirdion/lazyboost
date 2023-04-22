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
class ShopifyProduct:
    id: str
    title: str
    online_store_url: str
    handle: str
    featured_image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyProduct":
        _id = str(obj.get("id"))
        _title = str(obj.get("title"))
        _online_store_url = str(obj.get("onlineStoreUrl"))
        _handle = str(obj.get("handle"))
        _featured_image_url = dict(obj.get("featuredImage"))["url"]
        return ShopifyProduct(_id, _title, _online_store_url, _handle, _featured_image_url)
