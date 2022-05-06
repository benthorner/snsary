"""
Sends batches of :mod:`Readings <snsary.models.reading>` as rows to Google BigQuery to be stored in a dataset / table called ``snsary.readings``, using `the BigQuery Python client <https://github.com/googleapis/python-bigquery>`_.

Configuration should be in `a JSON credentials file <https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating>`_, the path to which should be specified using the environment variable ``GOOGLE_APPLICATION_CREDENTIALS``.

Setting up BigQuery
===================

You can use the BigQuery UI to do most of the setup.

1. Create a dataset called ``snsary``.

    - Do not enable table expiration (this is different to partition expiration).

2. Create a table called ``readings``.

    - Add columns ``timestamp``, ``host``, ``sensor``, ``metric`` and ``value``.
    - Use ``TIMESTAMP`` for ``timestamp``, ``FLOAT`` for ``value`` and otherwise ``STRING``.
    - Partition the table **by day** using values of the **timestamp** column.

3. Set up partition expiration e.g. ::

       ALTER TABLE snsary.readings
       SET OPTIONS (
        partition_expiration_days=425
       )

You will also need to create `a Google Cloud service account <https://cloud.google.com/iam/docs/service-accounts>`_ and corresponding API key. The service account should have the "BigQuery Data Editor" role or similar.

Querying the data
=================

Example query for data in the table: ::

    SELECT $__timeGroup(timestamp,$__interval), sensor, metric, avg(value)
    FROM `snsary.readings`
    where $__timeFilter(timestamp)
    group by $__timeGroup(timestamp,$__interval), sensor, metric
    order by 1 asc

Note that the ``$__`` functions are `defined by Grafana <https://grafana.com/grafana/plugins/grafana-bigquery-datasource/>`_. A service account reading the data will need to have "BigQuery Data Viewer" and "BigQuery Job User" roles.
"""
import platform

import pytz
from google.api_core.retry import Retry
from google.cloud import bigquery

from snsary.outputs import BatchOutput


class BigQueryOutput(BatchOutput):
    def __init__(self, retry_deadline=10):
        BatchOutput.__init__(self)
        self.__retry_deadline = retry_deadline
        self.__client = bigquery.Client()
        self.__table = self.__client.get_table("snsary.readings")

    def publish_batch(self, readings):
        errors = self.__client.insert_rows_json(
            self.__table,
            [self.__row(reading) for reading in readings],
            retry=Retry(deadline=self.__retry_deadline)
        )

        # useful to catch setup errors like incorrect table column names
        for row_error in errors:
            self.logger.error(f'Error inserting row: #{row_error}')

    def __row(self, reading):
        return {
            # using UTC ensures test stability when run in different zones
            'timestamp': reading.datetime.astimezone(pytz.utc).isoformat(),
            'host': platform.node(),
            'sensor': reading.sensor_name,
            'metric': reading.name,
            'value': reading.value,
        }
