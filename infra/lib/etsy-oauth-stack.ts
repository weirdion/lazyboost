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

import {CfnOutput, RemovalPolicy, SecretValue, Stack, StackProps, Tags} from 'aws-cdk-lib';
import {AuthorizationType, LambdaIntegration, RestApi} from 'aws-cdk-lib/aws-apigateway';
import {AssetCode, Code, Function, Runtime} from 'aws-cdk-lib/aws-lambda';
import {Secret} from 'aws-cdk-lib/aws-secretsmanager';
import {Construct} from 'constructs';
import * as fs from 'fs';
import * as path from 'path';

interface TenantCredentials {
  client_id: string;
  client_secret: string;
}

interface TenantMap {
  [tenantDomain: string]: TenantCredentials;
}

export interface EtsyOauthProps extends StackProps {
  tenantSecretsFile: string;
}

export class EtsyOauthStack extends Stack {
  constructor(scope: Construct, id: string, props: EtsyOauthProps) {
    super(scope, id, props);

    const secretData: { tenants: TenantMap } = JSON.parse(
      fs.readFileSync(props.tenantSecretsFile).toString()
    );

    const api = new RestApi(this, 'EtsyOAuthApi', {
      restApiName: 'Etsy OAuth Service',
      description: 'Handles Etsy OAuth initiation and callbacks.',
      defaultMethodOptions: {
        authorizationType: AuthorizationType.IAM
      }
    });

    for (const [tenant, creds] of Object.entries(secretData.tenants)) {
      // Create a secret for each tenant
      const etsySecret = new Secret(this, `Secret-${tenant}`, {
        secretName: `/etsy/clients/${tenant}/credentials`,
        secretObjectValue: {
          client_id: SecretValue.unsafePlainText(creds.client_id),
          client_secret: SecretValue.unsafePlainText(creds.client_secret)
        },
        removalPolicy: RemovalPolicy.RETAIN,
        description: `OAuth credentials for ${tenant}`
      });

      Tags.of(this).add('Tenant', tenant);

      // Init oauth lambda
      const initiateOAuthLambda = new Function(this, `InitiateOAuth-${tenant}`, {
        runtime: Runtime.PYTHON_3_13,
        handler: 'initiate.handler',
        code: Code.fromAsset(path.join(__dirname, '../lambda/oauth/initiate')),
        environment: {
          TENANT_SECRET_NAME: etsySecret.secretName,
          TENANT_DOMAIN: tenant
        }
      });

      const callbackOAuthLambda = new Function(this, `CallbackOAuth-${tenant}`, {
        runtime: Runtime.PYTHON_3_13,
        handler: 'callback.handler',
        code: Code.fromAsset(path.join(__dirname, '../lambda/oauth/callback')),
        environment: {
          TENANT_SECRET_NAME: etsySecret.secretName,
          TENANT_DOMAIN: tenant
        }
      });

      etsySecret.grantRead(initiateOAuthLambda);
      etsySecret.grantRead(callbackOAuthLambda);
      etsySecret.grantWrite(callbackOAuthLambda);

      const tenantResource = api.root.addResource(tenant.replace(/\./g, '-'));
      tenantResource
        .addResource('oauth')
        .addMethod('GET', new LambdaIntegration(initiateOAuthLambda));
      tenantResource
        .addResource('callback')
        .addMethod('GET', new LambdaIntegration(callbackOAuthLambda), {
          authorizationType: AuthorizationType.NONE
      });
    }
  }
}
