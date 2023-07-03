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
import {ComparisonOperator, Metric, TreatMissingData} from "aws-cdk-lib/aws-cloudwatch";
import {SnsAction} from "aws-cdk-lib/aws-cloudwatch-actions";
import {Topic} from "aws-cdk-lib/aws-sns";
import {EmailSubscription} from "aws-cdk-lib/aws-sns-subscriptions";
import {Construct} from 'constructs';

export interface LazyBoostMonitoringProps extends cdk.StackProps {
  metricNamespace: string
}

export class LazyboostMonitoringStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: LazyBoostMonitoringProps) {
    super(scope, id, props);

    const lazyboostSyncFailMetric = new Metric({
      namespace: props.metricNamespace,
      metricName: 'LazyBoostSyncFail',
    });

    const lazyboostFuncAlarm = lazyboostSyncFailMetric.createAlarm(
      this,
      'LazyBoostSyncFailAlarm', {
        alarmName: 'LazyBoostSyncFailAlarm',
        comparisonOperator: ComparisonOperator.GREATER_THAN_THRESHOLD,
        threshold: 0,
        evaluationPeriods: 1,
        treatMissingData: TreatMissingData.NOT_BREACHING,
        actionsEnabled: true,
      }
    );

    const lazyboostSNSTopic = new Topic(this, 'LazyBoostErrorTopic', {
      displayName: 'LazyBoostErrorTopic',
    });

    const lazyboostErrorEmail = process.env['LAZYBOOST_ERROR_EMAIL'] as string;
    if (!lazyboostErrorEmail) {
      throw new Error('LAZYBOOST_ERROR_EMAIL env variable is not set.')
    }

    lazyboostSNSTopic.addSubscription(new EmailSubscription(lazyboostErrorEmail));
    lazyboostFuncAlarm.addAlarmAction(new SnsAction(lazyboostSNSTopic));
  }
}