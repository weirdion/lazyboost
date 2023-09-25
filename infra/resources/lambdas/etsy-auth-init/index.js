/*
 * LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
 * Copyright (C) 2023  Ankit Patterson
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

const crypto = require('crypto');
const http = require('http');
const sm = require('@aws-sdk/client-secrets-manager');

const secret_name = process.env.SECRET_NAME;
const redirect_url = 'https://j8zlucnlxk.execute-api.us-east-1.amazonaws.com/prod/api/redirect';

const etsyScope = [
  'address_r',
  'email_r',
  'listings_d', 'listings_r', 'listings_w',
  'shops_r', 'shops_w',
  'transactions_r', 'transactions_w'
]

const client = new sm.SecretsManagerClient({
  region: 'us-east-1',
});

const getSecretString = async () => {
  try {
    const response = await client.send(
      new sm.GetSecretValueCommand({
        SecretId: secret_name,
        VersionStage: 'AWSCURRENT', // VersionStage defaults to AWSCURRENT if unspecified
      })
    );
    return JSON.parse(response.SecretString);
  } catch (error) {
    // For a list of exceptions thrown, see
    // https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    throw error;
  }
}

const updateSecret = async (secretString) => {
  try {
    const response = await client.send(
      new sm.UpdateSecretCommand({
        SecretId: secret_name,
        SecretString: JSON.stringify(secretString)
      })
    );
  } catch (error) {
    throw error;
  }
};

const handler = async function (event, context) {
  console.log(`Lambda init auth... event: ${event}, context: ${context}`);

  // The next two functions help us generate the code challenge
  // required by Etsy’s OAuth implementation.
  const base64URLEncode = (encode) =>
    encode
      .toString('base64')
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');

  const sha256 = (buffer) =>
    crypto.createHash("sha256").update(buffer).digest();

  // We’ll use the verifier to generate the challenge.
  // The verifier needs to be saved for a future step in the OAuth flow.
  const codeVerifier = base64URLEncode(crypto.randomBytes(32));

  // With these functions, we can generate
  // the values needed for our OAuth authorization grant.
  const codeChallenge = base64URLEncode(sha256(codeVerifier));
  const state = Math.random().toString(36).substring(7);

  const secretString = await getSecretString();
  const etsyScopeFromatted = etsyScope.join('%20');
  const etsyAuthURL = `https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=${redirect_url}&scope=${etsyScopeFromatted}&client_id=${secretString.ETSY_KEY_STRING}&state=${state}&code_challenge=${codeChallenge}&code_challenge_method=S256`;


  console.log(`State: ${state}`);
  console.log(`Code challenge: ${codeChallenge}`);
  console.log(`Code verifier: ${codeVerifier}`);
  console.log(`Full URL: ${etsyAuthURL}`)

  secretString.codeVerifier = codeVerifier;
  secretString.state = state;
  await updateSecret(secretString);

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: 'Hello LazyBoost!'
  };
}

exports.handler = handler;
