#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2024  Ankit Patterson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
cli module handles the creation and use of the cli arguments
"""

import sys
from argparse import ArgumentParser, _HelpAction, _SubParsersAction

from lazyboost import command_handler
from lazyboost.utilities import constants


class _HelpActionLongFormat(_HelpAction):  # pylint: disable=too-few-public-methods
    """
    Overridden class of argparse._HelpAction to allow long format print of help.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions if isinstance(action, _SubParsersAction)
        ]

        for subparsers_action in subparsers_actions:
            # get all subparsers and print help
            for choice, subparser in subparsers_action.choices.items():
                print(f"\nCommand '{choice}'")
                print(subparser.format_help())

        parser.exit()


def create_parser() -> ArgumentParser:
    """
    Function that creates the argument parser.
    :return: ArgumentParser, the object of ArgumentParser with configured options.
    """
    parser = ArgumentParser(
        prog=constants.CLI_NAME,
        description="A simple way to manage your shop listings between Etsy SHop Manager and "
        "Facebook Page Shop.",
        add_help=False,
    )

    parser.add_argument("-h", "--help", action=_HelpActionLongFormat)

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{constants.CLI_NAME} {constants.__version__}",
    )

    options_subparser = parser.add_subparsers(
        title="Options",
        description="Sub-options allow you to control smaller aspects of the platform",
        required=False,
        metavar="OPTION",
        dest="opt",
    )

    options_subparser.add_parser(
        "clipboard",
        help="Takes the clipboard contents and formats them for re-using them on Etsy and Facebook publishing",
    )

    orders_parser = options_subparser.add_parser("orders", help="orders help")
    order_opt_group = orders_parser.add_mutually_exclusive_group()
    order_opt_group.add_argument(
        "-s",
        "--sync",
        help="Sync Orders from both Etsy and Shopify with each other (default)",
        action="store_const",
        dest="order_option",
        const="sync",
        default="sync",
    )
    order_opt_group.add_argument(
        "-e2s",
        "--etsy-to-shopify",
        help="Sync Orders from Etsy to Shopify",
        action="store_const",
        dest="order_option",
        const="e2s",
    )
    order_opt_group.add_argument(
        "-s2e",
        "--shopify-to-etsy",
        help="Sync Orders from Etsy to Shopify",
        action="store_const",
        dest="order_option",
        const="s2e",
    )

    options_subparser.add_parser("review-sync", help="listings help")

    listings_parser = options_subparser.add_parser("listings", help="listings help")

    return parser


def main():
    """
    Function that serves as the primary entry-point for the cli.
    """
    if len(sys.argv) <= 1:
        raise SystemExit(
            f"{constants.CLI_NAME}: No command received. "
            f"Run `{constants.CLI_NAME} --help` to see available options."
        )

    args = create_parser().parse_args()
    command_handler.parse_received_command(args)


if __name__ == "__main__":
    main()
