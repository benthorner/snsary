from snsary.utils import Filter


def test_call():
    assert Filter()('reading')
    assert not Filter(lambda _: False)('reading')


def test_sensor_name(reading):
    assert not Filter.sensor_name('other')(reading)
    assert Filter.sensor_name('mysensor')(reading)


def test_invert():
    assert not Filter().invert('reading')
    assert Filter(lambda _: False).invert('reading')


def test_names(reading):
    assert not Filter.names([])(reading)
    assert not Filter.names('other')(reading)
    assert Filter.names('other', 'myreading')(reading)
