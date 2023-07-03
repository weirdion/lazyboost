/*
 * LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
 * Copyright (C) 2023  Ankit Sadana
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
import {Duration, RemovalPolicy} from 'aws-cdk-lib';
import {LambdaIntegration, RestApi} from 'aws-cdk-lib/aws-apigateway';
import {RuleTargetInput} from 'aws-cdk-lib/aws-events';
import {Architecture, AssetCode, DockerImageCode, DockerImageFunction, Function, Runtime} from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import {Construct} from 'constructs';
import path = require('path');

export interface LazyBoostProps extends cdk.StackProps {
  serviceName: string
  metricNamespace: string
}

export class LazyboostStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: LazyBoostProps) {
    super(scope, id, props);

    const secret = new secretsmanager.Secret(this, 'LAZYBOOST_CREDS', {
      secretName: 'LAZYBOOST_CREDS',
      removalPolicy: RemovalPolicy.RETAIN,
    });

    const initEtsyOauth = new Function(this, 'InitEtsyOauth', {
      functionName: 'InitEtsyOauth',
      runtime: Runtime.NODEJS_18_X,
      code: new AssetCode('infra/resources/lambdas/etsy-auth-init'),
      handler: 'index.handler',
      environment: {
        'SECRET_NAME': secret.secretName
      }
    });
    secret.grantRead(initEtsyOauth);
    secret.grantWrite(initEtsyOauth);

    const oauthRedirect = new Function(this, 'EtsyOauthRedirect', {
      functionName: 'EtsyOauthRedirect',
      runtime: Runtime.NODEJS_18_X,
      code: new AssetCode('infra/resources/lambdas/etsy-auth-redirect'),
      handler: 'index.handler',
      environment: {
        'SECRET_NAME': secret.secretName
      }
    });
    secret.grantRead(oauthRedirect);
    secret.grantWrite(oauthRedirect);

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

    const lazyboost_lambda = new DockerImageFunction(this, 'LazyBoostFunction', {
      functionName: 'LazyBoostFunction',
      code: DockerImageCode.fromImageAsset(path.resolve('.')),
      architecture: Architecture.ARM_64,
      environment: {
        POWERTOOLS_SERVICE_NAME: props.serviceName,
        LOG_LEVEL: 'INFO',
        POWERTOOLS_METRICS_NAMESPACE: props.metricNamespace,
      }
    });
    secret.grantRead(lazyboost_lambda);
    secret.grantWrite(lazyboost_lambda);

    new cdk.aws_events.Rule(this, 'order-sync-rule', {
        description: 'Rule to sync orders between Etsy and Shopify',
        targets: [
          new cdk.aws_events_targets.LambdaFunction(
            lazyboost_lambda,
            {
              event: RuleTargetInput.fromObject({"task": "sync"})
            }
          )],
        schedule: cdk.aws_events.Schedule.rate(Duration.minutes(16)),
      }
    );
  }
}
