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
import json

import shopify

from lazyboost.log import console_logger
from lazyboost.models.etsy_buyer_model import EtsyBuyer
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

    def is_existing_customer(self, etsy_buyer: EtsyBuyer) -> ShopifyCustomer | None:
        response = shopify.Customer.search(
            session=self.session,
            query=f"email:{etsy_buyer.email}"
        )
        if not response:
            return None
        return ShopifyCustomer.from_dict(response[0].attributes)

    def update_customer(self, etsy_buyer: EtsyBuyer, shopify_customer: ShopifyCustomer) -> None:
        default_address = shopify_customer.default_address

        is_existing_address = default_address.is_billing_address_same(etsy_buyer)
        if not is_existing_address:
            for address in shopify_customer.addresses:
                if address.is_billing_address_same(etsy_buyer):
                    res = shopify.Customer.put(f"{shopify_customer.id}/addresses/{address.id}/default",
                                               body=json.dumps({
                                                   "address_id": address.id,
                                                   "customer_id": shopify_customer.id
                                               }).encode("utf-8"))
                    log.info(f"updating customer: {shopify_customer.id} default address: {res.code}")
                    is_existing_address = True
                    break

        # Address not found in any existing addresses
        if not is_existing_address:
            self.add_customer_address(etsy_buyer, shopify_customer.id)

    def add_customer_address(self, etsy_buyer: EtsyBuyer, shopify_customer_id: int) -> None:
        log.info(f"Adding new address for {shopify_customer_id}")

        (buyer_name1, buyer_name2) = etsy_buyer.name.rsplit(" ", 1)
        response = shopify.Customer.post(f"{shopify_customer_id}/addresses",
                                         body=json.dumps({
                                             "address": {
                                                 "address1": etsy_buyer.address_first_line,
                                                 "address2": etsy_buyer.address_second_line,
                                                 "city": etsy_buyer.address_city,
                                                 "first_name": buyer_name1,
                                                 "last_name": buyer_name2,
                                                 "zip": etsy_buyer.address_zip,
                                                 "name": etsy_buyer.name,
                                                 "province_code": etsy_buyer.address_state,
                                                 "country_code": "US",
                                                 "default": True
                                             }
                                         }).encode("utf-8"))
        log.info(f"update customer response: {response}")

    def create_customer(self, etsy_buyer: EtsyBuyer) -> int:
        log.info(f"Creating a new customer for {etsy_buyer}")
        (buyer_name1, buyer_name2) = etsy_buyer.name.rsplit(" ", 1)
        new_customer = shopify.Customer()
        new_customer.first_name = buyer_name1
        new_customer.last_name = buyer_name2
        new_customer.email = etsy_buyer.email
        new_customer.verified_email = True
        new_customer.send_email_welcome: False
        new_customer.save()

        log.info(f"add new customer response: {new_customer.id}")
        self.add_customer_address(etsy_buyer, new_customer.id)
        return new_customer.id

    def create_order(self, order, customer_id):
        pass

    # use customer id or new customer info to create an order
    # mark it paid
    # add a tag to signify the lazyboost import
    # ensure gift message and gift pref is carried
    # ensure discounts are carried
    # ensure shipping, tax and totals are carried
