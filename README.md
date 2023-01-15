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

## Testing

Tests are written using pytest. To run the tests, run the following command:

```coverage run -m pytest```

Get coverage: ```coverage report```
