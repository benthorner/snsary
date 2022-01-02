# Pre-built Sensors and Outputs

These include:

- [Sensors for serial hardware](serial.md)
- [Sensors for I2C hardware](i2c.md)
- [Sensors and Outputs for Web APIs](web_apis.md)
- [Sensors for GPIO hardware](gpio.md)

## Installation

Some of the extra Sensors and Outputs need additional dependencies to work. To avoid making the core Snsary package too big, you need to specify which extras you want:

```bash
# a specific extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[grafana]

# all extras
... #egg=snsary[all]
```

The name of the extra is the same as the name of the module that provides it e.g. [`GraphiteOutput` is in the `grafana` module](https://snsary.readthedocs.io/en/latest/autoapi/snsary/contrib/grafana/index.html), so the extra to request dependencies for is `grafana`.

## Configuration

Some of the extra Sensors and Outputs need to be configured with secrets e.g. an API token. You can use a `.env` file and [python-dotenv](https://github.com/theskumar/python-dotenv) to inject environment variables e.g.

```bash
# .env
GRAPHITE_URL=http://user:password@graphite
```

```python
from dotenv import load_dotenv
load_dotenv()

# manually read each variable
GraphiteOutput(url=os.environ['GRAPHITE_URL'])

# read from expected variables
GraphiteOutput.from_env()
```

See [the API docs](https://snsary.readthedocs.io/en/latest/index.html) for the variables expected by each Sensor and Output.
