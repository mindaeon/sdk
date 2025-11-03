# Welcome to the Kubeflow SDK

This is the documentation for the Kubeflow SDK.

## Getting Started

The main entrypoint for the Kubeflow SDK is the `KubeflowClient` class.
This class provides access to all the individual Kubeflow component SDKs.

### Example

```python
from kubeflow.client import KubeflowClient

# Initialize the client
client = KubeflowClient()

# Access the Trainer SDK
trainer = client.trainer
jobs = trainer.list_jobs()

# Access the Optimizer SDK
optimizer = client.optimizer
studies = optimizer.list_jobs()

# Access the Notebooks SDK
notebooks = client.notebooks
notebooks.list_notebooks()

# Access the Pipelines SDK
pipelines = client.pipelines
pipelines.pipeline.list_pipelines()
```
