import * as cdk from 'aws-cdk-lib';
import { Duration, RemovalPolicy } from 'aws-cdk-lib';
import { LambdaIntegration, RestApi } from 'aws-cdk-lib/aws-apigateway';
import { Alarm, ComparisonOperator } from 'aws-cdk-lib/aws-cloudwatch';
import { SnsAction } from 'aws-cdk-lib/aws-cloudwatch-actions';
import { RuleTargetInput } from 'aws-cdk-lib/aws-events';
import { AssetCode, DockerImageCode, DockerImageFunction, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Topic } from 'aws-cdk-lib/aws-sns';
import { EmailSubscription } from 'aws-cdk-lib/aws-sns-subscriptions';
import { Construct } from 'constructs';
import path = require('path');

export class LazyboostStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
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
            environment: {
                POWERTOOLS_SERVICE_NAME: 'LazyBoost',
                LOG_LEVEL: 'INFO'
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
                        event: RuleTargetInput.fromObject({ "task": "sync" })
                    }
                )],
            schedule: cdk.aws_events.Schedule.rate(Duration.minutes(16)),
        }
        );

        const lazyboostFuncAlarm = new Alarm(
            this,
            'LazyBoostError', {
            alarmName: 'LazyBoostError',
            comparisonOperator: ComparisonOperator.GREATER_THAN_THRESHOLD,
            metric: lazyboost_lambda.metricErrors({
                period: Duration.minutes(15)  // Sum invocation errors at 15 minute interval.
            }),
            threshold: 1,
            evaluationPeriods: 15
        }
        );

        const lazyboostSNSTopic = new Topic(this, 'LazyBoostErrorTopic', {
            displayName: 'LazyBoostErrorTopic',
        });

        const lazyboostErrorEmail = new cdk.CfnParameter(this, "errorEmail", {
            type: "String",
            description: "The email address that will be notified on LazyBoost error is in alarm state."
        });

        lazyboostSNSTopic.addSubscription(new EmailSubscription(lazyboostErrorEmail.valueAsString));
        lazyboostFuncAlarm.addAlarmAction(new SnsAction(lazyboostSNSTopic));
    }
}
