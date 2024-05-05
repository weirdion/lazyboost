#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2024  Ankit Patterson
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

"""
Command Handler module handles operations after the cli receives a command
"""

from aws_lambda_powertools import Logger

from lazyboost import clipboard
from lazyboost.handlers import ListingHandler, OrderHandler, OrdersEnum, ReviewHandler

logger = Logger()


def parse_received_command(received_args):
    """
    Function that parses the received args into commands and executes the respective function.
    :params received_args: Namespace object received from ArgumentParser use.
    """
    logger.info(f"Command received: {received_args}")
    if received_args.opt == "clipboard":
        clipboard.update_clipboard_tags()
    elif received_args.opt == "orders":
        OrderHandler(order_sync_type=OrdersEnum(received_args.order_option))
    elif received_args.opt == "listings":
        ListingHandler()
    elif received_args.opt == "review-sync":
        ReviewHandler()
    else:
        logger.error("You seem to be lost.")
