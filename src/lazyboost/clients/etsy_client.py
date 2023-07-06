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
from datetime import datetime, timedelta
from urllib.parse import urljoin

import requests
from aws_lambda_powertools import Logger

from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.models.base_singleton import singleton
from lazyboost.utilities import constants

logger = Logger()


@singleton
class EtsyClient:
    def __init__(self):
        self.sm_client = SecretManagerClient()
        self.api_key_string = self.sm_client.secret_variables["ETSY_KEY_STRING"]
        self.access_token = self.sm_client.secret_variables["ETSY_ACCESS_TOKEN"]
        self.refresh_token = self.sm_client.secret_variables["ETSY_REFRESH_TOKEN"]
        self.shop_id = self.sm_client.secret_variables["ETSY_SHOP_ID"]
        self.headers = {
            "x-api-key": self.api_key_string,
            "Authorization": f"Bearer {self.access_token}",
        }

    def _http_oauth_request(self, method, suffix, params: dict = None, data: dict = None):
        """
        Execute HTTP API requests for Etsy REST API.
        """
        request_url = urljoin(constants.ETSY_API_BASE_URL, suffix)
        logger.debug(f"Sending {method} request to {request_url}, params: {params}, data: {data}")

        response = requests.request(
            method=method,
            url=request_url,
            headers=self.headers,
            params=params,
            data=data,
        )

        logger.debug(f"STATUS_CODE: {response.status_code} | URL: {request_url}")

        if response.status_code == 401 and response.json().get("error") == "invalid_token":
            self._refresh_token()
            logger.info("Retrying API call after Token Refresh...")
            response = requests.request(
                method=method,
                url=request_url,
                headers=self.headers,
                params=params,
                data=data,
            )

        if response.status_code == 200:
            return response.json()
        else:
            raise ConnectionError(f"Could Not Connect. Status Code: {response.status_code}")

    def _refresh_token(self):
        """
        Update Etsy Oauth tokens after expiration.
        """
        logger.debug("Attempting to update Access and Refresh tokens...")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": self.api_key_string,
            "refresh_token": self.refresh_token,
        }
        resp = requests.post(constants.ETSY_TOKEN_URL, headers=headers, data=data)
        if resp.status_code == 200:
            logger.debug("Successfully updated Access and Refresh tokens...")
            self.update_tokens(resp.json())
            self.set_headers()

    def update_tokens(self, response_dict: dict):
        """
        Update Access Token.
        """
        self.access_token = response_dict.get("access_token")
        self.refresh_token = response_dict.get("refresh_token")
        self.sm_client.secret_variables["ETSY_ACCESS_TOKEN"] = self.access_token
        self.sm_client.secret_variables["ETSY_REFRESH_TOKEN"] = self.refresh_token
        self.sm_client.update_secret_manager()

    def set_headers(self):
        """
        Update HTTP Headers.
        """
        self.headers = {
            "x-api-key": self.api_key_string,
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_shop_receipts(self):
        """
        Retrieve Etsy shop receipts.
        """
        logger.info("Retrieving shop receipts...")
        path = f"shops/{self.shop_id}/receipts"
        response = self._http_oauth_request(
            "GET",
            path,
            params={
                "min_created": int(round((datetime.now() - timedelta(minutes=20)).timestamp())),
                "max_created": int(round(datetime.now().timestamp())),
                "sort_order": "ascending",
                "was_shipped": False,
            },
        )
        return response

    def get_shop_receipt(self, receipt_id: int):
        """
        Retrieve Etsy shop receipt by id.
        """
        logger.debug("Retrieving shop transactions...")
        path = f"shops/{self.shop_id}/receipts/{receipt_id}"
        response = self._http_oauth_request("GET", path)
        return response

    def get_shop_reviews(self):
        """
        Retrieve Etsy shop reviews.
        """
        logger.debug("Retrieving shop reviews...")
        path = f"shops/{self.shop_id}/reviews"
        response = self._http_oauth_request(
            "GET",
            path,
            params={
                "min_created": int(round((datetime.now() - timedelta(minutes=16)).timestamp())),
                "max_created": int(round(datetime.now().timestamp())),
            },
        )
        return response

    def get_uer_info(self, user_id: int):
        """
        Retrieves Etsy user information with user_id.
        :param user_id: int, user id of the user to query.
        """
        logger.debug("Retrieving Etsy user")
        path = f"users/{user_id}"
        response = self._http_oauth_request(
            "GET",
            path,
        )
        return response

    def get_shop_transaction(self, transaction_id: int):
        """
        Retrieves Etsy user information with user_id.
        :param transaction_id: int, transaction id of the shop to query.
        """
        logger.debug("Retrieving Etsy transaction")
        # https://openapi.etsy.com/v3/application/
        path = f"shops/{self.shop_id}/transactions/{transaction_id}"
        response = self._http_oauth_request(
            "GET",
            path,
        )
        return response
