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

from lazyboost.clients import EtsyClient
from lazyboost.models import EtsyTransaction
from lazyboost.models.etsy_user_model import EtsyUser


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
    etsy_transaction: EtsyTransaction = None
    etsy_user: EtsyUser = None

    @staticmethod
    def from_dict(obj: Any) -> 'EtsyReview':
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
        return EtsyReview(_shop_id, _listing_id, _transaction_id, _buyer_user_id, _rating, _review, _language,
                          _image_url, _create_timestamp, _created_timestamp, _update_timestamp, _updated_timestamp)

    def get_additional_info(self, etsy_client: EtsyClient):
        transaction_response = etsy_client.get_shop_transaction(self.transaction_id)
        self.etsy_transaction = EtsyTransaction.from_dict(transaction_response)

        buyer_response = etsy_client.get_uer_info(self.buyer_user_id)
        self.etsy_user = EtsyUser.from_dict(buyer_response)
