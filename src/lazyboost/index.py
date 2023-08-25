#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Sadana
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
#
import os
from datetime import datetime

import boto3
from aws_lambda_powertools import Logger

from lazyboost.handlers import OrderHandler, OrdersEnum, ReviewHandler

logger = Logger()


def handler(event, context):
    """
    Handler function, entry point for the lambda triggers
    """
    logger.info(f"Starting lambda with event", event=event)

    try:
        if not (
            isinstance(event, dict)
            and "task" in event.keys()
            and event["task"] in ["order_sync", "review_sync", "sync"]
        ):
            raise ValueError(f"Invalid event or task type used: {event}, exiting...")

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
        sns_topic_arn = os.getenv("SNS_ERROR_TOPIC")
        date_now = datetime.now().strftime("%m/%d/%Y, %-I:%M:%S %p")
        if sns_topic_arn:
            sns_client = boto3.client("sns")
            response = sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=f"""
                An error occurred during execution of LazyBoost at {date_now}.\n\n
                Error: `{e}`\n
                ```{e.__traceback__}```
                """,
                Subject=f"LazyBoost encountered an error at {date_now}",
            )
            logger.info(f"SNS response: {response}")
        else:
            raise e
