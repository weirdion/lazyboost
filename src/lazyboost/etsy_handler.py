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
from lazyboost.models import EtsyListing, EtsyListingState, LazyEtsyConfig

SERVER_ADDRESS = "https://openapi.etsy.com/v2/"

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def get_active_listings(config: LazyEtsyConfig, number_of_items_to_sync: int) -> list:
    """
    Reference: https://www.etsy.com/developers/documentation/reference/listing
    :param config: LazyConfig, contains the config options to interact with
    :param number_of_items_to_sync: int, number of items to be synced from Etsy
    """
    sub_url = f"shops/{config.etsy_shop_id}/listings/active"
    params = dict()
    params['api_key'] = config.etsy_token
    params['limit'] = number_of_items_to_sync

    _cli_logger.info("Attempting to request information from Etsy...")
    response = requests.get(urljoin(SERVER_ADDRESS, sub_url), params=params)

    if response.status_code == 200:
        listings = _parse_active_listings(response.json())
        return _retrieve_listing_images(listings, config.etsy_token)
    else:
        log.combined_log(_logger, _cli_logger, logging.ERROR,
                         f"Failed to get Etsy active listings, error: {response.status_code}")


def _parse_active_listings(received_data: dict) -> list:
    """
    :param received_data:
    """
    listings = []
    result_list = received_data['results']
    for index, item in enumerate(reversed(result_list)):
        _cli_logger.info(f"Parsing result {index} out of {received_data['count']}")
        listing = EtsyListing(
            listing_id=item['listing_id'], state=EtsyListingState(item['state']),
            user_id=item['user_id'], title=item['title'], description=item['description'],
            price=item['price'], currency_code=item['currency_code'], quantity=item['quantity'],
            sku=item['sku'][0], tags=item['tags'], materials=item['materials'],
            occasion=item['occasion'], taxonomy_path=item['taxonomy_path'])
        listings.append(listing)

    _cli_logger.info("All listings parsed.")
    return listings


def _retrieve_listing_images(listings: list, api_key: str):
    """
    :param listings:
    :return:
    """
    params = dict()
    params['api_key'] = api_key

    for index, item in enumerate(listings):
        _cli_logger.info(f"Retrieving images for listing {index} out of {len(listings)}")
        sub_url = f"listings/{item.listing_id}/images"
        response = requests.get(urljoin(SERVER_ADDRESS, sub_url), params=params)

        if response.status_code == 200:
            response_json = response.json()['results']
            listings[index].primary_image = response_json[0]['url_fullxfull']
            listings[index].secondary_images = [i['url_fullxfull'] for i in response_json[1:]]

    _cli_logger.info("All listing images retrieved successfully.")
    return listings
