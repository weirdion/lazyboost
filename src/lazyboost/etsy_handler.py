#  LazyBoost
#  Copyright (C) 2020  Ankit Sadana
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
EtsyHandler contains the handlers to interact with Etsy API.
"""
import logging
from urllib.parse import urljoin

import requests

from lazyboost import log
from lazyboost.models import LazyEtsyConfig

SERVER_ADDRESS = "https://openapi.etsy.com/v2/"

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def get_active_listings(config: LazyEtsyConfig) -> []:
    """
    :param config: LazyConfig, contains the config options to interact with
    """
    sub_url = f"shops/{config.etsy_shop_id}/listings/active"
    params = dict()
    params['api_key'] = config.etsy_token

    response = requests.get(urljoin(SERVER_ADDRESS, sub_url), params=params)

    if response.status_code == 200:
        return _parse_active_listings(response.json())
    else:
        log.combined_log(_logger, _cli_logger, logging.ERROR,
                         f"Failed to get Etsy active listings, error: {response.status_code}")


def _parse_active_listings(received_data: dict) -> []:
    """
    :param received_data:
    """
    return []
