# Contributing

PRs welcome, especially with some tests!

Feel free to update the [CHANGELOG](CHANGELOG.md) and [version](setup.py) as well.

## Getting started

First install and test the core package.

```
make bootstrap

make test
```

## Contrib ('extras')

Optional ('extra') sensors and outputs are located in [`contrib/`](src/snsary/contrib/). The dependencies for each extra can be installed separately - extras shouldn't rely on each other's dependencies.

To install and test an existing extra:

```
make bootstrap-contrib-<extra>

make test-contrib-<extra>
```

Extras have a `requirements/<extra>/` directory for dependencies:

- `extra.txt` - additional runtime dependencies for `<extra>`
- `tests.txt` - additional test dependencies for `<extra>`

Each extra is discovered automatically for installation and testing:

- `pip install snsary[<extra>]` finds its runtime dependencies
- [`ci.yml`](.github/workflows/ci.yml) will run the above `make` commands in isolation

You can also install test everything:

```
make bootstrap-all

make test-all
```

## Documentation

Most of this should be in the form of docstrings. Run `make docs` to continuously build the docs. Preview at `localhost:8000` or via the output files in `tmp/docs`.

In [docs/extras](docs/extras) there is also a higher-level guide with setup instructions, shopping links and examples for different types of hardware e.g. serial, I2C.
