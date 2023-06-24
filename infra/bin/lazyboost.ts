#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { LazyboostStack } from '../lib/lazyboost-stack';
import { LazyboostMonitoringStack } from '../lib/lazyboost-monitoring';

const app = new cdk.App();

const serviceName = 'LazyBoost';
const metricNamespace = 'LazyBoost';

new LazyboostStack(app, 'LazyboostStack', {
    serviceName: serviceName,
    metricNamespace: metricNamespace,
});

new LazyboostMonitoringStack(app, 'LazyboostMonitoringStack', {
    metricNamespace: metricNamespace,
});
