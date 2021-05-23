from apispec import APISpec
from apispec.exceptions import APISpecError
from apispec.ext.marshmallow import MarshmallowPlugin


def generate_swagger_file(file_location, handlers):
    spec = APISpec(
        title="Widget",
        version="1.0.0",
        openapi_version="3.0.2",
        info=dict(description="Widget API"),
        plugins=[MarshmallowPlugin()],
        servers=[
            {"url": "http://localhost:888/",
             "description": "Local Environment"}
        ]

    )

    spec.components.schema(
        "Widget",
        {
            "properties": {
                "id": {"type": "integer", "format": "int64"},
                "name": {"type" : "string"},
                "number_of_parts": {"type": "integer", "format": "int64"},
                "created_date": {"type": "string"},
                "updated_date": {"type": "string"},
            }
        }
    )
    spec.path(
        path="/widgets",
        operations=dict(
            get=dict(
                parameters=[{"name": "page", "in": "query",
                             "type": "integer"},
                            {"name": "page_size",
                             "type": "int64", "in": "query"}],
                responses=
                {"200":
                 {"content":
                  {"application/json":
                   {"schema": {"array": "Widget"}}}}}
            ),
        ),
    )
    spec.path(
        path="/widgets",
        operations=dict(
            post=dict(
                responses=
                {"201":
                 {"content":
                  {"application/json":
                   {"schema": "Widget"}}}},
                requestBody={
                    "content": {"application/json":
                                {"schema": "Widget"}
                    }
                }
            ),
        ),
    )
    spec.path(
        path="/widgets/{widget_id}",
        operations=dict(
            get=dict(
                responses=
                {"200":
                 {"content":
                  {"application/json": {"schema": "Widget"}}}}
            ),
            delete=dict(
                responses=
                {"204" : {}}
            ),
        ),
        parameters=[{"name": "widget_id", "type": "int64", "in": "path"}]
    )
    spec.path(
        path="/widgets/{widget_id}",
        operations=dict(
            put=dict(
                responses=
                {"200" :
                 {"content": {"application/json": {"schema": "Widget"}}}},
                requestBody={
                    "content": {"application/json":
                                {"schema": "Widget"}
                    }
                }
            ),
        ),
    )

    for handler in handlers:
        try:
            spec.path(urlspec=handler)
        except APISpecError:
            pass
    with open(file_location, "w", encoding="utf-8") as f:
        f.write(spec.to_yaml())
