def identify_value_format_name(type):
    type = type.lower()
    default_value = "decimal_2"
    default_percentage = "percent_2"
    possibles = {
        "global": "gbp",
        "usd": "usd",
        "ratio": default_percentage,
        "percent": default_percentage,
        "pct": default_percentage,
    }
    for key, value in possibles.items():
        if key in type:
            return value
    return default_value


class Measure:
    def __init__(self, properties):
        self.properties = properties
        self.metrics: list = []
        self._set_sql_reference()
        self._set_name()
        self._create_metrics()

    def measures(self) -> list:
        return self.metrics

    def _set_sql_reference(self):
        if self.properties.get("sql"):
            # set sql to name wrapped in curly brackets
            self.properties["sql"] = f"{{self.properties['name']}}"

    def _set_name(self):
        self.properties["name"] = f"m_{self.properties['name']}"

    def _create_metrics(self):
        metrics = [
            {
                "type": "sum",
                "title": "Sum",
            },
            {
                "type": "count",
                "title": "Total",
            },
            {
                "type": "average",
                "title": "Average",
            },
        ]
        output_metrics = []
        for metric in metrics:
            metric_name = metric["type"].lower()
            metric_titlecase = metric["title"].title()
            m = self.properties.copy()

            m["type"] = metric

            # Add metric details to name, label
            m["field_type"] = "measure"
            m["name"] = f"{self.properties['name']}__{metric_name}"
            m["label"] = f"{self.properties['label']} ({metric_titlecase})"
            # Add metric details to description
            if m.get("description"):
                m["description"] = f"{m['description']} ({metric_titlecase})"
            else:
                m["description"] = f"{metric_titlecase} of {m['label']}"
            # Set the value_format_name
            m["value_format_name"] = identify_value_format_name(m["name"])

            output_metrics.append(m)

        self.metrics = output_metrics
