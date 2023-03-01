# LazyBoost

Python application to pull and sync Orders and Listings between Shopify and Etsy. 

## Features


## Dependencies

 1. [shopifyapi] - Shopify API - Python version for Admin API.
 2. [requests] - Python package needed for making requests with different API.
 3. [pyperclip] - Clipboard manager that uses underlying system's clipboard.
 4. [python-dotenv] - `.env` handler for python.

## Preparing for Development

1. Ensure `pip` and `poetry` are installed
2. Clone repository
3. `cd` into repository
4. Fetch development dependencies `make`
5. Initiate a local install for virtual system directories `make install`
6. Activate virtualenv: `poetry shell`

## Usage

To view the help page, and all available options,

```sh
    $ lazyboost --help
```

## Running Tests

Run tests:

```sh
    $ make test
```

License
---

    LazyBoost
    Copyright (C) 2023  Ankit Sadana

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


[shopifyapi]: <https://github.com/Shopify/shopify_python_api>
[requests]: <https://github.com/psf/requests>
[pyperclip]: <https://github.com/asweigart/pyperclip>
[python-dotenv]: <https://github.com/theskumar/python-dotenv>
[pipeline_image]: <https://gitlab.com/asadana/lazyboost/badges/develop/pipeline.svg>
[coverage_image]: <https://gitlab.com/asadana/lazyboost/badges/develop/coverage.svg>
