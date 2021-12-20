from snsary.sources import Source


def test_str():
    assert str(Source()).startswith('source')
