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
import json
import sys
from enum import auto
from typing import List

from lazyboost import log, models
from lazyboost.models.buyer_model import Buyer
from lazyboost.clients.etsy_client import EtsyClient
from lazyboost.models.etsy_order import EtsyTransaction, EtsyOrder
from lazyboost.clients.shopify_client import ShopifyClient
from lazyboost.utilities import utility_base
from lazyboost.utilities.utility_etsy import get_float_amount

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


class OrdersEnum(models.BaseEnum):
    SYNC = auto()
    ETSY_TO_SHOPIFY = "e2s"
    SHOPIFY_TO_ETSY = "s2e"


class OrderHandler:

    def __init__(self, order_sync_type: OrdersEnum) -> None:
        super().__init__()
        _cli_logger.info(order_sync_type)

        dotenv_variables = utility_base.get_dotenv_variables()
        self.etsy_client = EtsyClient(dotenv_variables)
        self.shopify_client = ShopifyClient(dotenv_variables)

        match order_sync_type:
            case OrdersEnum.SYNC:
                etsy_orders = self._get_etsy_orders()
                if not etsy_orders:
                    _cli_logger.info("No Etsy open orders detected.")

                _sync_etsy_orders(etsy_orders)
            case OrdersEnum.ETSY_TO_SHOPIFY:
                pass
            case OrdersEnum.SHOPIFY_TO_ETSY:
                pass
            case _:
                _cli_logger.error("Unknown type of order detected, exiting...")
                sys.exit(1)

    def _get_etsy_orders(self) -> List[EtsyOrder]:
        # response = self.etsy_client.get_shop_receipts()
        with open("sample-reponse.json") as f:
            response = json.load(f)
        etsy_orders = []
        for r in response["results"]:
            e = EtsyOrder.from_dict(r)

            _cli_logger.info(f"Adding etsy order: {e}")
            etsy_orders.append(e)
        return etsy_orders

    def _sync_etsy_orders(self, etsy_orders: List[EtsyOrder]):
        for order in etsy_orders:
            sc = self.shopify_client.is_existing_customer(order.buyer)
            _cli_logger.info(f"shopify customer: {sc}")
