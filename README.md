# Looker Generator

Looker Generator is a tool to generate LookML from BigQuery database schema.

## Installation

### Prerequisites

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


- Python 3.9 or later
- `pip install -r requirements.txt`

### Creating a view

1. Create a view in BigQuery in `ct-looker-*
2. Create a file in `looker_generator/views` with the same name as the view and fill out the relevant details
3. Run the application

## What this does

It does a few things with a view:

1. Adds a description to the view if one exists in the table
2. Identify dimensions, dimension_groups and measures
3. Creates nested views for each array field
4. Tries to identify Primary Keys if the column is called ID, PK or primary)key
5. Light-touch labelling of potentially diagnostic or Snowplow-identifiable fields
6. Remove `time` from date-based dimension groups
7. it 

## Testing

Tests are written using pytest. To run the tests, run the following command:

```coverage run -m pytest```

Get coverage: ```coverage report```
