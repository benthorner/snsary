import json
import os
from pathlib import Path

import httpretty
import pytest

from snsary.contrib.datastax import GraphQLOutput


# extracted using the following in a live GraphQL session:
#
#     with client as sess: sess.fetch_schema()
#     file = open('tests/contrib/datastax/schema.json', 'w')
#     file.write(json.dumps(data=client.introspection))
@pytest.fixture()
def schema():
    file = f"{Path(__file__).parent}/schema.json"
    return open(file, 'r').read()


@pytest.fixture
@httpretty.activate(allow_net_connect=False)
def graphql(schema, mocker):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphql/',
        content_type='application/json',
        body=schema
    )

    mocker.patch('platform.node', return_value='snsary')

    return GraphQLOutput(
        url="http://graphql", token="token"
    )


def test_from_env(mocker):
    mocker.patch.dict(os.environ, {
        'DATASTAX_URL': 'url',
        'DATASTAX_TOKEN': 'token',
    })

    mock_init = mocker.patch.object(
        GraphQLOutput, '__init__',
        return_value=None  # required to mock __init__
    )

    assert isinstance(
        GraphQLOutput.from_env(), GraphQLOutput
    )

    mock_init.assert_called_with(
        url='url', token='token'
    )


@httpretty.activate(allow_net_connect=False)
def test_publish_batch(graphql, reading):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphql/',
        content_type='application/json',
        body='{"data": []}'
    )

    graphql.publish_batch([reading])
    request = httpretty.last_request()

    # extracted using the following in a debugger session
    # pprint(json.loads(str(request.body, 'utf-8')))
    assert json.loads(request.body) == {
        'query': 'mutation {\n'
        '  r0: insertreading(\n'
        '    options: {ttl: 33696000}\n'
        '    value: {hostname: "snsary", sensor: "mysensor", metric: '
        '"myreading", timestamp: "2022-04-23T19:25:46+00:00", value: 123}\n'
        '  ) {\n'
        '    value {\n'
        '      metric\n'
        '    }\n'
        '  }\n'
        '}'
    }


@httpretty.activate(allow_net_connect=False)
def test_publish_batch_error(
    graphql,
    sensor,
    reading
):
    httpretty.register_uri(
        httpretty.POST,
        'http://graphql/',
        content_type='application/json',
        status=500
    )

    with pytest.raises(Exception) as excinfo:
        graphql.publish_batch([reading])

    assert 'Internal Server Error' in str(excinfo.value)
