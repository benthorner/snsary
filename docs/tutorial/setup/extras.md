# Pre-built sensors and outputs

The [rest of the tutorial](../README.md) covers many of these in detail. An example of a pre-built Output is the `GraphiteOutput`, which POSTs readings to a specified Graphite web API.

Some of the extra Sensors and Outputs need additional dependencies to work. To avoid making the core Snsary package too big, you need to specify which extras you want:

```bash
# a specific extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[graphite]

# all extras
... #egg=snsary[all]
```

Some of the Sensors and Outputs need to be configured with secrets e.g. an API token. You can use a `.env` file and `python-dotenv` to inject environment variables e.g.

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

See the rest of the documentation for the variables expected by each Sensor and Output.
