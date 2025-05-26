/*
 * LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
 * Copyright (C) 2025  Ankit Patterson
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

const https = require('https');
const sm = require('@aws-sdk/client-secrets-manager');
const { error } = require('console');

const secret_name = process.env.SECRET_NAME;
const redirect_url = 'https://j8zlucnlxk.execute-api.us-east-1.amazonaws.com/prod/api/redirect';

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

const processResult = async (result) => {
  console.log(`Result: ${JSON.stringify(result)}`)
};

const postPromise = ((url, urlOptions, postData) => {
  return new Promise((resolve, reject) => {
    const req = https.request(url, urlOptions,
      (res) => {
        let body = '';
        res.on('data', (chunk) => (body += chunk.toString()));
        res.on('error', reject);
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode <= 299) {
            resolve({statusCode: res.statusCode, headers: res.headers, body: body});
          } else {
            reject(`Request failed. status: ${res.statusCode}, body: ${body}`);
          }
        });
      });
    req.on('error', reject);
    req.write(postData);
    req.end();
  });
});

const handler = async function (event, context) {
  console.log(`Lambda oauth redirect... event: ${JSON.stringify(event, null, 2)}, context: ${JSON.stringify(context, null, 2)}`);

  const authCode = event.queryStringParameters.code;
  const state = event.queryStringParameters.state;
  const secretString = await getSecretString();

  if (state !== secretString.state) { throw error; };

  const tokenUrl = 'https://api.etsy.com/v3/public/oauth/token';
  const postData = JSON.stringify({
    grant_type: 'authorization_code',
    client_id: secretString.ETSY_KEY_STRING,
    redirect_uri: redirect_url,
    code: authCode,
    code_verifier: secretString.codeVerifier,
  });
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    }
  };

  // Sending the request
  const response = await postPromise(tokenUrl, requestOptions, postData);
  console.log(`Response status: ${response.statusCode}, headers: ${JSON.stringify(response.headers)}`);
  responseSecrets = JSON.parse(response.body);
  secretString.ETSY_ACCESS_TOKEN = responseSecrets.access_token;
  secretString.ETSY_REFRESH_TOKEN = responseSecrets.refresh_token;
  await updateSecret(secretString);

  return {
    statusCode: 200,
    headers: { 'Content-Type': 'text/json' },
    body: 'Hello LazyBoost!'
  };
}

exports.handler = handler;
