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
import base64
import hashlib
import os
import re

from rauth import OAuth2Service

from lazyboost.utilities import constants


def init_etsy_session(dotenv_variables: dict):
    etsy_key_string = dotenv_variables["ETSY_KEY_STRING"]
    etsy_shared_secret = dotenv_variables["ETSY_SHARED_SECRET"]
    etsy_redirect_url = dotenv_variables["ETSY_REDIRECT_URL"]

    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
    code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.replace("=", "")

    state = "testingstate"

    etsy_oauth_service = OAuth2Service(
        client_id=etsy_key_string,
        client_secret=etsy_shared_secret,
        name="etsy",
        authorize_url=constants.ETSY_AUTH_URL,
        access_token_url=constants.ETSY_TOKEN_URL,
        base_url=constants.ETSY_AUTH_BASE_URL,
    )

    params = {
        "scope": "transactions_r",
        "response_type": "code",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "redirect_uri": etsy_redirect_url
    }

    # initial authorization
    url = etsy_oauth_service.get_authorize_url(**params)


