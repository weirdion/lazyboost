# LazyBoost

A simple way to manage your shop listings between Etsy Shop Manager and Facebook Page Shop

## Features

    [x] Fetch all active listings from Etsy
    [x] Fetch all images for each active listing
    [] Allow creating listing on Etsy
    [] Allow updating listing on Etsy

    [] Convert Etsy listing to Facebook CSV import file
    [] Etsy --> Facebook listing delta update
    [] Facebook --> Etsy listing delta update
    [] Etsy <--> Facebook listing sync

    [] Fetch all active listings from Facebook
    [] Allow creating list on Facebook
    [] Allow updating list on Facebook

## Dependencies

 1. [jq] - Needed for parsing Pipfile.lock and updating requirements.txt (development only).
 2. [requests] - Python package, needed for making requests with different API.
 3. [urllib3] - Python package, needed for manipulating urls.

## Preparing for Development

1. Ensure ``pip`` and ``pipenv`` are installed
2. Clone repository
3. ``cd`` into repository
4. Fetch development dependencies ``make``
5. Initiate a local install for virtual system directories ``make install-pipenv``
6. Activate virtualenv: ``pipenv shell``

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
    Copyright (C) 2020  Ankit Sadana

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


[jq]: <https://stedolan.github.io/jq/>
[requests]: <https://github.com/psf/requests>
[urllib3]: <https://github.com/urllib3/urllib3>
[pipeline_image]: <https://gitlab.com/asadana/lazyboost/badges/develop/pipeline.svg>
[coverage_image]: <https://gitlab.com/asadana/lazyboost/badges/develop/coverage.svg>
