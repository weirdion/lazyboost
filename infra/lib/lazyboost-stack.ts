import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import { CfnOutput, RemovalPolicy } from 'aws-cdk-lib';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { LogGroup, LogRetention, RetentionDays } from 'aws-cdk-lib/aws-logs';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export class LazyboostStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const secret = new secretsmanager.Secret(this, 'LAZYBOOST_CREDS', {
      secretName: 'LAZYBOOST_CREDS',
      removalPolicy: RemovalPolicy.RETAIN,
    });

    const lazyboost_lambda = new PythonFunction(this, 'LazyBoostFunction', {
      entry: 'src/lazyboost',
      index: 'index.py',
      handler: 'order_sync_handler',
      bundling: {
        commandHooks: {
          beforeBundling(inputDir: string): string[] {
            return ["find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete"];
          },
          afterBundling(inputDir: string): string[] {
            return [];
          },
        },
      },
      logRetention: RetentionDays.TWO_WEEKS,
      runtime: Runtime.PYTHON_3_9,
    });
    secret.grantRead(lazyboost_lambda);
    secret.grantWrite(lazyboost_lambda);
  }
}
