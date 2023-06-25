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
import warnings

from aws_lambda_powertools import Logger, Metrics, single_metric
from aws_lambda_powertools.metrics import MetricUnit

from lazyboost.handlers import OrderHandler, OrdersEnum, ReviewHandler

warnings.filterwarnings("ignore", "No metrics to publish*")
logger = Logger()
metrics = Metrics()


@metrics.log_metrics  # Make sure metrics are flushed
def handler(event, context):
    """
    Handler function, entry point for the lambda triggers
    """
    logger.info(f"Starting lambda with event", event=event)

    if not (
        isinstance(event, dict)
        and "task" in event.keys()
        and event["task"] in ["order_sync", "review_sync", "sync"]
    ):
        raise ValueError(f"Invalid event or task type used: {event}, exiting...")

    try:
        if event["task"] == "order_sync":
            OrderHandler(order_sync_type=OrdersEnum.SYNC)
        elif event["task"] == "review_sync":
            ReviewHandler()
        elif event["task"] == "sync":
            OrderHandler(order_sync_type=OrdersEnum.SYNC)
            ReviewHandler()
        else:
            raise ValueError(f"Invalid task type received: {event['task']}")
    except Exception as e:
        with single_metric(name="LazyBoostSyncFail", unit=MetricUnit.Count, value=1) as metric:
            metric.add_dimension(name="Cause", value=str(e))

        logger.error(e)
