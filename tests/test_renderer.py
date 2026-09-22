import json

from bag_amsterdam_api.bevragingen.renderers import HALJSONRenderer


def test_json_rendering():
    renderer = HALJSONRenderer()
    data = {"foo": "1", "bar": "2"}

    result = renderer.render(data=data)

    assert renderer.media_type == "application/hal+json"
    assert renderer.format == "json"
    assert json.loads(result) == data
