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
#

import requests
from aws_lambda_powertools import Logger
from requests.auth import HTTPBasicAuth

from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.utilities import constants

logger = Logger()


class StampedIOClient:
    def __init__(self, secret_manager_client: SecretManagerClient):
        self.sm_client = secret_manager_client

        self.api_key = self.sm_client.secret_variables.get("STAMPED_IO_API_KEY")
        self.store_hash = self.sm_client.secret_variables["STAMPED_IO_STORE_HASH"]
        self.api_pub_key = self.sm_client.secret_variables["STAMPED_IO_API_PUB_KEY"]
        self.basic_auth = HTTPBasicAuth(self.api_pub_key, self.api_key)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        logger.info("Initiating StampedIO client")

    def create_review(self, review_data: dict):
        """
        Create an unpublished review
        :param review_data: dict, etsy review data
        """
        request_url = f"{constants.STAMPED_IO_BASE_URL}/reviews3/?sId={self.store_hash}"

        # TODO: change back to debug
        logger.info(f"Sending request to {request_url}, data: {review_data}")

        response = requests.request(
            method="POST",
            headers=self.headers,
            auth=self.basic_auth,
            url=request_url,
            data=review_data,
        )

        logger.debug(f"STATUS_CODE: {response.status_code} | URL: {request_url}")

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(
                f"Could Not Connect. Status Code: {response.status_code}: {response.reason}"
            )
