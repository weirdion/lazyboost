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
from datetime import datetime
from typing import Any, List


@dataclass
class ShopifyMinimalProduct:
    id: str
    title: str
    online_store_url: str
    handle: str
    featured_image_url: str

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyMinimalProduct":
        _id = str(obj.get("id"))
        _title = str(obj.get("title"))
        _online_store_url = str(obj.get("onlineStoreUrl"))
        _handle = str(obj.get("handle"))
        _featured_image_url = dict(obj.get("featuredImage"))["url"]
        return ShopifyMinimalProduct(_id, _title, _online_store_url, _handle, _featured_image_url)


@dataclass
class ShopifyNewVariant:
    id: str
    metafields: list
    updated_at: datetime

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyNewVariant":
        _id = str(obj.get("id"))
        _metafields = [m for m in obj.get("metafields").get("edges")]
        _updated_at = datetime.fromisoformat(str(obj.get("updatedAt")).replace('Z', '+00:00'))

        return ShopifyNewVariant(
            id=_id,
            metafields=_metafields,
            updated_at=_updated_at
        )


@dataclass
class ShopifyNewListing:
    id: str
    published_at: datetime
    has_only_default_variant: bool
    status: str
    updated_at: datetime
    total_inventory: int
    metafields: list
    variants: List[ShopifyNewVariant]

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyNewListing":
        _id = str(obj.get("id"))
        _published_at = datetime.fromisoformat(str(obj.get("publishedAt")).replace('Z', '+00:00'))
        _has_only_default_variant = bool(obj.get("hasOnlyDefaultVariant"))
        _status = str(obj.get("status"))
        _updated_at = datetime.fromisoformat(str(obj.get("updatedAt")).replace('Z', '+00:00'))
        _total_inventory = int(obj.get("totalInventory"))
        _metafields = [m for m in obj.get("metafields").get("edges")]
        _variants = [ShopifyNewVariant.from_dict(v["node"]) for v in obj.get("variants").get("edges")]

        return ShopifyNewListing(
            id=_id,
            published_at=_published_at,
            has_only_default_variant=_has_only_default_variant,
            status=_status,
            updated_at=_updated_at,
            metafields=_metafields,
            variants=_variants
        )
