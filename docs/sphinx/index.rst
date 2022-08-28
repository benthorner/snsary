API Reference
=============

An app in Snsary is made up of :mod:`Sources <snsary.sources.source>` and :mod:`Outputs <snsary.outputs.output>`. A :mod:`Source <snsary.sources.source>` can ``subscribe`` one or more :mod:`Output <snsary.outputs.output>` objects, which have a ``publish`` method to receive :mod:`Readings <snsary.models.reading>` i.e. data. ::

    # publish / subscribe pattern
    # raises NotImplementedError
    Source().subscribe(MockOutput())

:mod:`PollingSensors <snsary.sources.polling_sensor>` are a type of Source that can ``start`` and ``stop`` i.e. a :mod:`Service <snsary.system.service>`. Every instance of a :mod:`Service <snsary.system.service>` is recorded in ``Service.instances``, so the following should be equivalent: ::

    # assign for later use
    sensor = MockSensor()
    sensor.subscribe(MockOutput())

    # specific, direct control
    sensor.start()
    sensor.stop()

::

    # no need to assign
    MockSensor().subscribe(MockOutput())

    # general, central control
    system.start()
    system.stop()

:mod:`Outputs <snsary.outputs.output>` can also be :mod:`Services <snsary.system.service>`. These concepts are all you need to build an app, but Snsary has a few more tools to hide some of the complexity and reduce the amount of code needed:

- :mod:`Streams <snsary.streams>` and :mod:`MultiSource <snsary.sources.multi_source>` make it easier to connect :mod:`Sources <snsary.sources.source>` to :mod:`Outputs <snsary.outputs.output>`.
- :mod:`BatchOutput <snsary.outputs.batch_output>` makes it easier to build efficient :mod:`Outputs <snsary.outputs.output>` for Web APIs.

Table of contents
=================

.. toctree::
   :titlesonly:

   /./autoapi/snsary/index
