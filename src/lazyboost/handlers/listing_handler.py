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

from lazyboost.clients import SecretManagerClient, ShopifyClient
from lazyboost.models.shopify_product_model import ShopifyNewListing

logger = Logger()


class ListingHandler:
    def __init__(self) -> None:
        super().__init__()
        logger.info(f"Initializing ListingHandler")

        self.secret_manager_client: SecretManagerClient = SecretManagerClient()
        # self.etsy_client: EtsyClient = EtsyClient()
        self.shopify_client: ShopifyClient = ShopifyClient()

        self.timestamp_to_check = datetime.now() - timedelta(days=2)
        new_products = self.shopify_client.get_new_products(self.timestamp_to_check)

        self.product_ids = []
        self.variant_ids = []
        self._parse_new_products(new_products)

        if self.product_ids or self.variant_ids:
            logger.info(f"New listings detected",
                        product_ids=self.product_ids, variant_ids=self.variant_ids
                        )
            self._sync_new_listings_to_etsy()

    def _parse_new_products(self, new_products: List[ShopifyNewListing]):

        for p in new_products:
            if p.total_inventory < 1:
                logger.warning("Skipping product, inventory was 0", product=p)
                continue

            if not p.has_only_default_variant:
                for v in p.variants:
                    if v.updated_at > self.timestamp_to_check:
                        self.variant_ids.append(v.id)
            else:
                if p.updated_at > self.timestamp_to_check:
                    self.product_ids.append(p.id)

    def _sync_new_listings_to_etsy(self):
        pass
