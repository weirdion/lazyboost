#  LazyBoost: A lazy pythonian way to sync stuff between Shopify and Etsy.
#  Copyright (C) 2023  Ankit Patterson
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

import pyperclip
from aws_lambda_powertools import Logger

logger = Logger()


def update_clipboard_tags():
    current_clipboard = pyperclip.paste()
    current_clipboard = current_clipboard.splitlines()
    current_clipboard = [i for i in current_clipboard if i]
    current_clipboard.sort()

    logger.info(f"Cleaned up Etsy tags: {_etsy_description_tags(current_clipboard)}")
    logger.info(f"Cleaned up Facebook tags: {_facebook_post_description_tags(current_clipboard)}")
    pyperclip.copy(_etsy_description_tags(current_clipboard))
    pyperclip.copy(_facebook_post_description_tags(current_clipboard))


def _etsy_description_tags(tag_list: list) -> str:
    return ", ".join(tag_list)


def _facebook_post_description_tags(tag_list: list) -> str:
    fb_tag_list = []
    for t in tag_list:
        no_space_tag = {t.replace(" ", "").replace("'", "")}
        no_space_tag = f"#{no_space_tag}"
        if no_space_tag not in fb_tag_list:
            fb_tag_list.append(no_space_tag)

    return " ".join(fb_tag_list)
