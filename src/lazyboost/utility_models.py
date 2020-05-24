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
"""

from lazyboost.models import EtsyListing, EtsyListingState, FacebookListingAvailability, \
    FacebookListing


def convert_etsy_state_to_facebook_availability(etsy_listing_state: EtsyListingState) -> \
        FacebookListingAvailability:
    """
    :param etsy_listing_state:
    :return:
    """
    if etsy_listing_state == EtsyListingState.ACTIVE:
        return FacebookListingAvailability.IN_STOCK
    elif etsy_listing_state == EtsyListingState.REMOVED:
        return FacebookListingAvailability.DISCONTINUED
    elif etsy_listing_state == EtsyListingState.SOLD_OUT:
        return FacebookListingAvailability.OUT_OF_STOCK
    elif etsy_listing_state == EtsyListingState.EXPIRED:
        return FacebookListingAvailability.AVAILABLE_FOR_ORDER
    elif etsy_listing_state == EtsyListingState.DRAFT:
        return FacebookListingAvailability.PRE_ORDER
    elif etsy_listing_state == EtsyListingState.PRIVATE:
        return FacebookListingAvailability.PRE_ORDER
    elif etsy_listing_state == EtsyListingState.UNAVAILABLE:
        return FacebookListingAvailability.DISCONTINUED


def convert_etsy_to_facebook_listing(etsy_listing: EtsyListing) -> FacebookListing:
    """
    :param etsy_listing:
    :return:
    """
    facebook_listing = FacebookListing(
        # id =/= listing_id, id in facebook needs to be unique identifier
        # use SKU to manage listings across both platforms
        id=etsy_listing.sku,
        title=etsy_listing.title,
        description=etsy_listing.description,
        availability=convert_etsy_state_to_facebook_availability(etsy_listing.state),
        price=f"{etsy_listing.price} {etsy_listing.currency_code}",
        image_link=etsy_listing.primary_image,
        additional_image_link="\t".join(etsy_listing.secondary_images),
        inventory=etsy_listing.quantity,
    )
    return facebook_listing
