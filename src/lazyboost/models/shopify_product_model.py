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
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

from lazyboost.utilities.constants import ETSY_RETURN_POLICY_ID
from lazyboost.utilities.utility_etsy import (
    format_materials_to_list,
    get_section_id,
    get_shipping_profile_id,
    get_taxonomy_by_product_type,
)

DIMENSIONS_REGEX = (
    r"^.*(\d{2})\s+inches\s+in\s+height,\s+(\d{1,2})\s+inches\s+in\s+width\s+"
    r"and\s+(\d{1,2})\s+inches\s+in\s+depth.*$"
)


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
class ShopifyVariant:
    id: str
    price: str
    sku: str
    inventory_quantity: int
    metafields: list
    updated_at: datetime

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyVariant":
        _id = str(obj.get("id"))
        _price = str(obj.get("price"))
        _sku = str(obj.get("sku"))
        _inventory_quantity = int(obj.get("inventoryQuantity"))
        _metafields = [m for m in obj.get("metafields").get("edges")]
        _updated_at = datetime.fromisoformat(str(obj.get("updatedAt")).replace("Z", "+00:00"))

        return ShopifyVariant(
            id=_id,
            price=_price,
            sku=_sku,
            inventory_quantity=_inventory_quantity,
            metafields=_metafields,
            updated_at=_updated_at,
        )


@dataclass
class ShopifyListing:
    id: str
    title: str
    description: str
    product_type: str
    status: str
    updated_at: datetime
    total_inventory: int
    metafields: list
    variants: List[ShopifyVariant]
    tags: list

    @staticmethod
    def from_dict(obj: Any) -> "ShopifyListing":
        _id = str(obj.get("id"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _product_type = str(obj.get("productType"))
        _status = str(obj.get("status"))
        _updated_at = datetime.fromisoformat(str(obj.get("updatedAt")).replace("Z", "+00:00"))
        _total_inventory = int(obj.get("totalInventory"))
        _metafields = [m for m in obj.get("metafields").get("edges")]
        _variants = [ShopifyVariant.from_dict(v["node"]) for v in obj.get("variants").get("edges")]
        _tags = list(obj.get("tags"))

        return ShopifyListing(
            id=_id,
            title=_title,
            description=_description,
            product_type=_product_type,
            status=_status,
            updated_at=_updated_at,
            total_inventory=_total_inventory,
            metafields=_metafields,
            variants=_variants,
            tags=_tags,
        )

    def to_etsy_listing(self, variant: ShopifyVariant) -> dict:
        """
        Converts ShopifyListing to EtsyListing
        """

        return {
            "title": self.title,
            "description": f"{self.description}\n\n{', '.join(self.tags)}",
            "price": float(variant.price),
            "quantity": variant.inventory_quantity,
            "sku": variant.sku,
            "who_made": "i_did",
            "when_made": "2020_2023",
            "taxonomy_id": get_taxonomy_by_product_type(self.product_type),
            "should_auto_renew": False if self.product_type.casefold() == "bows" else True,
            "is_taxable": True,
            "type": "physical",
            "return_policy_id": ETSY_RETURN_POLICY_ID,
            "shipping_profile_id": get_shipping_profile_id(self.product_type, variant.price),
            "shop_section_id": get_section_id(self.tags),
            "materials": format_materials_to_list(self.description),
        }
