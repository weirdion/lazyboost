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
from datetime import datetime, timedelta
from enum import auto
from urllib.parse import urljoin

import requests

from lazyboost import log, models
from lazyboost.utilities import constants, utility_base

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)

ETSY_GET_SHOP_RECEIPTS = "shops/{shop_id}/receipts"


class OrdersEnum(models.BaseEnum):
    SYNC = auto()
    ETSY_TO_SHOPIFY = "e2s"
    SHOPIFY_TO_ETSY = "s2e"


class OrderHandler:

    def __init__(self, order_sync_type: OrdersEnum) -> None:
        super().__init__()
        _cli_logger.info(order_sync_type)

        dotenv_variables = utility_base.get_dotenv_variables()
        self.etsy_shop_id = dotenv_variables["ETSY_SHOP_ID"]
        self.etsy_key_string = dotenv_variables["ETSY_KEY_STRING"]
        self._get_etsy_orders()

    def _get_etsy_orders(self):
        etsy_receipts_url_with_shop_id = ETSY_GET_SHOP_RECEIPTS.format(shop_id=self.etsy_shop_id)
        etsy_receipts_url = urljoin(constants.ETSY_API_BASE_URL, etsy_receipts_url_with_shop_id)
        _cli_logger.info(f"ETSY_URL: {etsy_receipts_url}")

        api_headers = {
            "x-api-key": self.etsy_key_string,
            "ContentType": "application/json"
        }
        api_params = {
            "min_created": int(round((datetime.now() - timedelta(days=1)).timestamp())),
            "max_created": int(round(datetime.now().timestamp())),
            "was_shipped": False
        }
        response = requests.get(etsy_receipts_url, headers=api_headers, params=api_params)
        _cli_logger.info(response.json())
