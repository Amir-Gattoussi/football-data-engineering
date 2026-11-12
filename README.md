# football-data-foundations
Project
Hand-built tools for loading and standardising football (soccer) data,
starting with StatsBomb open event data. A learning project toward
football data engineering.

## Setup

    uv sync
    uv run pre-commit install

## Run the checks

    uv run pytest
    uv run ruff check .

## Data

Sample data is not committed. Download matches from the
statsbomb/open-data repository into `data/statsbomb/`.