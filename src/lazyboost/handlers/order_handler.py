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

"""
OrderHandler module handles operations related to order sync
"""
import sys
from enum import auto
from typing import List

from aws_lambda_powertools import Logger

from lazyboost import models
from lazyboost.clients.etsy_client import EtsyClient
from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.clients.shopify_client import ShopifyClient
from lazyboost.models.etsy_order import EtsyOrder

logger = Logger()


class OrdersEnum(models.BaseEnum):
    SYNC = auto()
    ETSY_TO_SHOPIFY = "e2s"
    SHOPIFY_TO_ETSY = "s2e"


class OrderHandler:
    def __init__(self, order_sync_type: OrdersEnum) -> None:
        super().__init__()
        logger.info(f"Initializing OrderHandler for: {order_sync_type}")

        self.secret_manager_client = SecretManagerClient()
        self.etsy_client = EtsyClient(self.secret_manager_client)
        self.shopify_client = ShopifyClient(self.secret_manager_client)

        if order_sync_type == OrdersEnum.SYNC:
            etsy_orders = self._get_etsy_orders()
            if not etsy_orders:
                logger.info("No Etsy open orders detected.")
            else:
                self._sync_etsy_orders(etsy_orders)
        elif order_sync_type == OrdersEnum.ETSY_TO_SHOPIFY:
            pass
        elif order_sync_type == OrdersEnum.SHOPIFY_TO_ETSY:
            pass
        else:
            logger.error("Unknown type of order detected, exiting...")
            sys.exit(1)

    def _get_etsy_orders(self) -> List[EtsyOrder]:
        response = self.etsy_client.get_shop_receipts()

        etsy_orders = []
        for r in response["results"]:
            e = EtsyOrder.from_dict(r)

            logger.info(f"Detected open etsy order: {e}")
            etsy_orders.append(e)
        return etsy_orders

    def _sync_etsy_orders(self, etsy_orders: List[EtsyOrder]):
        for order in etsy_orders:

            order_id = self.shopify_client.does_order_exist(order.receipt_id)

            if order_id:
                logger.info(f"Order Id: {order_id} already exists, skipping")
                continue

            logger.info(f"New order detected: {order_id}")
            sc = self.shopify_client.is_existing_customer(order.buyer)
            if sc:
                logger.info(f"Existing customer: {sc.id} placed an order.")
                self.shopify_client.update_customer(order.buyer, sc)
                customer_id = sc.id
            else:
                customer_id = self.shopify_client.create_customer(order.buyer)

            self.shopify_client.create_order(order, customer_id)
