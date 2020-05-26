from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

from application.plugins import DisableOptionsOperationPlugin

api_spec = {
    'APISPEC_SPEC': APISpec(
        title='assembly22',
        version='v1',
        plugins=[
            MarshmallowPlugin(schema_name_resolver=lambda _: False),  # hack to disable warnings
            DisableOptionsOperationPlugin()
        ],
        openapi_version="2.0",
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
}
