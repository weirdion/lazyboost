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
from enum import auto

from lazyboost import log, models
from lazyboost.models.buyer_model import Buyer
from lazyboost.models.etsy_client import EtsyClient
from lazyboost.models.etsy_order import EtsyTransaction, EtsyOrder
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

        self._get_etsy_orders()

    def _get_etsy_orders(self):
        response = self.etsy_client.get_shop_receipts()
        etsy_orders = []
        for r in response["results"]:
            e = EtsyOrder(
                receipt_id=r["receipt_id"],
                buyer=Buyer(
                    name=r["name"],
                    email=r["buyer_email"],
                    address_first_line=r["first_line"],
                    address_second_line=r["second_line"],
                    address_city=r["city"],
                    address_state=r["state"],
                    address_zip=r["zip"]
                ),
                message_from_buyer=r["message_from_buyer"],
                is_shipped=r["is_shipped"],
                create_timestamp=r["create_timestamp"],
                update_timestamp=r["update_timestamp"],
                is_gift=r["is_gift"],
                gift_message=r["gift_message"],
                sale_total_cost=get_float_amount(r["grandtotal"]),
                sale_subtotal_cost=get_float_amount(r["subtotal"]),
                sale_shipping_cost=get_float_amount(r["total_shipping_cost"]),
                sale_tax_cost=get_float_amount(r["total_tax_cost"]),
                sale_discount_cost=get_float_amount(r["discount_amt"])
            )
            for t in r["transactions"]:
                e.transactions.append(
                    EtsyTransaction(
                        product_sku=t["sku"],
                        product_quantity=t["quantity"],
                        product_price=get_float_amount(t["price"]),
                        product_shipping_cost=get_float_amount(t["shipping_cost"])
                    )
                )

            _cli_logger.info(f"Adding etsy order: {e}")
            etsy_orders.append(e)
