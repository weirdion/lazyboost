#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2025  Ankit Patterson
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


import os
import hmac
import hashlib
import base64
import boto3
import time
import json
import urllib.parse
import requests

HMAC_SECRET = os.environ.get("HMAC_SECRET", "default-dev-secret")

secrets = boto3.client("secretsmanager")

ALLOWED_CLOCK_SKEW_SEC = 300  # 5 minutes

def is_valid_state(state_token: str, tenant: str) -> bool:
    try:
        payload, signature = state_token.rsplit("|", 1)
        expected_signature = hmac.new(HMAC_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            return False

        state_parts = payload.split("|")
        if len(state_parts) != 2:
            return False

        token_tenant, timestamp = state_parts
        if token_tenant != tenant:
            return False

        now = int(time.time())
        if abs(now - int(timestamp)) > ALLOWED_CLOCK_SKEW_SEC:
            return False

        return True
    except Exception as e:
        print(f"State validation error: {e}")
        return False

def handler(event, context):
    tenant = os.environ["TENANT_DOMAIN"]
    secret_name = os.environ["TENANT_SECRET_NAME"]

    query = event.get("queryStringParameters") or {}
    code = query.get("code")
    state = query.get("state")

    if not code or not state or not is_valid_state(state, tenant):
        return {"statusCode": 400, "body": "Invalid or expired state/token"}

    try:
        raw_secret = secrets.get_secret_value(SecretId=secret_name)
        creds = json.loads(raw_secret["SecretString"])
    except Exception as e:
        return {"statusCode": 500, "body": f"Secret retrieval failed: {str(e)}"}

    redirect_uri = f"https://{event['requestContext']['domainName']}/{tenant.replace('.', '-')}/callback"

    # Exchange code for token
    token_response = requests.post(
        "https://api.etsy.com/v3/public/oauth/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    if token_response.status_code != 200:
        print(f"Token exchange failed: {token_response.text}")
        return {"statusCode": 502, "body": "Token exchange failed"}

    token_data = token_response.json()

    # Update secret with access token and refresh token
    try:
        secrets.update_secret(
            SecretId=secret_name,
            SecretString=json.dumps({
                **creds,
                "access_token": token_data["access_token"],
                "refresh_token": token_data["refresh_token"]
            })
        )
    except Exception as e:
        return {"statusCode": 500, "body": f"Secret update failed: {str(e)}"}

    return {
        "statusCode": 200,
        "body": "OAuth flow completed successfully and tokens securely stored."
    }
