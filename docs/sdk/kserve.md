# KServe

The `KServeClient` provides a Python interface for managing `InferenceService` resources in a Kubeflow cluster.

## Getting Started

To use the `KServeClient`, you first need to create an instance of the client:

```python
from kubeflow.kserve.clients import KServeClient

client = KServeClient()
```

## Creating an InferenceService

To create an `InferenceService`, you first need to define the `InferenceService` object:

```python
from kubeflow.kserve.types import (
    InferenceService,
    ModelFormat,
    ModelSpec,
    PredictorSpec,
)

inferenceservice = InferenceService(
    name="my-inference-service",
    predictor=PredictorSpec(
        model=ModelSpec(
            model_format=ModelFormat(name="sklearn"),
            storage_uri="gs://my-bucket/my-model",
        )
    ),
)

client.create(inferenceservice)
```

## Getting an InferenceService

To get an `InferenceService`, you can use the `get` method:

```python
inferenceservice = client.get("my-inference-service")
```

## Listing InferenceServices

To list all `InferenceService` resources in a namespace, you can use the `list` method:

```python
inferenceservices = client.list()
```

## Deleting an InferenceService

To delete an `InferenceService`, you can use the `delete` method:

```python
client.delete("my-inference-service")
```
