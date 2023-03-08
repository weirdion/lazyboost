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
from aws_lambda_powertools import Logger
from lazyboost.handlers import OrderHandler, OrdersEnum

logger = Logger()


def order_sync_handler(event, context):
    """
    Function that acts as an entrypoint for Order Sync entrypoint
    """
    logger.debug(f"Starting lambda with event: {event}")
    OrderHandler(order_sync_type=OrdersEnum.SYNC)
