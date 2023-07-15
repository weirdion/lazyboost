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
from datetime import datetime, timedelta
from typing import List

from aws_lambda_powertools import Logger

from lazyboost.clients import SecretManagerClient, ShopifyClient, EtsyClient
from lazyboost.models.shopify_product_model import ShopifyListing

logger = Logger()


class ListingHandler:
    def __init__(self) -> None:
        super().__init__()
        logger.info(f"Initializing ListingHandler")

        self.secret_manager_client: SecretManagerClient = SecretManagerClient()
        self.etsy_client: EtsyClient = EtsyClient()
        self.shopify_client: ShopifyClient = ShopifyClient()

        self.timestamp_to_check = datetime.now() - timedelta(days=2)
        self.updated_listings = self.shopify_client.get_new_products(self.timestamp_to_check)

        logger.info(f"{len(self.updated_listings)} updated listings detected")
        if len(self.updated_listings) is 0:
            return

        self._sync_new_listings_to_etsy()

    def _sync_new_listings_to_etsy(self):
        pass
