#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Sadana
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
#
from lazyboost.utilities.constants import (
    ETSY_TAXONOMY_ID_DICT,
    ETSY_SHIPPING_PROFILE_ID_DICT,
    ETSY_SECTION_ID_DICT,
)


def get_float_amount(price_dict: dict) -> float:
    return price_dict["amount"] / price_dict["divisor"]


def get_taxonomy_by_product_type(product_type: str) -> str:
    product_type = product_type.casefold()
    return ETSY_TAXONOMY_ID_DICT[product_type]


def get_shipping_profile_id(product_type: str, price: str) -> int:
    if product_type.casefold() == "bows":
        return ETSY_SHIPPING_PROFILE_ID_DICT["Bows"]

    if int(price) < 89:
        return ETSY_SHIPPING_PROFILE_ID_DICT["MediumWreath-FixedShipCost"]
    else:
        return ETSY_SHIPPING_PROFILE_ID_DICT["WreathUSFreeShip"]


def get_section_id(tags: str) -> int:
    normalized_tags = tags.casefold()
    if "bow" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Bows"]
    elif "halloween" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Halloween"]
    elif "fall" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Fall Collection"]
    elif "spring" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Spring Collection"]
    elif "patriotic" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Patriotic"]
    elif "summer" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Summer Fun"]
    elif "mother" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Mom/Grandma Love"]
    elif (
        "christmas" in normalized_tags
        or "holiday" in normalized_tags
        or "winter" in normalized_tags
    ):
        return ETSY_SECTION_ID_DICT["Winter and Christmas"]
    elif "dog" in normalized_tags or "cat" in normalized_tags:
        return ETSY_SECTION_ID_DICT["Pet Lovers"]
    else:
        return ETSY_SECTION_ID_DICT["Beautiful Everyday"]


def format_materials_to_list(description: str) -> list:
    description_paragraphs = description.split("\n")
    materials_list = []
    material_paragraph = ""
    for paragraph in description_paragraphs:
        paragraph_normalized = paragraph.casefold()
        if "is made with" in paragraph_normalized or "is made on" in paragraph_normalized:
            material_paragraph = paragraph_normalized
            break

    material_line = ""
    if material_paragraph:
        lines = material_paragraph.split(".")
        for line in lines:
            if "is made with" in line or "is made on" in line:
                # split the line after the match
                line_split_with = line.split("is made with")
                line_split_on = line.split("is made on")
                if len(line_split_on) > 1:
                    material_line = line_split_on[1].strip()
                else:
                    material_line = line_split_with[1].strip()
                break

    if material_line:
        raw_list = material_line.split(",")
        for raw_material in raw_list:
            if "and" in raw_material:
                for material in raw_material.split("and"):
                    materials_list.append(material.strip().rstrip(".").title())
            else:
                materials_list.append(raw_material.strip().rstrip(".").title())

    return materials_list
