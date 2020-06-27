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
FacebookHandler module handles interactions with Facebook API and other options for import/export.
"""

from lazyboost import file_handler, log, utility_models

_cli_logger = log.console_logger()
_logger = log.create_logger(__name__)


def generate_facebook_import_csv(etsy_listings: list):
    """
    Function that receives list(EtsyListing) and exports them to a CSV file for Facebook import.
    :param etsy_listings: list(EtsyListing)
    :return:
    """
    facebook_listings = [
        (lambda x: utility_models.convert_etsy_to_facebook_listing(x))(el) for el in etsy_listings]
    facebook_listings = sorted(facebook_listings, key=lambda f: f.id)
    file_handler.write_facebook_import_csv_file(facebook_listings=facebook_listings)
