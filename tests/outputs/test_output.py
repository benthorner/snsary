from snsary.outputs import Output


def test_str():
    assert str(Output()).startswith('output')
