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
import os
from datetime import datetime, timedelta

from aws_lambda_powertools import Logger

from lazyboost.clients import SecretManagerClient, ShopifyClient, EtsyClient

logger = Logger()


class ListingHandler:
    def __init__(self) -> None:
        super().__init__()
        logger.info(f"Initializing ListingHandler")

        self.secret_manager_client: SecretManagerClient = SecretManagerClient()
        self.etsy_client: EtsyClient = EtsyClient()
        self.shopify_client: ShopifyClient = ShopifyClient()

        self.sync_interval_listings = int(os.getenv("SYNC_INTERVAL_LISTINGS_MIN", 17))
        self.timestamp_to_check = datetime.now() - timedelta(minutes=self.sync_interval_listings)
        self.updated_listings = self.shopify_client.get_new_products(self.timestamp_to_check)

        logger.info(f"{len(self.updated_listings)} updated listings detected")
        if len(self.updated_listings) == 0:
            return

        self._sync_new_listings_to_etsy()

    def _sync_new_listings_to_etsy(self):
        for listing in self.updated_listings:
            for variant in listing.variants:
                if (
                    variant.updated_at.timestamp() >= self.timestamp_to_check.timestamp()
                    and variant.inventory_quantity > 0
                ):
                    etsy_listing_dict = listing.to_etsy_listing(variant)
                    logger.info(f"Creating new listing: {etsy_listing_dict}")
                    response = self.etsy_client.create_listing(etsy_listing_dict)
                    logger.info(f"Successfully created new listing: {response['listing_id']}")
                    logger.info(f"Etsy listing response: {response}")
                else:
                    logger.info(f"Listing {listing.id} variant {variant.id} is too old to sync.")

    def _get_shipping_profile_ids(self):
        response = self.etsy_client.get_shipping_profiles()
        shipping_profile_ids = {
            shipping_profile["title"]: shipping_profile["shipping_profile_id"]
            for shipping_profile in response["results"]
        }
        return shipping_profile_ids

    def _get_shop_section_ids(self):
        response = self.etsy_client.get_shop_sections()
        shop_section_ids = {
            section["title"]: section["shop_section_id"] for section in response["results"]
        }
        return shop_section_ids

    def _get_return_policy_ids(self):
        response = self.etsy_client.get_return_policies()
        return_policy_ids = {
            return_policy["title"]: return_policy["return_policy_id"]
            for return_policy in response["results"]
        }
        return return_policy_ids
