# Web APIs

_Tip: use a `.env` file and `python-dotenv` to inject the secrets needed by most of the following Sensors and Outputs. [The setup section has more detail on how to do this](../setup/extras.md)._

## Third party API proxy Sensors

Third party data can be ingested, alongside real sensors.

_While third party data can be visualised directly from the API or the third party app / website, it's useful to collect it like other sensor data, so it can be stored / processed in the same way._

### Octopus Energy

Outputs KWh consumption from a specified Smart Meter in [half hour intervals](https://developer.octopus.energy/docs/api/#consumption). At the time of writing, data is only available for the previous day sometime on the following day (not sure exactly when).

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[octopus]
```

See [examples/web_apis/octopus.py](../../examples/web_apis/octopus.py).

### Awair

Outputs raw (unaveraged) data from all sensors of a specified device every 5 minutes. The long period is necessary due to the severe rate limiting Awair have on [their API](https://docs.developer.getawair.com/#local-api).

This proxy Sensor can also auto-discover devices associated with an account, which is more convenient than having to manually find and specify the details of each device.

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[awair]
```

See [examples/web_apis/awair.py](../../examples/web_apis/awair.py).

## Remote API Outputs (storage)

### Grafana

`GraphiteOutput` sends batches of Readings to Grafana Cloud, who provide [a custom ingest endpoint for Graphite metrics](https://grafana.com/docs/grafana-cloud/metrics-graphite/http-api/). Metric names are of the form `<prefix>.<sensor name>.<reading name>`, where `<prefix>` is the hostname of the machine when created using `GraphiteOutput.from_env()`.

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[grafana]
```

See [examples/web_apis/grafana.py](../../examples/web_apis/grafana.py).

### InfluxDB

Sends batches of Readings as "points" to a specified InfluxDB bucket at a specified endpoint e.g. [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud). Each point is named after the Reading and tagged by **sensor** and **host**.

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[influxdb]
```

See [examples/web_apis/influxdb.py](../../examples/web_apis/influxdb.py).
