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
from urllib.parse import urljoin

import requests
from aws_lambda_powertools import Logger

from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.utilities import constants
from requests.auth import HTTPBasicAuth


logger = Logger()


class StampedIOClient:
    def __init__(self, secret_manager_client: SecretManagerClient):
        self.sm_client = secret_manager_client

        self.api_key = self.sm_client.secret_variables.get("STAMPED_IO_API_KEY")
        self.store_hash = self.sm_client.secret_variables["STAMPED_IO_STORE_HASH"]
        self.api_pub_key = self.sm_client.secret_variables["STAMPED_IO_API_PUB_KEY"]

        logger.info("Initiating StampedIO client")


    def _create_review(self, ):
        """
        Create an unpublished review
        """
