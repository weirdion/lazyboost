#  LazyBoost
#  Copyright (C) 2020  Ankit Sadana
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
cli module handles the creation and use of the cli arguments
"""

from argparse import ArgumentParser, _HelpAction, _SubParsersAction
import sys

from lazyboost import command_handler, constants


class _HelpActionLongFormat(_HelpAction):  # pylint: disable=too-few-public-methods
    """
    Overridden class of argparse._HelpAction to allow long format print of help.
    """

    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()

        # retrieve subparsers from parser
        subparsers_actions = [
            action for action in parser._actions
            if isinstance(action, _SubParsersAction)]

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
        description='A simple way to manage your shop listings between Etsy SHop Manager and '
                    'Facebook Page Shop.',
        add_help=False
    )

    parser.add_argument(
        '-h',
        '--help',
        action=_HelpActionLongFormat
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f"{constants.CLI_NAME} {constants.__version__}"
    )

    parser.add_argument(
        '-et',
        '--etsy-token',
        help='Etsy access token'
    )

    parser.add_argument(
        '-es',
        '--etsy-shop-id',
        help='Etsy shop id'
    )

    parser.add_argument(
        '-ft',
        '--facebook-token',
        default='',
        help='Facebook access token'
    )

    parser.add_argument(
        '-n',
        '--number-of-items',
        default='1',
        help='Number of items to sync.'
    )

    return parser


def main():
    """
    Function that serves as the primary entry-point for the cli.
    """
    if len(sys.argv) <= 1:
        raise SystemExit(
            f"{constants.CLI_NAME}: No command received. "
            f"Run `{constants.CLI_NAME} --help` to see available options.")

    args = create_parser().parse_args()
    command_handler.parse_received_command(args)
