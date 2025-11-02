# Kubeflow Pipelines Guide

The Kubeflow Pipelines integration in the SDK allows you to define, compile, and run your ML workflows using a Python-native DSL.

## Python-native DSL

The DSL (Domain-Specific Language) provides a way to define your pipelines and components in pure Python.

### `@dsl.component`

The `@dsl.component` decorator is used to define a pipeline component. A component is a self-contained set of code that performs a single task in your pipeline.

```python
from kubeflow.pipelines.dsl import component
from kubeflow.pipelines.types.component_spec import InputSpec

@component(
    name="say-hello",
    image="alpine:latest",
    inputs=[InputSpec(name="name", type="String")],
    command=["echo", "hello", "{{$.inputs.parameters['name']}}"],
)
def say_hello(name: str):
    """A simple component that prints a greeting."""
    print(f"Hello, {name}!")
```

### `@dsl.pipeline`

The `@dsl.pipeline` decorator is used to define a pipeline. A pipeline is a graph of components that are connected together.

```python
from kubeflow.pipelines.dsl import pipeline

@pipeline(name="hello-world")
def hello_world_pipeline(name: str):
    """A simple pipeline that greets the user."""
    say_hello(name=name)
```

## Compiler

The `Compiler` class is used to compile your Python-native DSL into the KFP IR YAML format, which can be understood by the Kubeflow Pipelines backend.

```python
from kubeflow.pipelines.compiler import Compiler

compiler = Compiler()
pipeline_yaml = compiler.compile(hello_world_pipeline(name="world"))
```

## API Clients

The SDK provides a set of API clients for interacting with the Kubeflow Pipelines API.

### `PipelineClient`

The `PipelineClient` is used to manage pipelines and pipeline versions.

```python
from kubeflow.pipelines.api import PipelineClient

client = PipelineClient()

# Create a pipeline
pipeline = client.create_pipeline("my-pipeline")

# Create a pipeline version
pipeline_version = client.create_pipeline_version(
    pipeline.pipeline_id, "v1", "pipeline.yaml"
)
```

### `RunClient`

The `RunClient` is used to manage pipeline runs.

```python
from kubeflow.pipelines.api import RunClient
from kubeflow.pipelines.types.run_types import PipelineVersionReference

client = RunClient()

# Create a run
run = client.create_run(
    "my-run",
    PipelineVersionReference(
        pipeline_id="my-pipeline-id",
        pipeline_version_id="my-version-id",
    ),
)
```

### `ExperimentClient`

The `ExperimentClient` is used to manage pipeline experiments.

```python
from kubeflow.pipelines.api import ExperimentClient

client = ExperimentClient()

# Create an experiment
experiment = client.create_experiment("my-experiment")
```
