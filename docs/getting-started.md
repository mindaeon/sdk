# Getting Started with the Kubeflow SDK

This guide will walk you through the process of installing the Kubeflow SDK, configuring it, and running your first pipeline.

## Installation

The Kubeflow SDK is available on PyPI and can be installed with `pip`:

```bash
pip install kubeflow
```

## Configuration

The Kubeflow SDK can be configured using a `kubeflow_config.yaml` file, environment variables, or programmatically. For most users, the default configuration should be sufficient.

### `kubeflow_config.yaml`

By default, the SDK will look for a `kubeflow_config.yaml` file in the current directory or any parent directory. You can also specify the path to the config file using the `KUBEFLOW_CONFIG_FILE` environment variable.

Here is an example `kubeflow_config.yaml` file:

```yaml
client:
  namespace: my-namespace
auth:
  provider: kubeconfig
```

### Environment Variables

You can also configure the SDK using environment variables. The environment variables are prefixed with `KUBEFLOW_` and are case-insensitive. Nested keys are separated by `__`.

For example, to set the namespace, you would use the following environment variable:

```bash
export KUBEFLOW_CLIENT__NAMESPACE=my-namespace
```

## Running Your First Pipeline

The `hello-world.py` example demonstrates how to define a simple pipeline using the Python-native DSL and run it using the `PipelineClient`.

```python
from kubeflow.pipelines.api import PipelineClient, RunClient
from kubeflow.pipelines.compiler import Compiler
from kubeflow.pipelines.dsl import component, pipeline
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


@pipeline(name="hello-world")
def hello_world_pipeline(name: str):
    """A simple pipeline that greets the user."""
    say_hello(name=name)


if __name__ == "__main__":
    compiler = Compiler()
    pipeline_yaml = compiler.compile(hello_world_pipeline(name="world"))

    # In a real-world scenario, you would save this YAML to a file
    # and upload it to Kubeflow Pipelines.
    print(pipeline_yaml)
```
