# Creating a new view

To create a new view in Looker, you need to create a `.yaml` file in the `views` directory.

## View file structure


### name

Name of the view as it will appear in Looker.

### reference

The fully qualified BigQuery reference, excluding region.

> "project.dataset.view"

### type

Set to "view"

### primary_key

Set to the primary key of the table.

If no primary key is available or provided, Looker will have difficulty accurately calculating metrics and will ask you to create a composite primary_key.

### overrides (struct)

convert_tz: default: no

### name
