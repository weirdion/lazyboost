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

"""
ReviewHandler module handles operations related to pulling reviews from Etsy.
"""
from typing import List

from aws_lambda_powertools import Logger

from lazyboost.clients.etsy_client import EtsyClient
from lazyboost.clients.secret_manager_client import SecretManagerClient
from lazyboost.models.etsy_review_model import EtsyReview

logger = Logger()


class ReviewHandler:
    def __init__(self) -> None:
        super().__init__()
        logger.info(f"Initializing ReviewHandler")

        self.secret_manager_client = SecretManagerClient()
        self.etsy_client = EtsyClient(self.secret_manager_client)

        etsy_reviews = self._get_etsy_reviews()
        if not etsy_reviews:
            logger.info("No new Etsy reviews detected.")
        else:
            self._sync_etsy_reviews(etsy_reviews)

    def _get_etsy_reviews(self):
        response = self.etsy_client.get_shop_reviews()

        etsy_reviews = []
        for r in response["results"]:
            e = EtsyReview.from_dict(r)
            logger.info(f"Detected Etsy review: {e}")
            e.get_additional_info(self.etsy_client)
            logger.info(f"Retrieved full etsy review information: {e}")
            etsy_reviews.append(e)
        return etsy_reviews

    def _sync_etsy_reviews(self, etsy_reviews: List[EtsyReview]):
        # for review in etsy_reviews:
        pass
