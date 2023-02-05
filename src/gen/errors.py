# create looker exception class and raise an exception
class ViewHasNoFieldsException(Exception):
    "This Looker object has no fields"
    pass


class LookerColumnTypeNotFound(Exception):
    def __init__(self, bigquery_type):
        super().__init__("Type {bigquery_type} not in types")
