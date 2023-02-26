#  LazyBoost
#  Copyright (C) 2023  Ankit Sadana
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

from lazyboost import log, clipboard
from lazyboost.handlers import OrderHandler, OrdersEnum

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def parse_received_command(received_args):
    """
    Function that parses the received args into commands and executes the respective function.
    :params received_args: Namespace object received from ArgumentParser use.
    """
    log.combined_log(_logger, _cli_logger, logging.INFO, f'Command received: {received_args}')
    match received_args.opt:
        case "clipboard":
            clipboard.update_clipboard_tags()
        case "orders":
            OrderHandler(order_sync_type=OrdersEnum(received_args.order_option))
        case "listings":
            _cli_logger.info("Listings: Under construction")
        case _:
            _cli_logger.error("You seem to be lost.")
