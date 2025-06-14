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

#!/usr/bin/env python3

import json
import boto3
import argparse

def update_secret(secret_name: str, secret_value: dict):
    client = boto3.client("secretsmanager")
    client.update_secret(
        SecretId=secret_name,
        SecretString=json.dumps(secret_value)
    )
    print(f"✅ Updated secret: {secret_name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to secrets.json")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        data = json.load(f)

    for tenant, creds in data["tenants"].items():
        secret_name = f"/etsy/clients/{tenant}/credentials"
        update_secret(secret_name, creds)

if __name__ == "__main__":
    main()
