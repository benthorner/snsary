from .logging import logger


def simple_scraper(value, name=''):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from simple_scraper(item, name=f'{name}-{key}')

    elif hasattr(value, '_asdict'):
        yield from simple_scraper(value._asdict(), name=name)

    elif isinstance(value, (tuple, list)):
        for index, item in enumerate(value):
            yield from simple_scraper(item, name=f'{name}-{index}')

    elif isinstance(value, int):
        yield (name, int(value))

    elif isinstance(value, float):
        yield (name, value)

    else:
        logger.debug(f"Ignoring {value} as not a number.")


class property_scraper:
    def __init__(self, klass):
        self.__props = [
            name for name, value in vars(klass).items()
            if isinstance(value, property)
            and not name.startswith('_')
        ]

    def __call__(self, instance):
        for prop in self.__props:
            value = getattr(instance, prop)
            yield from simple_scraper(value, prop)
