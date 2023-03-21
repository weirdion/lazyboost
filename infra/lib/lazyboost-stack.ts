import * as cdk from 'aws-cdk-lib';
import { Duration, RemovalPolicy } from 'aws-cdk-lib';
import { DockerImageCode, DockerImageFunction } from 'aws-cdk-lib/aws-lambda';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import path = require('path');

export class LazyboostStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const secret = new secretsmanager.Secret(this, 'LAZYBOOST_CREDS', {
      secretName: 'LAZYBOOST_CREDS',
      removalPolicy: RemovalPolicy.RETAIN,
    });

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
      targets: [new cdk.aws_events_targets.LambdaFunction(lazyboost_lambda)],
      schedule: cdk.aws_events.Schedule.rate(Duration.minutes(16)),
    }
    );
  }
}
