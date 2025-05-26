#!/usr/bin/env node
/*
 * LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
 * Copyright (C) 2025  Ankit Patterson
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
import 'source-map-support/register';
import { BaseStack } from '../lib/base-stack';
import { EtsyOauthStack } from '../lib/etsy-oauth-stack';
import { LazyboostLambdaStack } from '../lib/lazyboost-lambda-stack';

const app = new cdk.App();

const serviceName = 'LazyBoost';

const baseStack = new BaseStack(app, 'LazyboostBaseStack', {
  serviceName: serviceName,
});

const etsyOauthStack = new EtsyOauthStack(app, 'LazyboostEtsyOauthStack', {
  lbSecret: baseStack.lbSecret,
});

const lazyBoostLambdaStack = new LazyboostLambdaStack(app, 'LazyboostLambdaStack', {
  serviceName: serviceName,
  lbSecret: baseStack.lbSecret,
});
