# Spark Operator

The `SparkClient` provides a Python interface for managing `SparkApplication` resources in a Kubeflow cluster.

## Getting Started

To use the `SparkClient`, you first need to create an instance of the client:

```python
from kubeflow.spark_operator.clients import SparkClient

client = SparkClient()
```

## Creating a SparkApplication

To create a `SparkApplication`, you first need to define the `SparkApplication` object:

```python
from kubeflow.spark_operator.types import (
    DriverSpec,
    ExecutorSpec,
    SparkApplication,
    SparkApplicationSpec,
)

spark_application = SparkApplication(
    name="my-spark-app",
    spec=SparkApplicationSpec(
        type="Scala",
        sparkVersion="3.1.1",
        mode="cluster",
        mainApplicationFile="local:///opt/spark/examples/jars/spark-examples_2.12-3.1.1.jar",
        driver=DriverSpec(cores=1, memory="512m"),
        executor=ExecutorSpec(instances=1, cores=1, memory="512m"),
    ),
)

client.create(spark_application)
```
