from collections import namedtuple

import pytest

from snsary.utils import scraper

test_namedtuple = namedtuple(
    'test', ['string', 'int', 'float']
)


@pytest.mark.parametrize('value, expected', [
    (
        1, [('prefix', 1)]
    ),
    (
        1.23, [('prefix', 1.23)]
    ),
    (
        'a-string', []
    ),
    (
        [
            test_namedtuple('a-string', 1, 1.23)
        ],
        [
            ('prefix-0-int', 1),
            ('prefix-0-float', 1.23),
        ]
    ),
    (
        ('a-string', 1, 1.23),
        [
            ('prefix-1', 1),
            ('prefix-2', 1.23)
        ]
    ),
    (
        {
            'key1': ('a-string',),
            'key2': 1,
            'key3': (1.23,)
        },
        [
            ('prefix-key2', 1),
            ('prefix-key3-0', 1.23)
        ]
    )
])
def test_extract_from(value, expected):
    assert list(
        scraper.extract_from(value, prefix='prefix')
    ) == expected


def test_for_class():
    class MockClass:
        @property
        def prop_1(self):
            return 1

        @property
        def prop_2(self):
            return (1.1, 2.2)

        @property
        def _prop_3(self):
            return 2

    class_scraper = scraper.for_class(MockClass)
    results = class_scraper(MockClass())

    assert list(results) == [
        ('prop_1', 1),
        ('prop_2-0', 1.1),
        ('prop_2-1', 2.2),
    ]
