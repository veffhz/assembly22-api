from apispec import BasePlugin


class DisableOptionsOperationPlugin(BasePlugin):

    def operation_helper(self, path=None, operations=None, **kwargs):
        # flask-apispec auto generates an options operation, which cannot handled by apispec.
        # apispec.exceptions.DuplicateParameterError: Duplicate parameter with name body and location body
        # => remove
        operations.pop("options", None)
