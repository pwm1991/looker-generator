# Looker Generator
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Looker Generator is a tool to generate LookML from BigQuery database schema.

## Installation

- Python 3.9 or later
- `make setup`

### Authenticating with gcloud

`make auth`

You don't need a service key, but your personal account needs to be able to do fancy stuff in the project you want to generate views from.
### Update your env file

Create a `.env` file and fill in the relevant details. Use `.env.example` as a template.

### Creating a view

1. Create a view in BigQuery in `ct-looker-*
2. Create a file in `/configs` with the same name as the view and fill out the relevant details
3. `make run`


## What this does

It does a few things with a view:

1. Adds a description to the view if one exists in the table
2. Identify dimensions, dimension_groups and measures
3. Creates nested views for each array field
4. Tries to identify Primary Keys if the column is called ID, PK or primary)key
5. Light-touch labelling of potentially diagnostic or Snowplow-identifiable fields
6. Remove `time` from date-based dimension groups

## Testing

Tests are written using pytest. To run the tests, run the following command:

```make test```

A coverage report will be generated in the `coverage` directory.
