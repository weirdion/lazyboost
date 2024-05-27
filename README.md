# LazyBoost

A lazy python-ion way to pull and sync Orders and Listings between Etsy and Shopify.

## Features

 * Etsy OAuth handshake for auth (using API Gateway and NodeJS lambdas)
 * Python Docker Lambda to run the synchronization code
 * CloudWatch Cron rule to run Lambda at intervals
 * CLI interface for local execution
 * Clipboard interface to manipulate Shopify tags into your clipboard
 * Interface to pull Etsy reviews and publish to Judge.Me

## Preparing for Development

1. Ensure [poetry](https://python-poetry.org/docs/#installation) is installed
2. Run `make` to fetch development dependencies
3. Run `poetry shell` to activate virtual environment
4. You can now run `lazyboost` within your virtual environment

## Usage

To view the help page, and all available options,

```sh
> lazyboost --help

usage: lazyboost [-h] [-v] OPTION ...

A simple way to manage your shop listings between Etsy SHop Manager and Facebook Page Shop.

options:
    -h, --help
    -v, --version  show program's version number and exit

Options:
    Sub-options allow you to control smaller aspects of the platform

    OPTION
        clipboard    Takes the clipboard contents and formats them for re-using them on Etsy and Facebook publishing
        orders       orders help
        review-sync  listings help
        listings     listings help

Command 'clipboard'
usage: lazyboost clipboard [-h]

Command 'orders'
usage: lazyboost orders [-h] [-s | -e2s | -s2e]

options:
    -h, --help            show this help message and exit
    -s, --sync            Sync Orders from both Etsy and Shopify with each other (default)
    -e2s, --etsy-to-shopify
                                                Sync Orders from Etsy to Shopify
    -s2e, --shopify-to-etsy
                                                Sync Orders from Etsy to Shopify

Command 'review-sync'
usage: lazyboost review-sync [-h]

Command 'listings'
usage: lazyboost listings [-h]
```

## Running Tests

Run tests:

```sh
    $ make test
```
