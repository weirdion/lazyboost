import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import { RemovalPolicy } from 'aws-cdk-lib';
import { DockerImageCode, DockerImageFunction, LayerVersion, Runtime } from 'aws-cdk-lib/aws-lambda';
import { RetentionDays } from 'aws-cdk-lib/aws-logs';
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
      code: DockerImageCode.fromImageAsset(path.resolve('.')),
      environment: {
        POWERTOOLS_SERVICE_NAME: 'LazyBoost',
        LOG_LEVEL: 'INFO'
      },
    });
    secret.grantRead(lazyboost_lambda);
    secret.grantWrite(lazyboost_lambda);
  }
}
