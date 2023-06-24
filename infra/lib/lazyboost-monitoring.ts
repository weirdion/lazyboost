import * as cdk from 'aws-cdk-lib';
import { Alarm, ComparisonOperator, Metric, TreatMissingData } from "aws-cdk-lib/aws-cloudwatch";
import { SnsAction } from "aws-cdk-lib/aws-cloudwatch-actions";
import { Topic } from "aws-cdk-lib/aws-sns";
import { EmailSubscription } from "aws-cdk-lib/aws-sns-subscriptions";
import { Construct } from 'constructs';

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
            }
        );

        const lazyboostSNSTopic = new Topic(this, 'LazyBoostErrorTopic', {
            displayName: 'LazyBoostErrorTopic',
        });

        const lazyboostErrorEmail = new cdk.CfnParameter(this, "errorEmail", {
            type: "String",
            description: "The email address that will be notified on LazyBoost error is in alarm state.",
        });

        lazyboostSNSTopic.addSubscription(new EmailSubscription(lazyboostErrorEmail.valueAsString));
        lazyboostFuncAlarm.addAlarmAction(new SnsAction(lazyboostSNSTopic));
    }
}