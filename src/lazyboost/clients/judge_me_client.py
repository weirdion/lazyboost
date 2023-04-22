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
import json

import requests
from aws_lambda_powertools import Logger

from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.utilities import constants

logger = Logger()


class JudgeMeClient:
    def __init__(self):
        self.sm_client = SecretManagerClient()

        # self.public_token = self.sm_client.secret_variables["JUDGE_ME_PUBLIC_KEY"]
        # self.private_token = self.sm_client.secret_variables["JUDGE_ME_PRIVATE_KEY"]
        self.headers = {
            "Content-Type": "application/json",
        }

        logger.info("Initiating JudgeMe client")

    def create_review(self, review_data: dict):
        """
        Create an unpublished review
        :param review_data: dict, etsy review data
        """
        request_url = f"{constants.JUDGE_ME_BASE_URL}/reviews"

        # TODO: change back to debug
        logger.info(f"Sending request to {request_url}, data: {review_data}")

        response = requests.request(
            method="POST",
            url=request_url,
            headers=self.headers,
            data=json.dumps(review_data),
        )

        logger.debug(f"STATUS_CODE: {response.status_code} | URL: {request_url}")

        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ConnectionError(
                f"Could Not Connect. Status Code: {response.status_code}: {response.reason}"
            )
