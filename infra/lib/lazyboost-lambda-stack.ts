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
import { Duration } from 'aws-cdk-lib';
import { RuleTargetInput } from 'aws-cdk-lib/aws-events';
import { Architecture, DockerImageCode, DockerImageFunction } from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { EmailIdentity, Identity } from 'aws-cdk-lib/aws-ses';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { Construct } from 'constructs';
import path = require('path');

export interface LazyBoostLambdaProps extends cdk.StackProps {
  serviceName: string,
  lbSecret: Secret
}

export class LazyboostLambdaStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: LazyBoostLambdaProps) {
    super(scope, id, props);

    const lazyboostSNSTopic = new Topic(this, 'LazyBoostErrorTopic', {
      displayName: 'LazyBoostErrorTopic',
    });

    const lazyboostErrorEmail = process.env['LAZYBOOST_ERROR_EMAIL'] as string;
    if (!lazyboostErrorEmail) {
      throw new Error('LAZYBOOST_ERROR_EMAIL env variable is not set.');
    }

    const emailIdentity = new EmailIdentity(this, 'LazyBoostErrorEmail', {
      identity: Identity.email(lazyboostErrorEmail)
    });

    lazyboostSNSTopic.addSubscription(new EmailSubscription(lazyboostErrorEmail));
    const lazyboost_lambda = new DockerImageFunction(this, 'LazyBoostFunction', {
      functionName: 'LazyBoostFunction',
      code: DockerImageCode.fromImageAsset(path.resolve('.'), {
        assetName: `lazyboost_lambda_${new Date().toLocaleDateString('en-US')}`
      }),
      architecture: Architecture.X86_64,
      environment: {
        POWERTOOLS_SERVICE_NAME: props.serviceName,
        LOG_LEVEL: 'INFO',
        SNS_ERROR_TOPIC: lazyboostSNSTopic.topicArn,
        SYNC_INTERVAL_ORDERS_MIN: '20',
        SYNC_INTERVAL_REVIEWS_MIN: '17',
        SYNC_INTERVAL_LISTINGS_MIN: '17',
      }
    });
    props.lbSecret.grantRead(lazyboost_lambda);
    props.lbSecret.grantWrite(lazyboost_lambda);
    lazyboostSNSTopic.grantPublish(lazyboost_lambda);

    new cdk.aws_events.Rule(this, 'order-sync-rule', {
      description: 'Rule to sync orders between Etsy and Shopify',
      targets: [
        new cdk.aws_events_targets.LambdaFunction(
          lazyboost_lambda,
          {
            event: RuleTargetInput.fromObject({ "task": "sync" })
          }
        )],
      schedule: cdk.aws_events.Schedule.rate(Duration.minutes(17)),
    }
    );
  }
}
