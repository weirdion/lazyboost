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
Command Handler module handles operations after the cli receives a command
"""
import logging

from lazyboost import etsy_handler, facebook_handler, log
from lazyboost.models import LazyConfig, LazyEtsyConfig, LazyFacebookConfig

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def parse_received_command(received_args):
    """
    Function that parses the received args into commands and executes the respective function.
    :params received_args: Namespace object received from ArgumentParser use.
    """
    log.combined_log(_logger, _cli_logger, logging.INFO, f'Command received: {received_args}')
    lazy_config = LazyConfig(
        etsy_config=LazyEtsyConfig(etsy_token=received_args.etsy_token,
                                   etsy_shop_id=received_args.etsy_shop_id),
        facebook_config=LazyFacebookConfig(facebook_token=received_args.facebook_token)
    )
    convert_etsy_listing_to_facebook_import_csv(lazy_config=lazy_config)


def convert_etsy_listing_to_facebook_import_csv(lazy_config: LazyConfig):
    """
    :param lazy_config:
    """
    etsy_listings = etsy_handler.get_active_listings(config=lazy_config.etsy_config)
    facebook_handler.generate_facebook_import_csv(etsy_listings=etsy_listings)
