# In-built processing tools

An app in Snsary is made up of **Sources** and **Outputs**. A `Source` can `subscribe` one or more `Output` objects, which have a `publish` method to receive **Readings** i.e. data.

```python
# publish / subscribe pattern
# raises NotImplementedError
Source().subscribe(MockOutput())
```

**PollingSensors** are a type of `Source` that can `start` and `stop` i.e. a **Service**. Every instance of a `Service` is recorded in `Service.instances`, so the following should be equivalent:

```python
# assign for later use
sensor = MockSensor()
sensor.subscribe(MockOutput())

# specific, direct control
sensor.start()
sensor.stop()
```

```python
# no need to assign
MockSensor().subscribe(MockOutput())

# general, central control
system.start()
system.stop()
```

Outputs can also be Services. These concepts are all you need to build an app, but Snsary has a few more tools to hide some of the complexity and reduce the amount of code needed.

## Streams

A `Stream` is an `Output` and a `Source`. Being an `Output` means Sources can feed into it. Being a `Source` means it can feed Outputs. Different streams provide different functionality.

- `AsyncStream` creates a thread for each `Output` that subscribes to it. Any Readings are published to a separate queue for each output, with the thread logging any errors from relaying to it. Using an `AsyncStream` helps avoid issues due to flakey or time-consuming Outputs.

- `FilterStream` only publishes a `Reading` if it returns `True` when passed through a _filter function_. Any `Stream` can be filtered e.g. `stream.filter(lambda r: True)`. To help make filter functions there is [a `Filter` utility](../../../src/snsary/utils/filter.py), as well as `stream.filter_names('a', 'b', 'c')`.

Streams also make it easy to subscribe multiple outputs with `into`:

```python
# same as calling "subscribe" for each
stream.into(MockOutput(), MockOutput())
```

All **Sensors** expose a stream of their Readings, so you can do e.g.

```python
MockSensor().stream.filter_names('a').into(MockOutput(), MockOutput())
```

## Sources

Manually subscribing each source to each output is repetitive, especially when there are multiple outputs. This is where the `MultiSource` class can save some typing by combining multiple Sources as one. Just like a `Sensor`, a `MultiSource` also exposes a stream to make it easier to work with.

```python
MultiSource(MockSensor(), MockSensor()).stream.into(MockOutput())
```

## Outputs

Depending on the output, it may be more efficient to dispatch multiple Readings together. This can be done by inheriting from [`BatchOutput`](../../../src/snsary/outputs/batch_output.py), which requires a `publish_batch` method. `BatchOutput` is also a `Service` and will try to publish any remaining Readings when told to `stop()`.

See [the Web APIs section for examples of batched Outputs](../web_apis/README.md).
