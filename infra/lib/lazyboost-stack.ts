import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import { RemovalPolicy } from 'aws-cdk-lib';
import { LayerVersion, Runtime } from 'aws-cdk-lib/aws-lambda';
import { RetentionDays } from 'aws-cdk-lib/aws-logs';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export class LazyboostStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const secret = new secretsmanager.Secret(this, 'LAZYBOOST_CREDS', {
      secretName: 'LAZYBOOST_CREDS',
      removalPolicy: RemovalPolicy.RETAIN,
    });

    const powertoolsApp = new cdk.aws_sam.CfnApplication(this, 'AWSLambdaPowertoolsApplication', {
      location: {
        applicationId: 'arn:aws:serverlessrepo:eu-west-1:057560766410:applications/aws-lambda-powertools-python-layer',
        semanticVersion: '2.0.0'
      }
    });

    const powertoolsLayerArn = powertoolsApp.getAtt('Outputs.LayerVersionArn').toString();
    const powertoolsLayerVersion = LayerVersion.fromLayerVersionArn(this, 'AWSLambdaPowertools', powertoolsLayerArn);

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
      environment: {
        POWERTOOLS_SERVICE_NAME: 'LazyBoost',
        LOG_LEVEL: 'INFO'
      },
      logRetention: RetentionDays.TWO_WEEKS,
      runtime: Runtime.PYTHON_3_9,
      layers: [powertoolsLayerVersion],
    });
    secret.grantRead(lazyboost_lambda);
    secret.grantWrite(lazyboost_lambda);
  }
}
