from snsary.outputs import FilterOutput, Output


def test_str():
    output = Output()
    filtered = FilterOutput(output, 'filter')
    assert str(filtered) == f'{str(output)} (filtered)'
