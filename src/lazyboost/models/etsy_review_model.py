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
from datetime import datetime, timezone
from typing import Any

from lazyboost.clients import EtsyClient
from lazyboost.models import EtsyOrder
from lazyboost.models.etsy_transaction_model import EtsyTransaction
from lazyboost.models.shopify_product_model import ShopifyProduct
from lazyboost.utilities import constants
from lazyboost.utilities.constants import JUDGE_ME_TIME_FORMAT


@dataclass
class EtsyReview:
    shop_id: int
    listing_id: int
    transaction_id: int
    buyer_user_id: int
    rating: int
    review: str
    language: str
    image_url: str
    create_timestamp: int
    created_timestamp: int
    update_timestamp: int
    updated_timestamp: int
    location: str = "United States"
    title: str = "Etsy Review"  # Etsy doesn't really do Review titles
    etsy_order: EtsyOrder = None
    etsy_transaction: EtsyTransaction = None

    @staticmethod
    def from_dict(obj: Any) -> "EtsyReview":
        _shop_id = int(obj.get("shop_id"))
        _listing_id = int(obj.get("listing_id"))
        _transaction_id = int(obj.get("transaction_id"))
        _buyer_user_id = int(obj.get("buyer_user_id"))
        _rating = int(obj.get("rating"))
        _review = str(obj.get("review"))
        _language = str(obj.get("language"))
        _image_url = str(obj.get("image_url_fullxfull"))
        _create_timestamp = int(obj.get("create_timestamp"))
        _created_timestamp = int(obj.get("created_timestamp"))
        _update_timestamp = int(obj.get("update_timestamp"))
        _updated_timestamp = int(obj.get("updated_timestamp"))
        return EtsyReview(
            _shop_id,
            _listing_id,
            _transaction_id,
            _buyer_user_id,
            _rating,
            _review,
            _language,
            _image_url,
            _create_timestamp,
            _created_timestamp,
            _update_timestamp,
            _updated_timestamp,
        )

    def get_additional_info(self, etsy_client: EtsyClient):
        transaction_response = etsy_client.get_shop_transaction(self.transaction_id)
        self.etsy_transaction = EtsyTransaction.from_dict(transaction_response)

        etsy_order_response = etsy_client.get_shop_receipt(self.etsy_transaction.receipt_id)
        self.etsy_order = EtsyOrder.from_dict(etsy_order_response)

    def to_stamped_io_review_dict(self, product_sku: str, shopify_product: ShopifyProduct) -> dict:
        review_dict = {
            "productId": shopify_product.id,
            "author": self.etsy_order.buyer.name,
            "email": self.etsy_order.buyer.email,
            "location": "United States",
            "reviewRating": self.rating,
            "reviewTitle": self.title,
            "reviewMessage": self.review if self.review else " ",
            "reviewRecommendProduct": True,
            "productSKU": product_sku,
            "productName": shopify_product.title,
            "productImageUrl": shopify_product.featured_image_url,
            "productUrl": shopify_product.online_store_url,
        }

        if self.image_url and self.image_url != "None":
            review_dict["photo0"] = self.image_url

        return review_dict

    def to_judge_me_review_dict(self, shopify_domain: str, product_id: int) -> dict:
        review_dict = {
            "shop_domain": shopify_domain,
            "platform": constants.JUDGE_ME_REVIEW_PLATFORM,
            "id": product_id,
            "name": self.etsy_order.buyer.name,
            "email": self.etsy_order.buyer.email,
            "rating": self.rating,
            "title": self.title,
            "body": self.review if self.review else "",
            "review_name_format": constants.JUDGE_ME_REVIEW_NAME_FORMAT,
        }

        if self.image_url and self.image_url != "None":
            review_dict["picture_urls"] = {"0": self.image_url}

        return review_dict

    def csv_row_judge_me(self, shopify_product: ShopifyProduct) -> list:
        return [
            self.title,
            self.review if self.review else " ",
            self.rating,
            datetime.fromtimestamp(self.created_timestamp, tz=timezone.utc).strftime(
                JUDGE_ME_TIME_FORMAT
            ),
            self.etsy_order.buyer.name,
            self.etsy_order.buyer.email,
            int(shopify_product.id.rsplit("/", 1)[-1]) if shopify_product else "",
            shopify_product.handle if shopify_product else "",
            "",  # reply is always empty since this is newer and unused
            self.image_url if self.image_url and self.image_url != "None" else "",
        ]

    @classmethod
    def csv_header_judge_me(cls) -> list:
        return [
            "title",
            "body",
            "rating",
            "review_date",
            "reviewer_name",
            "reviewer_email",
            "product_id",
            "product_handle",
            "reply",
            "picture_urls",
        ]
