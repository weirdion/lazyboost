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

import { RemovalPolicy, Stack, StackProps } from 'aws-cdk-lib';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';

export interface BaseProps extends StackProps {
  serviceName: string
}

export class BaseStack extends Stack {
  public lbSecret: Secret;
  constructor(scope: Construct, id: string, props: BaseProps) {
    super(scope, id, props);

    this.lbSecret = new Secret(this, 'LAZYBOOST_CREDS', {
      secretName: 'LAZYBOOST_CREDS',
      removalPolicy: RemovalPolicy.RETAIN,
    });
  }
}
