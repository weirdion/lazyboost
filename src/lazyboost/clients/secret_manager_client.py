#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Patterson
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
import json
import os

import boto3
from aws_lambda_powertools import Logger
from botocore.exceptions import ClientError

from lazyboost.models.base_singleton import singleton


@singleton
class SecretManagerClient:
    def __init__(self):
        self.client = boto3.client("secretsmanager")
        self.secret_name = os.getenv("SECRET_NAME", "LAZYBOOST_CREDS")
        self.logger = Logger()
        self.secret_variables = {}
        self._get_value()

    def get_secret_variables(self) -> dict:
        if not self.secret_variables:
            self._get_value()
        return self.secret_variables

    def _get_value(self):
        """
        Function that gets the value of a secret.

        :return: The value of the secret. When the secret is a string, the value is
                 contained in the `SecretString` field. When the secret is bytes,
                 it is contained in the `SecretBinary` field.
        """
        try:
            kwargs = {"SecretId": self.secret_name}
            response = self.client.get_secret_value(**kwargs)
            self.logger.debug(f"Retrieved value for secret {self.secret_name}.")
        except ClientError:
            self.logger.exception(f"Couldn't get value for secret {self.secret_name}.")
            raise
        else:
            self.secret_variables = json.loads(response["SecretString"])

    def update_secret_manager(self):
        """
        Function that gets the value of a secret.

        :return: The value of the secret. When the secret is a string, the value is
                 contained in the `SecretString` field. When the secret is bytes,
                 it is contained in the `SecretBinary` field.
        """
        try:
            kwargs = {
                "SecretId": self.secret_name,
                "SecretString": json.dumps(self.secret_variables),
            }
            response = self.client.update_secret(**kwargs)
            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                self.logger.info(f"Successfully updated value for secret {self.secret_name}.")
            else:
                self.logger.warning(f"Something went wrong while updating the secret: {response}")
        except ClientError:
            self.logger.exception(f"Couldn't get value for secret {self.secret_name}.")
            raise
