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


import json
import os
from datetime import datetime, timedelta
from typing import List

import shopify
from aws_lambda_powertools import Logger

from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.models.base_singleton import singleton
from lazyboost.models.etsy_buyer_model import EtsyBuyer
from lazyboost.models.etsy_order import EtsyOrder
from lazyboost.models.shopify_customer_model import ShopifyCustomer
from lazyboost.models.shopify_product_model import ShopifyMinimalProduct, ShopifyVariant, ShopifyListing

logger = Logger()


@singleton
class ShopifyClient:
    def __init__(self):
        self.sm_client = SecretManagerClient()
        self.api_version = "2023-04"
        self.is_test_mode = True if os.getenv("SHOPIFY_TEST_MODE", "").lower() == "true" else False

        if self.is_test_mode:
            self.shop_url = self.sm_client.secret_variables["SHOPIFY_TEST_SHOP_URL"]
            self.api_key = self.sm_client.secret_variables["SHOPIFY_TEST_API_KEY"]
            self.client_secret = self.sm_client.secret_variables["SHOPIFY_TEST_SECRET_KEY"]
            self.access_token = self.sm_client.secret_variables["SHOPIFY_TEST_ACCESS_TOKEN"]
        else:
            self.shop_url = self.sm_client.secret_variables["SHOPIFY_AFD_SHOP_URL"]
            self.api_key = self.sm_client.secret_variables["SHOPIFY_AFD_API_KEY"]
            self.client_secret = self.sm_client.secret_variables["SHOPIFY_AFD_SECRET_KEY"]
            self.access_token = self.sm_client.secret_variables["SHOPIFY_AFD_ACCESS_TOKEN"]

        logger.info("Initiating Shopify session")
        self.session = shopify.Session(self.shop_url, self.api_version, self.access_token)
        shopify.ShopifyResource.activate_session(self.session)

    def __del__(self):
        logger.debug("Clearing shopify session")
        shopify.ShopifyResource.clear_session()

    @property
    def shopify_domain(self) -> str:
        return self.session.url

    def is_existing_customer(self, etsy_buyer: EtsyBuyer) -> ShopifyCustomer:
        response = shopify.Customer.search(session=self.session, query=f"email:{etsy_buyer.email}")
        if not response:
            return None
        return ShopifyCustomer.from_dict(response[0].attributes)

    def update_customer(self, etsy_buyer: EtsyBuyer, shopify_customer: ShopifyCustomer) -> None:
        default_address = shopify_customer.default_address

        is_existing_address = None
        if default_address:
            # default_address will be None for customers that failed with Lambda timeout
            is_existing_address = default_address.is_billing_address_same(etsy_buyer)

        if not is_existing_address:
            for address in shopify_customer.addresses:
                if address.is_billing_address_same(etsy_buyer):
                    res = shopify.Customer.put(
                        f"{shopify_customer.id}/addresses/{address.id}/default",
                        body=json.dumps(
                            {
                                "address_id": address.id,
                                "customer_id": shopify_customer.id,
                            }
                        ).encode("utf-8"),
                    )
                    logger.info(
                        f"updating customer: {shopify_customer.id} default address: {res.code}"
                    )
                    is_existing_address = True
                    break

        # Address not found in any existing addresses
        if not is_existing_address:
            self.add_customer_address(etsy_buyer, shopify_customer.id)

    def add_customer_address(self, etsy_buyer: EtsyBuyer, shopify_customer_id: int) -> None:
        logger.info(f"Adding new address for {shopify_customer_id}")

        response = shopify.Customer.post(
            f"{shopify_customer_id}/addresses",
            body=json.dumps({"address": etsy_buyer.to_shopify_address()}).encode("utf-8"),
        )
        logger.debug(f"update customer response: {response}")

    def create_customer(self, etsy_buyer: EtsyBuyer) -> int:
        logger.info(f"Creating a new customer for {etsy_buyer}")
        (buyer_name1, buyer_name2) = etsy_buyer.name.rsplit(" ", 1)
        new_customer = shopify.Customer()
        new_customer.first_name = buyer_name1
        new_customer.last_name = buyer_name2
        new_customer.email = etsy_buyer.email
        new_customer.verified_email = True
        new_customer.send_email_welcome: False
        new_customer.save()

        logger.info(f"add new customer response: {new_customer.id}")
        self.add_customer_address(etsy_buyer, new_customer.id)
        return new_customer.id

    def get_product_id(self, product_sku: str):
        res = shopify.GraphQL().execute(
            query="""
            query($filter: String!) {
              productVariants(first: 1, query: $filter) {
                edges {
                  node {
                    id
                  }
                }
              }
            }
            """,
            variables={"filter": f"sku:{product_sku}"},
        )

        response_dict: dict = json.loads(res)
        if "errors" in response_dict.keys() and response_dict["errors"]:
            logger.error("Failed to get product variant", error=response_dict)
        else:
            products = json.loads(res)["data"]["productVariants"]["edges"]
            logger.info(f"Product found: {products}")
            return products[0]["node"]["id"].rsplit("/", 1)[-1]

    def get_product_info(self, product_sku: str):
        res = shopify.GraphQL().execute(
            query="""
            query($filter: String!) {
              productVariants(first: 1, query: $filter) {
                edges {
                  node {
                    id
                    product {
                      id
                      title
                      onlineStoreUrl
                      handle
                      featuredImage {
                        url
                      }
                    }
                  }
                }
              }
            }
            """,
            variables={"filter": f"sku:{product_sku}"},
        )

        response_dict: dict = json.loads(res)
        if "errors" in response_dict.keys() and response_dict["errors"]:
            logger.error("Failed to get product info", error=response_dict)
        else:
            products = json.loads(res)["data"]["productVariants"]["edges"]
            logger.debug(f"Product found: {products}")
            if products:
                return ShopifyMinimalProduct.from_dict(products[0]["node"]["product"])
            else:
                return None

    def get_new_products(self, timestamp_to_check: datetime) -> List[ShopifyListing]:
        timestamp = timestamp_to_check.strftime('%Y-%m-%dT%H:%M:%SZ')
        res = shopify.GraphQL().execute(
            query="""
                query($filter: String!, $lzNamespace: String!) {
                  products(first: 10, query: $filter) {
                    edges {
                      node {
                        id
                        title
                        description
                        updatedAt
                        totalInventory
                        tags
                        metafields(first: 1, namespace: $lzNamespace) {
                          edges {
                            node {
                              namespace
                              key
                              value
                            }
                          }
                        }
                        variants(first: 10) {
                          edges {
                            node {
                              id
                              price
                              sku
                              inventoryQuantity
                              updatedAt
                              metafields(first: 1, namespace: $lzNamespace) {
                                edges {
                                  node {
                                    namespace
                                    key
                                    value
                                  }
                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }
                """,
            variables={
                "filter": f"status:ACTIVE AND updated_at:>{timestamp}",
                "lzNamespace": "lazyboost"
            },
        )

        response_dict: dict = json.loads(res)
        if "errors" in response_dict.keys() and response_dict["errors"]:
            logger.error("Failed to get products", error=response_dict)
            return []

        logger.info("Query cost for get_new_products", cost=response_dict["extensions"]["cost"])

        raw_products = json.loads(res)["data"]["products"]["edges"]
        products = [ShopifyListing.from_dict(p["node"]) for p in raw_products]
        logger.debug(f"Products found: {products}")
        return products

    def does_order_exist(self, receipt_id: int) -> str:
        res = shopify.GraphQL().execute(
            query="""
            query($filter: String!) {
              orders(first: 1, query: $filter) {
                edges {
                  node {
                    id
                  }
                }
              }
            }
            """,
            variables={"filter": f"tag:ETSY_{receipt_id}"},
        )
        orders_found = json.loads(res)["data"]["orders"]["edges"]
        return orders_found[0]["node"]["id"].rsplit("/", 1)[-1] if orders_found else ""

    def create_order(self, etsy_order: EtsyOrder, customer_id):
        logger.info(f"Creating a new shopify order for customer: {customer_id}")
        new_order = shopify.Order.create(
            {
                "email": etsy_order.buyer.email,
                "billing_address": etsy_order.buyer.to_shopify_address(),
                "customer": {"id": customer_id},
                "inventory_behaviour": "decrement_obeying_policy",
                "financial_status": "paid",
                "fulfillment_status": None,
                "line_items": [
                    {
                        "variant_id": self.get_product_id(t.product_sku),
                        "sku": t.product_sku,
                        "quantity": t.product_quantity,
                        "requires_shipping": True,
                        "price": t.product_price,
                        "properties": {"message": etsy_order.message_from_buyer}
                        if etsy_order.message_from_buyer
                        else [],
                    }
                    for t in etsy_order.transactions
                ],
                "note": f"Gift Message: {etsy_order.gift_message}" if etsy_order.is_gift else "",
                "send_receipt": True,
                "shipping_address": etsy_order.buyer.to_shopify_address(),
                "shipping_lines": [
                    {
                        "title": "Standard Shipping",
                        "price": etsy_order.sale_shipping_cost,
                    }
                ],
                "source_name": "Etsy",
                "source_identifier": etsy_order.receipt_id,
                "subtotal_price": etsy_order.sale_subtotal_cost,
                "tags": f"LazyBoost, ETSY_{etsy_order.receipt_id}",
                "tax_lines": [
                    {
                        "title": "Etsy Sales Tax",
                        "price": etsy_order.sale_tax_cost,
                        "rate": round(etsy_order.sale_tax_cost / etsy_order.sale_subtotal_cost, 2),
                        "channel_liable": None,
                    }
                ],
                "total_discounts": etsy_order.sale_discount_cost,
                "total_price": etsy_order.sale_total_cost,
                "total_tax": etsy_order.sale_tax_cost,
                "transactions": [
                    {
                        "amount": etsy_order.sale_total_cost,
                        "currency": "USD",
                        "kind": "capture",
                        "status": "success",
                        "gateway": "Etsy Checkout",
                    }
                ],
            }
        )
        if new_order.errors:
            logger.error(f"Error occurred during order creation: {new_order.errors.errors}")
        else:
            logger.info(f"Shopify order created successfully: {new_order}")
