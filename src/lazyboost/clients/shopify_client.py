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
#
import shopify

from lazyboost.log import console_logger
from lazyboost.models.buyer_model import Buyer
from lazyboost.models.shopify_customer_model import ShopifyCustomer

log = console_logger()


class ShopifyClient:
    def __init__(self, dotenv_variables: dict):
        self.shop_url = dotenv_variables["SHOPIFY_TEST_SHOP_URL"]
        self.api_version = dotenv_variables["SHOPIFY_API_VERSION"]
        self.api_key = dotenv_variables["SHOPIFY_TEST_API_KEY"]
        self.client_secret = dotenv_variables["SHOPIFY_TEST_CLIENT_SECRET"]
        self.access_token = dotenv_variables["SHOPIFY_TEST_ACCESS_TOKEN"]
        log.info("Initiating Shopify session")
        self.session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(self.session)

    def __del__(self):
        log.debug("Clearing shopify session")
        shopify.ShopifyResource.clear_session()

    def is_existing_customer(self, buyer: Buyer) -> ShopifyCustomer | None:
        response = shopify.Customer.search(
            session=self.session,
            query=f"email:{buyer.email}"
        )
        if not response:
            return None
        return ShopifyCustomer.from_dict(response[0].attributes)

    # is_existing_customer
    # yes - update needed? update or not, keep id
    # ensure that the right address is used if new address is used - maybe default the new one
    # no, create new customer

    # use customer id or new customer info to create an order
    # mark it paid
    # add a tag to signify the lazyboost import
    # ensure gift message and gift pref is carried
    # ensure discounts are carried
    # ensure shipping, tax and totals are carried
