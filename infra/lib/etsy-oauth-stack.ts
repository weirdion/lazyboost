/*
 * LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
 * Copyright (C) 2024  Ankit Patterson
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

import * as cdk from 'aws-cdk-lib';
import { LambdaIntegration, RestApi } from 'aws-cdk-lib/aws-apigateway';
import { AssetCode, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import path = require('path');

export interface EtsyOauthProps extends cdk.StackProps {
  lbSecret: Secret
}

export class EtsyOauthStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: EtsyOauthProps) {
    super(scope, id, props);

    const initEtsyOauth = new Function(this, 'InitEtsyOauth', {
      functionName: 'InitEtsyOauth',
      runtime: Runtime.NODEJS_18_X,
      code: new AssetCode('infra/resources/lambdas/etsy-auth-init'),
      handler: 'index.handler',
      environment: {
        'SECRET_NAME': props.lbSecret.secretName
      }
    });
    props.lbSecret.grantRead(initEtsyOauth);
    props.lbSecret.grantWrite(initEtsyOauth);
    new cdk.CfnOutput(this, "initEtsyOauthFunction", {
      value: initEtsyOauth.functionName
    });

    const oauthRedirect = new Function(this, 'EtsyOauthRedirect', {
      functionName: 'EtsyOauthRedirect',
      runtime: Runtime.NODEJS_18_X,
      code: new AssetCode('infra/resources/lambdas/etsy-auth-redirect'),
      handler: 'index.handler',
      environment: {
        'SECRET_NAME': props.lbSecret.secretName
      }
    });
    props.lbSecret.grantRead(oauthRedirect);
    props.lbSecret.grantWrite(oauthRedirect);
    new cdk.CfnOutput(this, "etsyOauthRedirect", {
      value: oauthRedirect.functionName
    });

    const apiGW = new RestApi(this, 'LazyBoostApi', {
      deploy: false
    });
    apiGW.root.addMethod('ANY');

    const apiNode = apiGW.root.addResource('api');
    const authCallback = apiNode.addResource('redirect');
    authCallback.addMethod(
      'GET',
      new LambdaIntegration(oauthRedirect)
    );
  }
}
