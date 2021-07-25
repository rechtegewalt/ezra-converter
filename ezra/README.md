# ezra converter

Converting data about right-wing incidents in Thuringia (_Thüringen_), Germany as monitored by the NGO [ezra](https://ezra.de/).

We use an internal API to transform the data into another data format. So technically, we are not scraping.

-   Website: <https://ezra.de/chronik/>
-   API: <https://angstraeume.ezra.de/wp-json/ezra/v1/chronic">
-   Data: <https://morph.io/rechtegewalt/ezra-converter>

## Caveats

1. Not consindering `endDates` for now
2. Only using one location (the first in the array) if there are multiple.

## Usage

For local development:

-   Install [poetry](https://python-poetry.org/)
-   `poetry install`
-   `poetry run python scraper.py`

For Morph:

-   `poetry export -f requirements.txt --output requirements.txt`
-   commit the `requirements.txt`
-   modify `runtime.txt`

## Morph

This is scraper runs on [morph.io](https://morph.io). To get started [see the documentation](https://morph.io/documentation).
