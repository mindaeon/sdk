# Model Registry

The `ModelRegistryClient` provides a Python interface for managing resources in the Kubeflow Model Registry.

## Getting Started

To use the `ModelRegistryClient`, you first need to create an instance of the client:

```python
from kubeflow.model_registry.clients import ModelRegistryClient

client = ModelRegistryClient()
```

## Creating a Registered Model

To create a `RegisteredModel`, you first need to define the `RegisteredModelCreate` object:

```python
from kubeflow.model_registry.types import RegisteredModelCreate

registered_model = RegisteredModelCreate(
    name="my-model",
)

client.create_registered_model(registered_model)
```

## Creating a Model Version

To create a `ModelVersion`, you first need to define the `ModelVersionCreate` object:

```python
from kubeflow.model_registry.types import ModelVersionCreate

model_version = ModelVersionCreate(
    name="my-version",
    registered_model_id="my-model-id",
)

client.create_model_version(model_version)
```

## Creating a Model Artifact

To create a `ModelArtifact`, you first need to define the `ModelArtifactCreate` object:

```python
from kubeflow.model_registry.types import ModelArtifactCreate

model_artifact = ModelArtifactCreate(
    name="my-artifact",
)

client.create_model_artifact(model_artifact)
```
