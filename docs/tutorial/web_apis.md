# Web APIs

Third party data can be ingested, alongside real sensors.

_While third party data can be visualised directly from the API or the third party app / website, it's useful to collect it like other sensor data, so it can be stored / processed in the same way._

## Third party API proxy sensors

_Tip: use a `.env` file and `python-dotenv` to inject environment variables like `MY_API_TOKEN`._

### Octopus Energy

_Outputs KWh consumption from a specified Smart Meter in [half hour intervals](https://developer.octopus.energy/docs/api/#consumption). At the time of writing, data is only available for the previous day sometime after midnight on the following day.

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[octopus]
```

Add it to the list of sensors for an existing Snsary app.

```python
from snsary.contrib.octopus import OctopusSensor

...

    sensors=[
        ...
        OctopusSensor(
            mpan=os.environ['OCTOPUS_MPAN'],
            serial_number=os.environ['OCTOPUS_SERIAL'],
            token=os.environ['OCTOPUS_TOKEN'],
        ),
        ...
    ],

...
```

### Awair

_Outputs raw (unaveraged) data from all sensors of a specified device every 5 minutes. The long period is necessary due to the severe rate limiting Awair have on [their API](https://docs.developer.getawair.com/#local-api)._

_This proxy sensor can also auto-discover devices associated with an account, which is more convenient than having to manually find and specify the details of each device._

```
# install it as an extra
pip3 install git+https://github.com/benthorner/snsary#egg=snsary[awair]
```

Add it to the list of sensors for an existing Snsary app.

```python
from snsary.contrib.awair import AwairSensor

...

    sensors=[
        ...
        *AwairSensor.discover(token=os.environ['AWAIR_TOKEN']),
        ...
    ],

...
```


